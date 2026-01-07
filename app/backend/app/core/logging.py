from flask import Flask

import logging
from logging.handlers import RotatingFileHandler

from .config import config


def setup_logging(app: Flask, log_file_name : str = config.log_file) -> None:
    formatter  = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s "
    )
    
    # File handler (rotating logs)
    
    file_handler = RotatingFileHandler(
        log_file_name,
        maxBytes=5_000_000,
        backupCount=5
    )
    
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # console handler
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    
    # Attach Handlers
     
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(file_handler)
    # app.logger.addHandler(console_handler)