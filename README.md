
The Analytics MCP (Model Control Protocol) Server is a Python-based application that provides programmatic access to an Analytics platform's API, enabling AI assistants or automated systems to interact with dashboards, charts, databases, datasets, SQL queries, user activities, tags, and more. It uses the `FastMCP` framework to manage tools and integrate with the platform's API.

## Features

+ **Authentication**: Manage user authentication, token validation, and token refreshing.
+ **Dashboards**: List, retrieve, create, update, and delete dashboards.
+ **Charts**: Manage chart creation, updates, and deletions with support for various visualization types.
+ **Databases**: Handle database connections, including creation, testing, and schema/table retrieval.
+ **Datasets**: Create and manage datasets linked to database tables.
+ **SQL Lab**: Execute SQL queries, format queries, estimate query costs, and export results.
+ **Saved Queries**: Retrieve and create saved SQL queries.
+ **Query Management**: Stop running queries and retrieve query history.
+ **User Activity**: Access recent user activities and user role information.
+ **Tags**: Create, manage, and associate tags with platform objects.
+ **Exploration**: Create and retrieve form data and permalinks for chart exploration.
+ **Menu and Configuration**: Retrieve navigation menu data and platform API URL.
+ **Advanced Data Types**: Convert values to advanced data types and list available types.

## Installation

1. **Clone the Repository**:
   |||bash
   git clone <repository-url>
   cd analytics_mcp
   |||

2. **Install Dependencies**:
   Ensure you have Python 3.8+ installed. Create a virtual environment and install the required packages:
   |||bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install uvicorn python-dotenv httpx
   |||

3. **Set Up Environment Variables**:
   Create a `.env` file in the `analytics_mcp` directory with the following:
   |||env
   ANALYTICS_API_URL=http://localhost:8080
   ANALYTICS_USER=your_username
   ANALYTICS_PASS=your_password
   |||
   - `ANALYTICS_API_URL`: The base URL of the Analytics platform API (default: `http://localhost:8080`).
   - `ANALYTICS_USER`: Your Analytics platform username.
   - `ANALYTICS_PASS`: Your Analytics platform password.

## Usage

1. **Run the Server**:
   Start the MCP server using the `main.py` script:
   |||bash
   python -m analytics_mcp.main
   |||
   This starts a Uvicorn server on `0.0.0.0:8000` by default.

2. **Use in a Script**:
   You can integrate the MCP server into another Python script:
   |||python
   from analytics_mcp import setup_mcp

   mcp = setup_mcp()
   # Use mcp to interact with the Analytics platform
   |||

3. **Example API Calls**:
   Use the registered tools to interact with the Analytics platform. For example, to authenticate:
   |||python
   import asyncio
   from analytics_mcp import setup_mcp

   async def main():
       mcp = setup_mcp()
       ctx = mcp.create_context()  # Assuming FastMCP provides a context creation method
       result = await mcp.tools["analytics_auth_authenticate_user"](ctx, username="user", password="pass")
       print(result)

   asyncio.run(main())
   |||

## Configuration

+ **Environment Variables**: Ensure the `.env` file is correctly configured with the Analytics platform's API URL and credentials.
+ **Port and Host**: Modify the `uvicorn.run` call in `main.py` to change the host or port if needed.
+ **Dependencies**: The server requires `uvicorn`, `python-dotenv`, and `httpx`. Install additional dependencies as needed for your environment.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Notes

+ The server assumes the Analytics platform API follows a structure similar to common BI platforms. If the API endpoints differ, update the endpoint paths in the respective tool files.
+ The `FastMCP` framework is used for tool registration and server management. Ensure you have access to the `mcp.server.fastmcp` module.
+ For production use, secure the `.env` file and consider using a reverse proxy (e.g., Nginx) for the Uvicorn server.
