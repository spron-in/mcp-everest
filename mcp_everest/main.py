
"""Internal main module, not meant to be run directly."""

def main():
    from .mcp_server import mcp
    mcp.run()
