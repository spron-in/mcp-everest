import logging
import json
from typing import Optional, List, Any, Dict
import concurrent.futures
import atexit
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from dataclasses import asdict, is_dataclass

from .everest_client import EverestClient, EverestConfig

MCP_SERVER_NAME = "mcp-everest"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(MCP_SERVER_NAME)

load_dotenv()

deps = [
    "python-dotenv",
    "uvicorn",
    "requests",
]

# Check if read-only mode is enabled
readonly_mode = os.getenv("EVEREST_READONLY", "false").lower() == "true"

# Configure MCP server
mcp = FastMCP(
    MCP_SERVER_NAME,
    dependencies=deps,
)

if readonly_mode:
    logger.info("Running in read-only mode - only GET operations are allowed")
else:
    # Import and register write operations only in non-readonly mode
    from .write_operations import register_write_operations
    register_write_operations(mcp)

def to_json(obj: Any) -> str:
    if is_dataclass(obj):
        return json.dumps(asdict(obj), default=to_json)
    elif isinstance(obj, list):
        return [to_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: to_json(value) for key, value in obj.items()}
    return obj

def create_everest_client() -> EverestClient:
    """Create and return an Everest client instance."""
    config = EverestConfig(
        host=os.getenv("EVEREST_HOST", "http://localhost:8080"),
        api_key=os.getenv("EVEREST_API_KEY"),
        verify_ssl=os.getenv("EVEREST_VERIFY_SSL", "true").lower() == "true",
        timeout=int(os.getenv("EVEREST_TIMEOUT", "30"))
    )
    return EverestClient(config)

@mcp.tool()
def list_database_clusters(namespace: str) -> List[Dict[str, Any]]:
    """List available database clusters in the specified namespace."""
    logger.info(f"Listing database clusters in namespace '{namespace}'")
    client = create_everest_client()
    try:
        clusters = client.list_database_clusters(namespace)
        logger.info(f"Found {len(clusters)} database clusters")
        return clusters
    except Exception as e:
        logger.error(f"Failed to list database clusters: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def get_database_cluster(namespace: str, name: str) -> Dict[str, Any]:
    """Get details of a specific database cluster."""
    logger.info(f"Getting database cluster '{name}' in namespace '{namespace}'")
    client = create_everest_client()
    try:
        cluster = client.get_database_cluster(namespace, name)
        return cluster
    except Exception as e:
        logger.error(f"Failed to get database cluster: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def get_database_cluster_credentials(namespace: str, name: str) -> Dict[str, Any]:
    """Get credentials for a specific database cluster."""
    logger.info(f"Getting credentials for database cluster '{name}' in namespace '{namespace}'")
    client = create_everest_client()
    try:
        credentials = client.get_database_cluster_credentials(namespace, name)
        return credentials
    except Exception as e:
        logger.error(f"Failed to get database cluster credentials: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def get_database_cluster_components(namespace: str, name: str) -> Dict[str, Any]:
    """Get components of a specific database cluster."""
    logger.info(f"Getting components for database cluster '{name}' in namespace '{namespace}'")
    client = create_everest_client()
    try:
        components = client.get_database_cluster_components(namespace, name)
        return components
    except Exception as e:
        logger.error(f"Failed to get database cluster components: {str(e)}")
        return {"error": str(e)}



