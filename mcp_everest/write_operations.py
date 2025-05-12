
from typing import Dict, Any
import logging
from .mcp_server import create_everest_client

logger = logging.getLogger(__name__)

def register_write_operations(mcp):
    """Register write operations with the MCP server."""
    
    @mcp.tool(
        spec_params={
            "allowUnsafeConfiguration": {"type": "boolean", "description": "Allow unsafe configurations (deprecated)"},
            "backup": {
                "type": "object",
                "properties": {
                    "dataSource": {
                        "type": "object",
                        "description": "Data source for bootstrapping a new cluster"
                    }
                }
            },
            "engine": {
                "type": "object",
                "description": "Database engine specification",
                "required": True
            },
            "monitoring": {
                "type": "object",
                "properties": {
                    "monitoringConfigName": {"type": "string", "description": "Name of monitoringConfig CR"},
                    "resources": {"type": "object", "description": "Resource limitations for monitoring"}
                }
            },
            "paused": {"type": "boolean", "description": "Flag to stop the cluster"},
            "proxy": {
                "type": "object",
                "properties": {
                    "config": {"type": "string", "description": "Proxy configuration"},
                    "expose": {
                        "type": "object",
                        "properties": {
                            "replicas": {"type": "integer", "minimum": 1, "description": "Number of proxy replicas"},
                            "resources": {"type": "object", "description": "Resource limits for proxy replicas"}
                        }
                    },
                    "type": {"type": "string", "description": "Proxy type"}
                }
            },
            "sharding": {
                "type": "object",
                "properties": {
                    "configServer": {
                        "type": "object",
                        "required": True,
                        "properties": {
                            "enabled": {"type": "boolean", "required": True, "description": "Enable sharding"},
                            "shards": {"type": "integer", "minimum": 1, "required": True, "description": "Number of shards"}
                        }
                    }
                }
            }
        }
    )
    def update_database_cluster(namespace: str, name: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Update a database cluster's specification with the provided configuration parameters."""
        logger.info(f"Updating database cluster '{name}' in namespace '{namespace}'")
        client = create_everest_client()
        try:
            result = client.update_database_cluster(namespace, name, spec)
            return result
        except Exception as e:
            logger.error(f"Failed to update database cluster: {str(e)}")
            return {"error": str(e)}

    @mcp.tool()
    def delete_database_cluster(namespace: str, name: str) -> Dict[str, Any]:
        """Delete a database cluster."""
        logger.info(f"Deleting database cluster '{name}' in namespace '{namespace}'")
        client = create_everest_client()
        try:
            result = client.delete_database_cluster(namespace, name)
            return result
        except Exception as e:
            logger.error(f"Failed to delete database cluster: {str(e)}")
            return {"error": str(e)}
