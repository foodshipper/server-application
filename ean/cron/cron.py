from ean.cron.send_notifications import send_invitations
from ean.cron.create_groups import create_groups, suggest_all_recipes
import logging

if __name__ == '__main__':
    logging.basicConfig(filename='foodship-cron.log', level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

    logging.info("Run Cronjob")
    create_groups()
    suggest_all_recipes()
    send_invitations()