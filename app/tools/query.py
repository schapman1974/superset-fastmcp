from typing import Any, Dict
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_query_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_query_stop(ctx: Any, client_id: str) -> Dict[str, Any]:
        """
        Stop a running query
        Makes a request to the /api/v1/query/stop endpoint to terminate a query.
        Args:
            client_id: Client ID of the query to stop
        Returns:
            A dictionary with confirmation of query termination
        """
        payload = {"client_id": client_id}
        return await make_platform_request(ctx, "post", "/api/v1/query/stop", data=payload)

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_query_list(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve a list of queries from the Analytics platform
        Makes a request to the /api/v1/query/ endpoint to fetch query history.
        Returns:
            A dictionary with query info including status, duration, and SQL
        """
        return await make_platform_request(ctx, "get", "/api/v1/query/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_query_get_by_id(ctx: Any, query_id: int) -> Dict[str, Any]:
        """
        Fetch details for a specific query
        Makes a request to the /api/v1/query/{id} endpoint.
        Args:
            query_id: ID of the query to retrieve
        Returns:
            A dictionary with complete query execution details
        """
        return await make_platform_request(ctx, "get", f"/api/v1/query/{query_id}")
