# app/main.py
from time import sleep
from std_logging import logger

from network import does_record_match, get_public_ipv4
from providers.cloudflare import update_or_create_record, cf


if __name__ == "__main__":
    logger.info("Starting simpleDDNS")
    while True:
        if does_record_match():
            logger.info("Records match, no update needed")
        else:
            logger.info("Records do not match, updating")
            update_or_create_record(get_public_ipv4(), cf)
        logger.info("Checking again in 15 minutes")
        sleep(900)