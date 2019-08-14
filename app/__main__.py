#!/usr/bin/env python

import logging
from app.aggregator import Aggregator

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting the application.")
    aggregator = Aggregator(input_dir='data')
    aggregator.aggregate()
    average = aggregator.field_average()
    total = aggregator.total_count() 
    logger.info(f"Average number of fields: {average}.")
    logger.info(f"Total number of rows: {total}.")
    logger.info("================================")
    logger.info("Generating file with word counts.")
    aggregator.create_counts_file(file_name='count_file.csv')
    logger.info("Done generating file.")
    logger.info("Done scanning.")
 
