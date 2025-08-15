from typing import Any, Dict
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_menu_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_menu_get(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve the Analytics platform menu data
        Makes a request to the /api/v1/menu/ endpoint to fetch the navigation
        menu structure based on user permissions.
        Returns:
            A dictionary with menu items and their configurations
        """
        return await make_platform_request(ctx, "get", "/api/v1/menu/")
