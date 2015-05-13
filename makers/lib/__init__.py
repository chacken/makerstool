from datetime import datetime
from datetime import timedelta

def day(days=1):
  return timedelta(days=days)

today = datetime.today().date()
yesterday = today-day()
