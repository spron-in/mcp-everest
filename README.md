
# Unofficial Percona Everest MCP Server

An unofficial MCP (Modular Copilot Protocol) server implementation for Percona Everest. This server enables AI-powered interaction with Percona Everest database clusters through a standardized protocol.

## Available Tools

The MCP server provides the following tools for interacting with Percona Everest:

- `list_database_clusters(namespace)`: Lists all available database clusters in the specified namespace
- `get_database_cluster(namespace, name)`: Retrieves detailed information about a specific database cluster
- `get_database_cluster_credentials(namespace, name)`: Fetches credentials for a specific database cluster
- `get_database_cluster_components(namespace, name)`: Gets components information for a specific database cluster

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/spron-in/mcp-everest
cd mcp-everest
```

2. Set up environment variables:
```bash
# Required
export EVEREST_API_KEY="your-api-key"

# Optional with defaults
export EVEREST_HOST="http://localhost:8080"  # Everest API base URL
export EVEREST_VERIFY_SSL="true"             # SSL verification
export EVEREST_TIMEOUT="30"                  # Request timeout in seconds
export EVEREST_READONLY="false"              # Read-only mode
```

3. Run the server:
```bash
uv run --with mcp-everest mcp-everest
```

## Testing with MCP Client

To test the server with the MCP development client:

```bash
python mcp_client.py
```

This will start an interactive session where you can query the Everest database clusters through natural language.

Example queries:
- "List all database clusters in the 'default' namespace"
- "Get details for the database cluster named 'my-cluster' in namespace 'production'"
- "Show me the credentials for cluster 'test-db' in namespace 'staging'"

## Future Development

### Planned Improvements

1. **Official Integration**
   - Work towards making this an official MCP server for Percona Everest
   - Submit for inclusion in popular MCP server collections

2. **API Coverage Expansion**
   - Implement more GET endpoints from the Everest API
   - Add support for POST/PUT/DELETE operations
   - Include monitoring and metrics endpoints

3. **Cross-Integration**
   - Integrate with other database MCP servers (MongoDB, PostgreSQL, etc.)
   - Enable cross-database operations and management
   - Implement unified monitoring across different database platforms

### Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
