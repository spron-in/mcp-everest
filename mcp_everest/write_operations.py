
from typing import Dict, Any
import logging
from .utils import create_everest_client

logger = logging.getLogger(__name__)

def register_write_operations(mcp):
    """Register write operations with the MCP server."""
    
    @mcp.tool()
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
