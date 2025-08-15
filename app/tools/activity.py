from typing import Any, Dict
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_activity_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_activity_get_recent(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve recent activity data for the current user
        Makes a request to the /api/v1/log/recent_activity/ endpoint.
        Returns:
            A dictionary with recent user activities including viewed charts and dashboards
        """
        return await make_platform_request(ctx, "get", "/api/v1/log/recent_activity/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_user_get_current(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve information about the currently authenticated user
        Makes a request to the /api/v1/me/ endpoint.
        Returns:
            A dictionary with user profile data
        """
        return await make_platform_request(ctx, "get", "/api/v1/me/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_user_get_roles(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve roles for the current user
        Makes a request to the /api/v1/me/roles/ endpoint.
        Returns:
            A dictionary with user role information
        """
        return await make_platform_request(ctx, "get", "/api/v1/me/roles/")
