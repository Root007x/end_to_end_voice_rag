import os
import sys
import logging
from src.mysoft_rag.config import config

log_dir = config.logger.log_dir
logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"

log_file_path = os.path.join(log_dir, "system_logs.log")

os.makedirs(log_dir, exist_ok=True)


logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[logging.FileHandler(log_file_path), logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("rag")
