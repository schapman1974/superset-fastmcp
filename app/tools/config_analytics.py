from typing import Any, Dict
from .core import AnalyticsContext, handle_platform_errors, make_platform_request

def register_config_tools(mcp):
    @mcp.tool()
    @handle_platform_errors
    async def analytics_config_get_api_url(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve the API URL of the Analytics platform
        Returns the configured API URL that this MCP server is connecting to.
        Returns:
            A dictionary with the Analytics platform API URL
        """
        analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
        return {
            "api_url": analytics_ctx.api_url,
            "message": f"Connected to Analytics platform at: {analytics_ctx.api_url}",
        }
