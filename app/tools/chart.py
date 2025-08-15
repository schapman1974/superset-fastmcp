from typing import Any, Dict
import json
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_chart_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_chart_list(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve a list of charts from the Analytics platform
        Makes a request to the /api/v1/chart/ endpoint to fetch all charts
        accessible to the current user. Results are paginated.
        Returns:
            A dictionary with chart data including id, name, viz_type, and datasource info
        """
        return await make_platform_request(ctx, "get", "/api/v1/chart/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_chart_get_by_id(ctx: Any, chart_id: int) -> Dict[str, Any]:
        """
        Fetch details for a specific chart
        Makes a request to the /api/v1/chart/{id} endpoint to retrieve detailed
        information about a specific chart.
        Args:
            chart_id: ID of the chart to retrieve
        Returns:
            A dictionary with complete chart details including visualization configuration
        """
        return await make_platform_request(ctx, "get", f"/api/v1/chart/{chart_id}")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_chart_create(
        ctx: Any,
        chart_name: str,
        datasource_id: int,
        datasource_type: str,
        viz_type: str,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create a new chart in the Analytics platform
        Makes a request to the /api/v1/chart/ POST endpoint to create a new visualization.
        Args:
            chart_name: Name/title of the chart
            datasource_id: ID of the dataset or SQL table
            datasource_type: Type of datasource ('table' for datasets, 'query' for SQL)
            viz_type: Visualization type (e.g., 'bar', 'line', 'pie', 'big_number', etc.)
            params: Visualization parameters including metrics, groupby, time_range, etc.
        Returns:
            A dictionary with the created chart information including its ID
        """
        payload = {
            "slice_name": chart_name,
            "datasource_id": datasource_id,
            "datasource_type": datasource_type,
            "viz_type": viz_type,
            "params": json.dumps(params),
        }
        return await make_platform_request(ctx, "post", "/api/v1/chart/", data=payload)

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_chart_update(
        ctx: Any, chart_id: int, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing chart
        Makes a request to the /api/v1/chart/{id} PUT endpoint to update
        chart properties and visualization settings.
        Args:
            chart_id: ID of the chart to update
            data: Data to update, including name, description, viz_type, params, etc.
        Returns:
            A dictionary with the updated chart information
        """
        return await make_platform_request(ctx, "put", f"/api/v1/chart/{chart_id}", data=data)

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_chart_delete(ctx: Any, chart_id: int) -> Dict[str, Any]:
        """
        Delete a chart
        Makes a request to the /api/v1/chart/{id} DELETE endpoint.
        Args:
            chart_id: ID of the chart to delete
        Returns:
            A dictionary with deletion confirmation message
        """
        response = await make_platform_request(ctx, "delete", f"/api/v1/chart/{chart_id}")
        if not response.get("error"):
            return {"message": f"Chart {chart_id} deleted successfully"}
        return response
