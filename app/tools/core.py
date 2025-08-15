from typing import (
    Any,
    Dict,
    Optional,
    AsyncIterator,
    Callable,
    TypeVar,
    Awaitable,
)
import os
import httpx
from contextlib import asynccontextmanager
from dataclasses import dataclass
from functools import wraps
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Constants
ANALYTICS_API_URL = os.getenv("ANALYTICS_API_URL", "http://localhost:8080")
ANALYTICS_USER = os.getenv("ANALYTICS_USER")
ANALYTICS_PASS = os.getenv("ANALYTICS_PASS")
TOKEN_CACHE_PATH = os.path.join(os.path.dirname(__file__), ".analytics_token")

@dataclass
class AnalyticsContext:
    """Context for the Analytics MCP server"""
    client: httpx.AsyncClient
    api_url: str
    access_token: Optional[str] = None
    csrf_token: Optional[str] = None

def load_cached_token() -> Optional[str]:
    """Load cached access token if it exists"""
    try:
        if os.path.exists(TOKEN_CACHE_PATH):
            with open(TOKEN_CACHE_PATH, "r") as f:
                return f.read().strip()
    except Exception:
        return None
    return None

def cache_access_token(token: str):
    """Cache access token to file"""
    try:
        with open(TOKEN_CACHE_PATH, "w") as f:
            f.write(token)
    except Exception as e:
        logger.warning(f"Warning: Could not cache access token: {e}")

@asynccontextmanager
async def analytics_lifespan(server: Any) -> AsyncIterator[AnalyticsContext]:
    """Manage application lifecycle for Analytics platform integration"""
    logger.info("Initializing Analytics context...")
    client = httpx.AsyncClient(base_url=ANALYTICS_API_URL, timeout=30.0)
    ctx = AnalyticsContext(client=client, api_url=ANALYTICS_API_URL)
    cached_token = load_cached_token()
    if cached_token:
        ctx.access_token = cached_token
        client.headers.update({"Authorization": f"Bearer {cached_token}"})
        logger.info("Using cached access token")
        try:
            response = await client.get("/api/v1/me/")
            if response.status_code != 200:
                logger.info(
                    f"Cached token is invalid (status {response.status_code}). Re-authentication required."
                )
                ctx.access_token = None
                client.headers.pop("Authorization", None)
        except Exception as e:
            logger.info(f"Error verifying cached token: {e}")
            ctx.access_token = None
            client.headers.pop("Authorization", None)
    try:
        yield ctx
    finally:
        logger.info("Shutting down Analytics context...")
        await client.aclose()

# Type variables
T = TypeVar("T")
R = TypeVar("R")

def requires_authentication(
    func: Callable[..., Awaitable[Dict[str, Any]]],
) -> Callable[..., Awaitable[Dict[str, Any]]]:
    """Decorator to check authentication before executing a function"""
    @wraps(func)
    async def wrapper(ctx: Any, *args, **kwargs) -> Dict[str, Any]:
        analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
        if not analytics_ctx.access_token:
            return {"error": "Not authenticated. Please authenticate first."}
        return await func(ctx, *args, **kwargs)
    return wrapper

def handle_platform_errors(
    func: Callable[..., Awaitable[Dict[str, Any]]],
) -> Callable[..., Awaitable[Dict[str, Any]]]:
    """Decorator to handle platform API errors consistently"""
    @wraps(func)
    async def wrapper(ctx: Any, *args, **kwargs) -> Dict[str, Any]:
        try:
            return await func(ctx, *args, **kwargs)
        except Exception as e:
            function_name = func.__name__
            return {"error": f"Error in {function_name}: {str(e)}"}
    return wrapper

async def fetch_csrf_token(ctx: Any) -> Optional[str]:
    """Fetch a CSRF token from the Analytics platform"""
    analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
    client = analytics_ctx.client
    try:
        response = await client.get("/api/v1/security/csrf_token/")
        if response.status_code == 200:
            data = response.json()
            csrf_token = data.get("result")
            analytics_ctx.csrf_token = csrf_token
            return csrf_token
        else:
            logger.info(
                f"Failed to fetch CSRF token: {response.status_code} - {response.text}"
            )
            return None
    except Exception as e:
        logger.info(f"Error fetching CSRF token: {str(e)}")
        return None

async def make_platform_request(
    ctx: Any,
    method: str,
    endpoint: str,
    data: Dict[str, Any] = None,
    params: Dict[str, Any] = None,
    auto_refresh: bool = True,
) -> Dict[str, Any]:
    """Helper function to make API requests to the Analytics platform"""
    analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
    client = analytics_ctx.client
    if method.lower() != "get" and not analytics_ctx.csrf_token:
        await fetch_csrf_token(ctx)
    async def make_request() -> httpx.Response:
        headers = {}
        if method.lower() != "get" and analytics_ctx.csrf_token:
            headers["X-CSRFToken"] = analytics_ctx.csrf_token
        if method.lower() == "get":
            return await client.get(endpoint, params=params)
        elif method.lower() == "post":
            return await client.post(
                endpoint, json=data, params=params, headers=headers
            )
        elif method.lower() == "put":
            return await client.put(endpoint, json=data, headers=headers)
        elif method.lower() == "delete":
            return await client.delete(endpoint, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
    response = (
        await auto_refresh_token(ctx, make_request)
        if auto_refresh
        else await make_request()
    )
    if response.status_code not in [200, 201]:
        return {
            "error": f"API request failed: {response.status_code} - {response.text}"
        }
    return response.json()

async def auto_refresh_token(
    ctx: Any, api_call: Callable[[], Awaitable[httpx.Response]]
) -> httpx.Response:
    """Handle automatic token refreshing for API calls"""
    analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
    if not analytics_ctx.access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        response = await api_call()
        if response.status_code != 401:
            return response
    except httpx.HTTPStatusError as e:
        if e.response.status_code != 401:
            raise e
        response = e.response
    except Exception as e:
        raise e
    logger.info("Received 401 Unauthorized. Attempting to refresh token...")
    from .auth import analytics_auth_refresh_token, analytics_auth_authenticate_user
    refresh_result = await analytics_auth_refresh_token(ctx)
    if refresh_result.get("error"):
        logger.info(
            f"Token refresh failed: {refresh_result.get('error')}. Attempting re-authentication..."
        )
        auth_result = await analytics_auth_authenticate_user(ctx)
        if auth_result.get("error"):
            raise HTTPException(status_code=401, detail="Authentication failed")
    return await api_call()
