from typing import Any, Dict, Optional
from .core import (
    AnalyticsContext,
    cache_access_token,
    fetch_csrf_token,
    handle_platform_errors,
    ANALYTICS_USER,
    ANALYTICS_PASS,
)

def register_auth_tools(mcp):
    @mcp.tool()
    @handle_platform_errors
    async def analytics_auth_check_token_validity(ctx: Any) -> Dict[str, Any]:
        """
        Check if the current access token is valid
        Makes a request to the /api/v1/me/ endpoint to verify token validity.
        Returns:
            A dictionary with token validity status and any error details
        """
        analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
        if not analytics_ctx.access_token:
            return {"valid": False, "error": "No access token available"}
        try:
            response = await analytics_ctx.client.get("/api/v1/me/")
            if response.status_code == 200:
                return {"valid": True}
            else:
                return {
                    "valid": False,
                    "status_code": response.status_code,
                    "error": response.text,
                }
        except Exception as e:
            return {"valid": False, "error": str(e)}

    @mcp.tool()
    @handle_platform_errors
    async def analytics_auth_refresh_token(ctx: Any) -> Dict[str, Any]:
        """
        Refresh the access token using the refresh endpoint
        Makes a request to the /api/v1/security/refresh endpoint to obtain a new access token.
        Returns:
            A dictionary with the new access token or error details
        """
        analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
        if not analytics_ctx.access_token:
            return {"error": "No access token to refresh. Please authenticate first."}
        try:
            response = await analytics_ctx.client.post("/api/v1/security/refresh")
            if response.status_code != 200:
                return {
                    "error": f"Failed to refresh token: {response.status_code} - {response.text}"
                }
            data = response.json()
            access_token = data.get("access_token")
            if not access_token:
                return {"error": "No access token returned from refresh"}
            cache_access_token(access_token)
            analytics_ctx.access_token = access_token
            analytics_ctx.client.headers.update({"Authorization": f"Bearer {access_token}"})
            return {
                "message": "Successfully refreshed access token",
                "access_token": access_token,
            }
        except Exception as e:
            return {"error": f"Error refreshing token: {str(e)}"}

    @mcp.tool()
    @handle_platform_errors
    async def analytics_auth_authenticate_user(
        ctx: Any,
        username: Optional[str] = None,
        password: Optional[str] = None,
        refresh: bool = True,
    ) -> Dict[str, Any]:
        """
        Authenticate with the Analytics platform and obtain an access token
        Makes a request to the /api/v1/security/login endpoint.
        Args:
            username: Analytics platform username (falls back to environment variable)
            password: Analytics platform password (falls back to environment variable)
            refresh: Whether to refresh the token if invalid (defaults to True)
        Returns:
            A dictionary with authentication status and access token or error details
        """
        analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
        if analytics_ctx.access_token:
            validity = await analytics_auth_check_token_validity(ctx)
            if validity.get("valid"):
                return {
                    "message": "Already authenticated with valid token",
                    "access_token": analytics_ctx.access_token,
                }
            if refresh:
                refresh_result = await analytics_auth_refresh_token(ctx)
                if not refresh_result.get("error"):
                    return refresh_result
        username = username or ANALYTICS_USER
        password = password or ANALYTICS_PASS
        if not username or not password:
            return {
                "error": "Username and password must be provided via arguments or environment variables"
            }
        try:
            response = await analytics_ctx.client.post(
                "/api/v1/security/login",
                json={
                    "username": username,
                    "password": password,
                    "provider": "db",
                    "refresh": refresh,
                },
            )
            if response.status_code != 200:
                return {
                    "error": f"Failed to get access token: {response.status_code} - {response.text}"
                }
            data = response.json()
            access_token = data.get("access_token")
            if not access_token:
                return {"error": "No access token returned"}
            cache_access_token(access_token)
            analytics_ctx.access_token = access_token
            analytics_ctx.client.headers.update({"Authorization": f"Bearer {access_token}"})
            await fetch_csrf_token(ctx)
            return {
                "message": "Successfully authenticated with Analytics platform",
                "access_token": access_token,
            }
        except Exception as e:
            return {"error": f"Authentication error: {str(e)}"}
