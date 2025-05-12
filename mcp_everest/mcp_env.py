
"""Environment configuration for the MCP Percona Everest server.

This module handles all environment variable configuration with sensible defaults
and type conversion.
"""

from dotenv import load_dotenv
from dataclasses import dataclass
import os


@dataclass
class EverestEnvConfig:
    """Configuration for Everest connection settings.

    Required environment variables:
        EVEREST_HOST: Everest API base URL (default: http://localhost:8080)
        EVEREST_API_KEY: The API key for authentication
        EVEREST_VERIFY_SSL: Whether to verify SSL certificates (default: true)
        EVEREST_TIMEOUT: Request timeout in seconds (default: 30)
        EVEREST_READONLY: Whether to run in read-only mode (default: false)
    """

    def __init__(self):
        """Initialize the configuration from environment variables."""
        load_dotenv()

    @property
    def host(self) -> str:
        """Get the Everest Base URL."""
        return os.getenv("EVEREST_HOST", "http://localhost:8080")

    @property
    def api_key(self) -> str:
        """Get the Everest API Key."""
        return os.getenv("EVEREST_API_KEY")

    @property
    def verify_ssl(self) -> bool:
        """Get SSL verification setting."""
        return os.getenv("EVEREST_VERIFY_SSL", "true").lower() == "true"

    @property
    def timeout(self) -> int:
        """Get request timeout."""
        return int(os.getenv("EVEREST_TIMEOUT", "30"))

    @property
    def readonly(self) -> bool:
        """Get readonly mode setting."""
        return os.getenv("EVEREST_READONLY", "false").lower() == "true"

    def validate(self) -> None:
        """Validate that all required environment variables are set.

        Raises:
            ValueError: If any required environment variable is missing.
        """
        if not self.api_key:
            raise ValueError("EVEREST_API_KEY environment variable is required")


# Global instance for easy access
config = EverestEnvConfig()
