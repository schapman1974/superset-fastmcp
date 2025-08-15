from typing import Any, Dict
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_dashboard_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_dashboard_list(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve a list of dashboards from the Analytics platform
        Makes a request to the /api/v1/dashboard/ endpoint to fetch all dashboards
        accessible to the current user. Results are paginated.
        Returns:
            A dictionary with dashboard data including id, title, url, and metadata
        """
        return await make_platform_request(ctx, "get", "/api/v1/dashboard/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_dashboard_get_by_id(
        ctx: Any, dashboard_id: int
    ) -> Dict[str, Any]:
        """
        Fetch details for a specific dashboard
        Makes a request to the /api/v1/dashboard/{id} endpoint to retrieve detailed
        information about a specific dashboard.
        Args:
            dashboard_id: ID of the dashboard to retrieve
        Returns:
            A dictionary with complete dashboard details including components and layout
        """
        return await make_platform_request(ctx, "get", f"/api/v1/dashboard/{dashboard_id}")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_dashboard_create(
        ctx: Any, dashboard_title: str, json_metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create a new dashboard in the Analytics platform
        Makes a request to the /api/v1/dashboard/ POST endpoint.
        Args:
            dashboard_title: Title of the dashboard
            json_metadata: Optional JSON metadata for dashboard configuration
        Returns:
            A dictionary with the created dashboard information including its ID
        """
        payload = {"dashboard_title": dashboard_title}
        if json_metadata:
            payload["json_metadata"] = json_metadata
        return await make_platform_request(ctx, "post", "/api/v1/dashboard/", data=payload)

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_dashboard_update(
        ctx: Any, dashboard_id: int, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing dashboard
        Makes a request to the /api/v1/dashboard/{id} PUT endpoint to update
        dashboard properties.
        Args:
            dashboard_id: ID of the dashboard to update
            data: Data to update, including dashboard_title, slug, owners, position, and metadata
        Returns:
            A dictionary with the updated dashboard information
        """
        return await make_platform_request(
            ctx, "put", f"/api/v1/dashboard/{dashboard_id}", data=data
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_dashboard_delete(ctx: Any, dashboard_id: int) -> Dict[str, Any]:
        """
        Delete a dashboard
        Makes a request to the /api/v1/dashboard/{id} DELETE endpoint.
        Args:
            dashboard_id: ID of the dashboard to delete
        Returns:
            A dictionary with deletion confirmation message
        """
        response = await make_platform_request(
            ctx, "delete", f"/api/v1/dashboard/{dashboard_id}"
        )
        if not response.get("error"):
            return {"message": f"Dashboard {dashboard_id} deleted successfully"}
        return response
