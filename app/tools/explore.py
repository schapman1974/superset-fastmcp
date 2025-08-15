from typing import Any, Dict
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_explore_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_explore_form_data_create(
        ctx: Any, form_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create form data for chart exploration
        Makes a request to the /api/v1/explore/form_data POST endpoint.
        Args:
            form_data: Chart configuration including datasource, metrics, and visualization settings
        Returns:
            A dictionary with a key to retrieve the form data
        """
        return await make_platform_request(
            ctx, "post", "/api/v1/explore/form_data", data=form_data
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_explore_form_data_get(ctx: Any, key: str) -> Dict[str, Any]:
        """
        Retrieve form data for chart exploration
        Makes a request to the /api/v1/explore/form_data/{key} endpoint.
        Args:
            key: Key of the form data to retrieve
        Returns:
            A dictionary with the stored chart configuration
        """
        return await make_platform_request(ctx, "get", f"/api/v1/explore/form_data/{key}")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_explore_permalink_create(
        ctx: Any, state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a permalink for chart exploration
        Makes a request to the /api/v1/explore/permalink POST endpoint.
        Args:
            state: State data for the permalink including form_data
        Returns:
            A dictionary with a key to access the permalink
        """
        return await make_platform_request(ctx, "post", "/api/v1/explore/permalink", data=state)

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_explore_permalink_get(ctx: Any, key: str) -> Dict[str, Any]:
        """
        Retrieve a permalink for chart exploration
        Makes a request to the /api/v1/explore/permalink/{key} endpoint.
        Args:
            key: Key of the permalink to retrieve
        Returns:
            A dictionary with the stored exploration state
        """
        return await make_platform_request(ctx, "get", f"/api/v1/explore/permalink/{key}")
