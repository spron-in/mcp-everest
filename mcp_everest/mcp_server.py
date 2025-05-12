import logging
from typing import List, Dict, Any

from mcp.server.fastmcp import FastMCP

from mcp_everest.mcp_env import config
from mcp_everest.everest_client import EverestClient, EverestConfig

MCP_SERVER_NAME = "mcp-everest"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(MCP_SERVER_NAME)

deps = [
    "python-dotenv",
    "uvicorn",
    "requests",
]

# Configure MCP server
mcp = FastMCP(
    MCP_SERVER_NAME,
    dependencies=deps,
)

# Initialize Everest client using config
everest_config = EverestConfig(
    host=config.host,
    api_key=config.api_key,
    verify_ssl=config.verify_ssl,
    timeout=config.timeout
)
everest_client = EverestClient(everest_config)

@mcp.tool()
def list_database_clusters(namespace: str) -> List[Dict[str, Any]]:
    """List available database clusters in the specified namespace."""
    logger.info(f"Listing database clusters in namespace '{namespace}'")
    try:
        clusters = everest_client.list_database_clusters(namespace)
        logger.info(f"Found {len(clusters)} database clusters")
        return clusters
    except Exception as e:
        logger.error(f"Failed to list database clusters: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def get_database_cluster(namespace: str, name: str) -> Dict[str, Any]:
    """Get details of a specific database cluster."""
    logger.info(f"Getting database cluster '{name}' in namespace '{namespace}'")
    try:
        cluster = everest_client.get_database_cluster(namespace, name)
        return cluster
    except Exception as e:
        logger.error(f"Failed to get database cluster: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def get_database_cluster_credentials(namespace: str, name: str) -> Dict[str, Any]:
    """Get credentials for a specific database cluster."""
    logger.info(f"Getting credentials for database cluster '{name}' in namespace '{namespace}'")
    try:
        credentials = everest_client.get_database_cluster_credentials(namespace, name)
        return credentials
    except Exception as e:
        logger.error(f"Failed to get database cluster credentials: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def get_database_cluster_components(namespace: str, name: str) -> Dict[str, Any]:
    """Get components of a specific database cluster."""
    logger.info(f"Getting components for database cluster '{name}' in namespace '{namespace}'")
    try:
        components = everest_client.get_database_cluster_components(namespace, name)
        return components
    except Exception as e:
        logger.error(f"Failed to get database cluster components: {str(e)}")
        return {"error": str(e)}

@mcp.tool()
def create_database_cluster(
    namespace: str,
    name: str,
    engine_type: str,
    storage_size: str = "10Gi",
    replicas: int = 1,
    cpu: int = 1,
    memory: str = "1Gi",
    allow_unsafe: bool = True,
    proxy_replicas: int = 1
) -> Dict[str, Any]:
    """Create a new database cluster in the specified namespace.

    Args:
        namespace: The namespace to create the cluster in
        name: Name of the database cluster
        engine_type: Type of database engine (e.g. 'pxc')
        storage_size: Size of storage in GB
        replicas: Number of database replicas
        cpu: CPU cores per replica
        memory: Memory in GB per replica
        allow_unsafe: Allow unsafe configurations
        proxy_replicas: Number of proxy replicas
    """
    logger.info(f"Creating database cluster in namespace '{namespace}'")
    try:
        cluster = everest_client.create_database_cluster(
            namespace=namespace,
            engine_type=engine_type,
            storage_size=storage_size,
            replicas=replicas,
            cpu=cpu,
            memory=memory,
            allow_unsafe=allow_unsafe,
            proxy_replicas=proxy_replicas
        )
        return cluster
    except Exception as e:
        logger.error(f"Failed to create database cluster: {str(e)}")
        return {"error": str(e)}