from typing import Any, Dict
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_saved_query_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_saved_query_get_by_id(ctx: Any, query_id: int) -> Dict[str, Any]:
        """
        Fetch details for a specific saved query
        Makes a request to the /api/v1/saved_query/{id} endpoint.
        Args:
            query_id: ID of the saved query to retrieve
        Returns:
            A dictionary with saved query details including SQL text and database
        """
        return await make_platform_request(ctx, "get", f"/api/v1/saved_query/{query_id}")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_saved_query_create(
        ctx: Any, query_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create a new saved query
        Makes a request to the /api/v1/saved_query/ POST endpoint to save a SQL query.
        Args:
            query_data: Dictionary with query info including db_id, schema, sql, label, and description
        Returns:
            A dictionary with the created saved query information including its ID
        """
        return await make_platform_request(ctx, "post", "/api/v1/saved_query/", data=query_data)
