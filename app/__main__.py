"""Application main process."""

import logging
import argparse

from app.aggregator import Aggregator

FORMAT = '%(asctime)s %(message)s'
USAGE = 'usage: app [-h] [--input INPUT] [--output OUTPUT]'

logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Screeing app.")
    parser.add_argument('--input', dest='input')
    parser.add_argument('--output', dest='output')
    args = parser.parse_args()
    if args.input is None or args.output is None:
        logger.info(USAGE)
        exit(1)

    logger.info("Starting the application.")
    logger.info(f"Reading directory: {args.input}")
    logger.info(f"Writing to file: {args.output}")

    aggregator = Aggregator(input_dir=args.input)
    aggregator.aggregate()
    average = aggregator.field_average()
    total = aggregator.total_count() 
    logger.info(f"Average number of fields: {average}.")
    logger.info(f"Total number of rows: {total}.")

    logger.info("================================")
    logger.info("Generating file with word counts.")
    aggregator.create_counts_file(file_name=args.output)
    logger.info("Done generating file.")
    logger.info("Done scanning.")
 
