"""Client library for Percona Everest API."""

import logging
import requests
from dataclasses import dataclass
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

@dataclass
class EverestConfig:
    """Configuration for Everest API connection."""
    host: str
    api_key: Optional[str] = None
    verify_ssl: bool = True
    timeout: int = 30
    
    @property
    def base_url(self) -> str:
        """Get the base URL for API calls."""
        return f"{self.host}/v1"

class EverestClient:
    """Client for interacting with Percona Everest API."""
    
    def __init__(self, config: EverestConfig):
        self.config = config
        self.session = requests.Session()
        if self.config.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.config.api_key}"
            })
    
    def _make_request(
        self, 
        method: str, 
        path: str, 
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make HTTP request to Everest API."""
        url = f"{self.config.base_url}{path}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                verify=self.config.verify_ssl,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise

    def list_database_clusters(self, namespace: str) -> List[Dict[str, Any]]:
        """List all database clusters in a namespace."""
        return self._make_request("GET", f"/namespaces/{namespace}/database-clusters")

    def get_database_cluster(self, namespace: str, name: str) -> Dict[str, Any]:
        """Get details of a specific database cluster."""
        return self._make_request("GET", f"/namespaces/{namespace}/database-clusters/{name}")

    def get_database_cluster_credentials(self, namespace: str, name: str) -> Dict[str, Any]:
        """Get credentials for a specific database cluster."""
        return self._make_request("GET", f"/namespaces/{namespace}/database-clusters/{name}/credentials")

    def get_database_cluster_components(self, namespace: str, name: str) -> Dict[str, Any]:
        """Get components of a specific database cluster."""
        return self._make_request("GET", f"/namespaces/{namespace}/database-clusters/{name}/components")

    def update_database_cluster(self, namespace: str, name: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Update a database cluster's specification."""
        return self._make_request("PUT", f"/namespaces/{namespace}/database-clusters/{name}", json={"spec": spec})
