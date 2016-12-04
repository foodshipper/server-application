from ean.cron.create_groups import create_groups
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='foodship-cron.log', level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

    logging.info("Run Cronjob")
    create_groups()
