# config.py
import logging

logger = logging.getLogger(__name__)


def get_logger(roll):
    logging.basicConfig(
        filename="RAG.log",
        encoding="utf-8",
        format="%(asctime)s: %(roll)",
        level=logging.INFO,
    )
    logger.info("Reza Started")


if __name__ == "__main__":
    get_logger(roll="user")
