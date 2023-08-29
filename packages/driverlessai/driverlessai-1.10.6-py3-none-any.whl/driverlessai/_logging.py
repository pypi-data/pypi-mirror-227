import logging

logger = logging.getLogger("driverlessai")


def configure_console_logger() -> None:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    logger.handlers.append(console_handler)
