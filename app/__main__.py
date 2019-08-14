import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting the application.")
    logger.info("Done scanning.")
