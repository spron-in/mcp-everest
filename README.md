
# Unofficial Percona Everest MCP Server

An unofficial MCP (Model Context Protocol) server implementation for [Percona Everest](https://docs.percona.com/everest/index.html) - an open-source cloud native database platform. This server enables AI-powered interaction with Percona Everest database clusters through a standardized protocol.

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
uv venv
source .venv/bin/activate
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

Read [Percona Everest documentation](https://docs.percona.com/everest/API.html) to learn more about API. I sent a [pull request](https://github.com/percona/everest-doc/pull/255) that explains how to get the API (JWT) key, hope it is going to be accepted soon.

3. Run the server:
```bash
uv run --with mcp-everest mcp-everest
```

## Testing and playing

### Testing with mcp tool

To test the server with the MCP development client:

```bash
mcp dev mcp_server.py
```

This requires Node to be installed. It will start a nodejs MCP server that you can open in your browser and play with.

### Example mcp_client.py

There is also a client that can be used to interact with the MCP server:

```bash
python mcp_client.py
```

This will output the tools available in the MCP server. Script can be easily altered.

## Future Development

### Planned Improvements

1. **Official Integration**
   - Work towards making this an official MCP server for Percona Everest
   - Submit for inclusion in popular MCP server collections

2. **API Coverage Expansion**
   - Implement more GET endpoints from the Everest API
   - Add support for POST/PUT/DELETE operations (but have read-only mode available)
   - Include resources and prompts into MCP

3. **Cross-Integration**
   - Integrate with other database MCP servers (MongoDB, PostgreSQL, etc.)
   - Enable cross-database operations and management
   - Implement unified monitoring across different database platforms

### Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
