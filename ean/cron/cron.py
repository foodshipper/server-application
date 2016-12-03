from cron.create_groups import create_groups
from database import create_tables


if __name__ == '__main__':
    print("Run")
    create_tables()
    create_groups()
