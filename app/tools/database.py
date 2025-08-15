from typing import Any, Dict
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_database_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_list(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve a list of databases from the Analytics platform
        Makes a request to the /api/v1/database/ endpoint to fetch all database
        connections accessible to the current user. Results are paginated.
        Returns:
            A dictionary with database connection info including id, name, and configuration
        """
        return await make_platform_request(ctx, "get", "/api/v1/database/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_get_by_id(ctx: Any, database_id: int) -> Dict[str, Any]:
        """
        Fetch details for a specific database
        Makes a request to the /api/v1/database/{id} endpoint.
        Args:
            database_id: ID of the database to retrieve
        Returns:
            A dictionary with complete database configuration details
        """
        return await make_platform_request(ctx, "get", f"/api/v1/database/{database_id}")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_create(
        ctx: Any,
        engine: str,
        config_method: str,
        database_name: str,
        connection_uri: str,
    ) -> Dict[str, Any]:
        """
        Create a new database connection in the Analytics platform
        Makes a POST request to /api/v1/database/ to create a new database connection.
        Args:
            engine: Database engine (e.g., 'postgresql', 'mysql', etc.)
            config_method: Configuration method (typically 'sqlalchemy_form')
            database_name: Name for the database connection
            connection_uri: SQLAlchemy URI for the connection
        Returns:
            A dictionary with the created database connection information including its ID
        """
        payload = {
            "engine": engine,
            "configuration_method": config_method,
            "database_name": database_name,
            "sqlalchemy_uri": connection_uri,
            "allow_dml": True,
            "allow_cvas": True,
            "allow_ctas": True,
            "expose_in_sqllab": True,
        }
        return await make_platform_request(ctx, "post", "/api/v1/database/", data=payload)

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_get_tables(
        ctx: Any, database_id: int
    ) -> Dict[str, Any]:
        """
        Retrieve a list of tables for a given database
        Makes a request to the /api/v1/database/{id}/tables/ endpoint.
        Args:
            database_id: ID of the database
        Returns:
            A dictionary with a list of tables including schema and table name details
        """
        return await make_platform_request(ctx, "get", f"/api/v1/database/{database_id}/tables/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_schemas(ctx: Any, database_id: int) -> Dict[str, Any]:
        """
        Retrieve schemas for a specific database
        Makes a request to the /api/v1/database/{id}/schemas/ endpoint.
        Args:
            database_id: ID of the database
        Returns:
            A dictionary with a list of schema names
        """
        return await make_platform_request(
            ctx, "get", f"/api/v1/database/{database_id}/schemas/"
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_test_connection(
        ctx: Any, database_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Test a database connection
        Makes a request to the /api/v1/database/test_connection endpoint.
        Args:
            database_data: Database connection details including connection_uri and other parameters
        Returns:
            A dictionary with connection test results
        """
        return await make_platform_request(
            ctx, "post", "/api/v1/database/test_connection", data=database_data
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_update(
        ctx: Any, database_id: int, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing database connection
        Makes a request to the /api/v1/database/{id} PUT endpoint.
        Args:
            database_id: ID of the database to update
            data: Data to update, including database_name, connection_uri, password, and extra configs
        Returns:
            A dictionary with the updated database information
        """
        return await make_platform_request(
            ctx, "put", f"/api/v1/database/{database_id}", data=data
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_delete(ctx: Any, database_id: int) -> Dict[str, Any]:
        """
        Delete a database connection
        Makes a request to the /api/v1/database/{id} DELETE endpoint.
        Args:
            database_id: ID of the database to delete
        Returns:
            A dictionary with deletion confirmation message
        """
        response = await make_platform_request(ctx, "delete", f"/api/v1/database/{database_id}")
        if not response.get("error"):
            return {"message": f"Database {database_id} deleted successfully"}
        return response

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_get_catalogs(
        ctx: Any, database_id: int
    ) -> Dict[str, Any]:
        """
        Retrieve all catalogs from a database
        Makes a request to the /api/v1/database/{id}/catalogs/ endpoint.
        Args:
            database_id: ID of the database
        Returns:
            A dictionary with a list of catalog names for databases that support catalogs
        """
        return await make_platform_request(
            ctx, "get", f"/api/v1/database/{database_id}/catalogs/"
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_get_connection(
        ctx: Any, database_id: int
    ) -> Dict[str, Any]:
        """
        Retrieve database connection information
        Makes a request to the /api/v1/database/{id}/connection endpoint.
        Args:
            database_id: ID of the database
        Returns:
            A dictionary with detailed connection information
        """
        return await make_platform_request(
            ctx, "get", f"/api/v1/database/{database_id}/connection"
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_get_function_names(
        ctx: Any, database_id: int
    ) -> Dict[str, Any]:
        """
        Retrieve function names supported by a database
        Makes a request to the /api/v1/database/{id}/function_names/ endpoint.
        Args:
            database_id: ID of the database
        Returns:
            A dictionary with a list of supported function names
        """
        return await make_platform_request(
            ctx, "get", f"/api/v1/database/{database_id}/function_names/"
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_get_related_objects(
        ctx: Any, database_id: int
    ) -> Dict[str, Any]:
        """
        Retrieve charts and dashboards associated with a database
        Makes a request to the /api/v1/database/{id}/related_objects/ endpoint.
        Args:
            database_id: ID of the database
        Returns:
            A dictionary with counts and lists of related charts and dashboards
        """
        return await make_platform_request(
            ctx, "get", f"/api/v1/database/{database_id}/related_objects/"
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_validate_sql(
        ctx: Any, database_id: int, sql: str
    ) -> Dict[str, Any]:
        """
        Validate arbitrary SQL against a database
        Makes a request to the /api/v1/database/{id}/validate_sql/ endpoint.
        Args:
            database_id: ID of the database
            sql: SQL query to validate
        Returns:
            A dictionary with validation results
        """
        payload = {"sql": sql}
        return await make_platform_request(
            ctx, "post", f"/api/v1/database/{database_id}/validate_sql/", data=payload
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_database_validate_parameters(
        ctx: Any, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate database connection parameters
        Makes a request to the /api/v1/database/validate_parameters/ endpoint.
        Args:
            parameters: Connection parameters to validate
        Returns:
            A dictionary with validation results
        """
        return await make_platform_request(
            ctx, "post", "/api/v1/database/validate_parameters/", data=parameters
        )
