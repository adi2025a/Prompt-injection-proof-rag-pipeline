# logger.py
import logging
import os

# Define log directory and file
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,  # Change to DEBUG for more detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create a logger instance
logger = logging.getLogger("fastapi_logger")