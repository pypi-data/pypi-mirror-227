from honeyhive.api.client import HoneyHive, get_client
from typing import Dict, Optional
import honeyhive


def honeyhive_client() -> HoneyHive:
    """Get a HoneyHive client"""
    return get_client("https://api.honeyhive.ai", honeyhive.api_key)

__all__ = ["honeyhive_client"]