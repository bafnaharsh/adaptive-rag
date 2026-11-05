"""
Logger configuration module. Logs go to stderr: the MCP server speaks JSON-RPC on stdout, so nothing may print there.
"""

import logging
import sys

# Third-party libraries (ddgs/primp, httpx) stay at WARNING; only our own logger is chatty.
logging.basicConfig(stream=sys.stderr, level=logging.WARNING, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("adaptive_rag")
logger.setLevel(logging.INFO)
