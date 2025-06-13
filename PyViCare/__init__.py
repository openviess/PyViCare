import logging
import subprocess

# Configure basic logging if no handlers are configured
if not logging.getLogger().hasHandlers():
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.info("testxxxx - custom library")
