import json
import logging
import logging.config


class PlatoLogHandler(logging.FileHandler):
    """Custom Plato Log Handler"""

    def __init__(self, filename, mode="a", encoding=None, delay=False):
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record):
        log_entry = {
            "timestamp": record.created,
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "thread": record.threadName,
            "module": record.module,
            "line": record.lineno,
            "func": record.funcName,
        }

        self.stream.write(json.dumps(log_entry))
        self.stream.write("\n")
        self.flush()
