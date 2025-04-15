import logging
import os
import sys
from pathlib import Path

def get_logger(name: str) -> logging.Logger:
    """Create and configure a logger with both console and file handlers."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        try:
            logger.setLevel(logging.INFO)

            worker = os.getenv('PYTEST_XDIST_WORKER', 'main')
            format_str = f'%(asctime)s | %(levelname)s | {worker} | %(message)s'
            datefmt = "%Y-%m-%d %H:%M:%S"

            # Console logging
            console_handler = logging.StreamHandler(sys.stdout)
            console_formatter = logging.Formatter(format_str, datefmt=datefmt)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            logger.info("Console logging configured successfully")

            # File logging
            log_path = Path("logs")
            log_path.mkdir(exist_ok=True)
            file_handler = logging.FileHandler(log_path / "test.log")
            file_formatter = logging.Formatter(format_str, datefmt=datefmt)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
            logger.info(f"File logging configured successfully at {log_path / 'test.log'}")

        except Exception as e:
            logger.error(f"Failed to configure logger: {e}")
            raise

    return logger

