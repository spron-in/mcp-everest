
import os
from .everest_client import EverestClient, EverestConfig

def create_everest_client() -> EverestClient:
    """Create and return an Everest client instance."""
    config = EverestConfig(
        host=os.getenv("EVEREST_HOST", "http://localhost:8080"),
        api_key=os.getenv("EVEREST_API_KEY"),
        verify_ssl=os.getenv("EVEREST_VERIFY_SSL", "true").lower() == "true",
        timeout=int(os.getenv("EVEREST_TIMEOUT", "30"))
    )
    return EverestClient(config)
