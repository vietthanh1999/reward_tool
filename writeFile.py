import logging
from datetime import date

logging.basicConfig(filename='result-'+str(date.today())+'.txt', format="%(message)s")
logging.fatal('234234|123123123')