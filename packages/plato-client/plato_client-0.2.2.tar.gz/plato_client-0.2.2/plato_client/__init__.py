import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from envyaml import EnvYAML
from pydantic import BaseSettings, Field

from plato_client.core.plato_logger import PlatoLogHandler


def add_system_paths():
    """
    Add the parent directory of this file to the system path
    """
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    grandparent_dir = parent_dir.parent
    directories = [current_dir, parent_dir, grandparent_dir]
    for directory in directories:
        if str(directory) not in sys.path:
            # print(f"adding path {directory} to sys.path")
            sys.path.insert(0, str(directory))


def initialize_logging():
    """
    Initialize logging
    """
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    # root_logger.addHandler(PlatoLogHandler("plato_logs.log"))
    logging.config.fileConfig(
        Path(__file__).parent / "logging.ini", disable_existing_loggers=False
    )


add_system_paths()
initialize_logging()


PACKAGE_DIR = Path(__file__).parent.parent.resolve().absolute()
__version__ = open(str((PACKAGE_DIR / "VERSION").resolve().absolute())).read().strip()
load_dotenv(dotenv_path=PACKAGE_DIR / ".env")
CACHE = str((PACKAGE_DIR / ".cache").resolve().absolute())
os.makedirs(CACHE, exist_ok=True)
_current_dir = os.path.dirname(__file__)
CONFIG = EnvYAML(str((PACKAGE_DIR / "config" / "config.yaml").resolve().absolute()))
