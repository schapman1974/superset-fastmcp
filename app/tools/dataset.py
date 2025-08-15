from typing import Any, Dict, List, Optional
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_dataset_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_dataset_list(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve a list of datasets from the Analytics platform
        Makes a request to the /api/v1/dataset/ endpoint to fetch all datasets
        accessible to the current user. Results are paginated.
        Returns:
            A dictionary with dataset info including id, table_name, and database
        """
        return await make_platform_request(ctx, "get", "/api/v1/dataset/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_dataset_get_by_id(ctx: Any, dataset_id: int) -> Dict[str, Any]:
        """
        Fetch details for a specific dataset
        Makes a request to the /api/v1/dataset/{id} endpoint to retrieve detailed
        information about a specific dataset including columns and metrics.
        Args:
            dataset_id: ID of the dataset to retrieve
        Returns:
            A dictionary with complete dataset details
        """
        return await make_platform_request(ctx, "get", f"/api/v1/dataset/{dataset_id}")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_dataset_create(
        ctx: Any,
        table_name: str,
        database_id: int,
        schema: Optional[str] = None,
        owners: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new dataset in the Analytics platform
        Makes a request to the /api/v1/dataset/ POST endpoint to create a new dataset
        from an existing database table or view.
        Args:
            table_name: Name of the physical table in the database
            database_id: ID of the database where the table exists
            schema: Optional database schema name where the table is located
            owners: Optional list of user IDs who should own this dataset
        Returns:
            A dictionary with the created dataset information including its ID
        """
        payload = {
            "table_name": table_name,
            "database": database_id,
        }
        if schema:
            payload["schema"] = schema
        if owners:
            payload["owners"] = owners
        return await make_platform_request(ctx, "post", "/api/v1/dataset/", data=payload)
