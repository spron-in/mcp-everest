import logging
import json
from typing import Optional, List, Any, Dict
import concurrent.futures
import atexit
import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from dataclasses import dataclass, field, asdict, is_dataclass

from .everest_client import EverestClient, EverestConfig

@dataclass
class Column:
    database: str
    table: str
    name: str
    column_type: str
    default_kind: Optional[str]
    default_expression: Optional[str]
    comment: Optional[str]

@dataclass
class Table:
    database: str
    name: str
    engine: str
    create_table_query: str
    dependencies_database: str
    dependencies_table: str
    engine_full: str
    sorting_key: str
    primary_key: str
    total_rows: int
    total_bytes: int
    total_bytes_uncompressed: int
    parts: int
    active_parts: int
    total_marks: int
    comment: Optional[str] = None
    columns: List[Column] = field(default_factory=list)

MCP_SERVER_NAME = "mcp-everest"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(MCP_SERVER_NAME)

QUERY_EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=10)
atexit.register(lambda: QUERY_EXECUTOR.shutdown(wait=True))
SELECT_QUERY_TIMEOUT_SECS = 30

load_dotenv()

deps = [
    "python-dotenv",
    "uvicorn",
    "requests",
]

mcp = FastMCP(MCP_SERVER_NAME, dependencies=deps)

def result_to_table(query_columns, result) -> List[Table]:
    return [Table(**dict(zip(query_columns, row))) for row in result]

def result_to_column(query_columns, result) -> List[Column]:
    return [Column(**dict(zip(query_columns, row))) for row in result]

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
def list_databases():
    return {"error": "Not Implemented"}

@mcp.tool()
def list_tables(
    database: str, like: Optional[str] = None, not_like: Optional[str] = None
):
    return {"error": "Not Implemented"}

@mcp.tool()
def run_select_query(query: str):
    return {"error": "Not Implemented"}
def execute_query(query: str):
    return {"error": "Not Implemented"}
def create_clickhouse_client():
    return {"error": "Not Implemented"}
def get_readonly_setting(client):
    return {"error": "Not Implemented"}