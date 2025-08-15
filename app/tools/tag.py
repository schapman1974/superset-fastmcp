from typing import Any, Dict
from .core import requires_authentication, handle_platform_errors, make_platform_request

def register_tag_tools(mcp):
    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_tag_list(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve a list of tags from the Analytics platform
        Makes a request to the /api/v1/tag/ endpoint.
        Returns:
            A dictionary with tag info including id and name
        """
        return await make_platform_request(ctx, "get", "/api/v1/tag/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_tag_create(ctx: Any, name: str) -> Dict[str, Any]:
        """
        Create a new tag in the Analytics platform
        Makes a request to the /api/v1/tag/ POST endpoint.
        Args:
            name: Name for the tag
        Returns:
            A dictionary with the created tag information
        """
        payload = {"name": name}
        return await make_platform_request(ctx, "post", "/api/v1/tag/", data=payload)

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_tag_get_by_id(ctx: Any, tag_id: int) -> Dict[str, Any]:
        """
        Fetch details for a specific tag
        Makes a request to the /api/v1/tag/{id} endpoint.
        Args:
            tag_id: ID of the tag to retrieve
        Returns:
            A dictionary with tag details
        """
        return await make_platform_request(ctx, "get", f"/api/v1/tag/{tag_id}")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_tag_objects(ctx: Any) -> Dict[str, Any]:
        """
        Retrieve objects associated with tags
        Makes a request to the /api/v1/tag/get_objects/ endpoint.
        Returns:
            A dictionary with tagged objects grouped by tag
        """
        return await make_platform_request(ctx, "get", "/api/v1/tag/get_objects/")

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_tag_delete(ctx: Any, tag_id: int) -> Dict[str, Any]:
        """
        Delete a tag
        Makes a request to the /api/v1/tag/{id} DELETE endpoint.
        Args:
            tag_id: ID of the tag to delete
        Returns:
            A dictionary with deletion confirmation message
        """
        response = await make_platform_request(ctx, "delete", f"/api/v1/tag/{tag_id}")
        if not response.get("error"):
            return {"message": f"Tag {tag_id} deleted successfully"}
        return response

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_tag_object_add(
        ctx: Any, object_type: str, object_id: int, tag_name: str
    ) -> Dict[str, Any]:
        """
        Add a tag to an object
        Makes a request to tag an object with a specific tag.
        Args:
            object_type: Type of the object ('chart', 'dashboard', etc.)
            object_id: ID of the object to tag
            tag_name: Name of the tag to apply
        Returns:
            A dictionary with the tagging confirmation
        """
        payload = {
            "object_type": object_type,
            "object_id": object_id,
            "tag_name": tag_name,
        }
        return await make_platform_request(
            ctx, "post", "/api/v1/tag/tagged_objects", data=payload
        )

    @mcp.tool()
    @requires_authentication
    @handle_platform_errors
    async def analytics_tag_object_remove(
        ctx: Any, object_type: str, object_id: int, tag_name: str
    ) -> Dict[str, Any]:
        """
        Remove a tag from an object
        Makes a request to remove a tag association from an object.
        Args:
            object_type: Type of the object ('chart', 'dashboard', etc.)
            object_id: ID of the object to untag
            tag_name: Name of the tag to remove
        Returns:
            A dictionary with the untagging confirmation message
        """
        response = await make_platform_request(
            ctx,
            "delete",
            f"/api/v1/tag/{object_type}/{object_id}",
            params={"tag_name": tag_name},
        )
        if not response.get("error"):
            return {
                "message": f"Tag '{tag_name}' removed from {object_type} {object_id} successfully"
            }
        return response
