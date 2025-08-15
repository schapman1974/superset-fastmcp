from typing import Any, Dict, Optional
from .core import AnalyticsContext, requires_authentication, handle_platform_errors, make_platform_request, fetch_csrf_token

def register_sqllab_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_sqllab_execute_query(
        ctx: Any, database_id: int, sql: str
    ) -> Dict[str, Any]:
        """
        Execute a SQL query in the Analytics platform's SQL Lab
        Makes a request to the /api/v1/sqllab/execute/ endpoint to run a SQL query.
        Args:
            database_id: ID of the database to query
            sql: SQL query to execute
        Returns:
            A dictionary with query results or execution status for async queries
        """
        analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
        if not analytics_ctx.csrf_token:
            await fetch_csrf_token(ctx)
        payload = {
            "database_id": database_id,
            "sql": sql,
            "schema": "",
            "tab": "MCP Query",
            "runAsync": False,
            "select_as_cta": False,
        }
        return await make_platform_request(ctx, "post", "/api/v1/sqllab/execute/", data=payload)

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_sqllab_get_saved_queries(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve a list of saved queries from SQL Lab
        Makes a request to the /api/v1/saved_query/ endpoint to fetch all saved queries.
        Returns:
            A dictionary with saved query info including id, label, and database
        """
        return await make_platform_request(ctx, "get", "/api/v1/saved_query/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_sqllab_format_sql(ctx: Any, sql: str) -> Dict[str, Any]:
        """
        Format a SQL query for better readability
        Makes a request to the /api/v1/sqllab/format_sql endpoint.
        Args:
            sql: SQL query to format
        Returns:
            A dictionary with the formatted SQL
        """
        payload = {"sql": sql}
        return await make_platform_request(
            ctx, "post", "/api/v1/sqllab/format_sql", data=payload
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_sqllab_get_results(ctx: Any, key: str) -> Dict[str, Any]:
        """
        Retrieve results of a previously executed SQL query
        Makes a request to the /api/v1/sqllab/results/ endpoint to fetch results
        for an asynchronous query using its result key.
        Args:
            key: Result key to retrieve
        Returns:
            A dictionary with query results including column info and data rows
        """
        return await make_platform_request(
            ctx, "get", f"/api/v1/sqllab/results/", params={"key": key}
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_sqllab_estimate_query_cost(
        ctx: Any, database_id: int, sql: str, schema: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Estimate the cost of executing a SQL query
        Makes a request to the /api/v1/sqllab/estimate endpoint.
        Args:
            database_id: ID of the database
            sql: SQL query to estimate
            schema: Optional schema name
        Returns:
            A dictionary with estimated query cost metrics
        """
        payload = {
            "database_id": database_id,
            "sql": sql,
        }
        if schema:
            payload["schema"] = schema
        return await make_platform_request(ctx, "post", "/api/v1/sqllab/estimate", data=payload)

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_sqllab_export_query_results(
        ctx: Any, client_id: str
    ) -> Dict[str, Any]:
        """
        Export SQL query results to CSV
        Makes a request to the /api/v1/sqllab/export/{client_id} endpoint.
        Args:
            client_id: Client ID of the query
        Returns:
            A dictionary with the exported data or error details
        """
        analytics_ctx: AnalyticsContext = ctx.request_context.lifespan_context
        try:
            response = await analytics_ctx.client.get(f"/api/v1/sqllab/export/{client_id}")
            if response.status_code != 200:
                return {
                    "error": f"Failed to export query results: {response.status_code} - {response.text}"
                }
            return {"message": "Query results exported successfully", "data": response.text}
        except Exception as e:
            return {"error": f"Error exporting query results: {str(e)}"}

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_sqllab_get_bootstrap_data(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve bootstrap data for SQL Lab
        Makes a request to the /api/v1/sqllab/ endpoint to fetch configuration data.
        Returns:
            A dictionary with SQL Lab configuration including allowed databases and settings
        """
        return await make_platform_request(ctx, "get", "/api/v1/sqllab/")
