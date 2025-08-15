from typing import Any, Dict
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_advanced_data_type_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_advanced_data_type_convert(
        ctx: Any, type_name: str, value: Any
    ) -> Dict[str, Any]:
        """
        Convert a value to an advanced data type
        Makes a request to the /api/v1/advanced_data_type/convert endpoint.
        Args:
            type_name: Name of the advanced data type
            value: Value to convert
        Returns:
            A dictionary with the converted value
        """
        params = {
            "type_name": type_name,
            "value": value,
        }
        return await make_platform_request(
            ctx, "get", "/api/v1/advanced_data_type/convert", params=params
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_advanced_data_type_list(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve a list of available advanced data types
        Makes a request to the /api/v1/advanced_data_type/types endpoint.
        Returns:
            A dictionary with available advanced data types and their configurations
        """
        return await make_platform_request(ctx, "get", "/api/v1/advanced_data_type/types")
