import logging
import sys
from pathlib import Path

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

LOG_FILE = Path(__file__).parent / 'anime_downloader.log'

class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    } if COLORAMA_AVAILABLE else {}

    def format(self, record):
        msg = super().format(record)
        if COLORAMA_AVAILABLE:
            color = self.COLORS.get(record.levelno, '')
            reset = Style.RESET_ALL
            return f"{color}{msg}{reset}"
        return msg

# Create logger
logger = logging.getLogger("anime_downloader")
logger.setLevel(logging.DEBUG)
logger.propagate = False

# Console handler with color
console_handler = logging.StreamHandler(sys.stdout)
console_format = ColorFormatter('[%(asctime)s] [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(console_format)
console_handler.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_format = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_format)
file_handler.setLevel(logging.DEBUG)

# Add handlers if not already present
if not logger.hasHandlers():
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
else:
    # Avoid duplicate handlers in reloads
    logger.handlers.clear()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

# Convenience functions
log_debug = logger.debug
log_info = logger.info
log_warning = logger.warning
log_error = logger.error
log_critical = logger.critical

__all__ = [
    "logger",
    "log_debug",
    "log_info",
    "log_warning",
    "log_error",
    "log_critical",
]
