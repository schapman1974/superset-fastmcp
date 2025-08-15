from mcp.server.fastmcp import FastMCP

from .conifg import Config
from .tools import (register_auth_tools,
                    register_dashboard_tools,
                    register_chart_tools,
                    register_database_tools,
                    register_dataset_tools,
                    register_sqllab_tools,
                    register_saved_query_tools,
                    register_query_tools,
                    register_activity_tools,
                    register_tag_tools,
                    register_explore_tools,
                    register_menu_tools,
                    register_config_tools,
                    register_advanced_data_type_tools)

MCP = FastMCP(
    name="superset fastmcp",
    instructions="Superset FastMCP is a tool for interacting with Apache Superset's API. Use the tools provided to access various functionalities such as analytics, user management, and data exploration.",
)

def setup_mcp(mcp):    
    # Register all tools
    register_auth_tools(mcp)
    register_dashboard_tools(mcp)
    register_chart_tools(mcp)
    register_database_tools(mcp)
    register_dataset_tools(mcp)
    register_sqllab_tools(mcp)
    register_saved_query_tools(mcp)
    register_query_tools(mcp)
    register_activity_tools(mcp)
    register_tag_tools(mcp)
    register_explore_tools(mcp)
    register_menu_tools(mcp)
    register_config_tools(mcp)
    register_advanced_data_type_tools(mcp)

class SupersetMCP:
    def __init__(self, host: str, port: int):
        """ Initialize the SupersetMCP with the host and port."""
        self.host = host
        self.port = port
    
    def run(self):
        """ Run the FastMCP server."""
        MCP.run(host=self.host, port=self.port)
        setup_mcp(MCP)

def main():
    config = Config()
    superset_mcp = SupersetMCP(host=config.host, port=config.port)
    superset_mcp.run()

if __name__ == "__main__":
    main()



