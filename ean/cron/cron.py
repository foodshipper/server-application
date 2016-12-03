from cron.create_groups import create_groups
from database import create_tables

def cron():
    create_tables()
    create_groups()
    print("Run")