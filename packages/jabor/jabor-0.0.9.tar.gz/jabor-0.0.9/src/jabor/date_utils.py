
from datetime import datetime, timedelta

dateformat ='%Y-%m-%d'

def valid_date(date_text, dateformat=dateformat):
        try:
            datetime.strptime(str(date_text), dateformat)
            return True
        except ValueError:
            return False

def validate_future_date(date, dateformat=dateformat):
    if valid_date(date):
        if datetime.strptime(str(date), dateformat).date() > datetime.now().date():
            return f"Date cannot be in the past"
    else:
        return print('Invalid date')

def count_days_from_today(date, dateformat=dateformat):
    if valid_date(date) == True:
        try:
            today = datetime.now()
            selecteddate = datetime.strptime(date, dateformat)
            return (selecteddate-today).days
        except:
            return False
    else:
        return print('Invalid date')
        

def get_week_list_for_date(date, dateformat=dateformat):
    list = []
    if valid_date(date) == True:
        for i in reversed(range(0,3)):
            ddate =datetime.strptime(date, dateformat).date() - timedelta(days=i)
            if count_days_from_today(ddate.strftime(dateformat)) >= -1:
               list.append(ddate)
        for i in range(1,3):
            ddate =datetime.strptime(date, dateformat).date() + timedelta(days=i)
            if count_days_from_today(ddate.strftime(dateformat)) >= 0:
               list.append(ddate)
        return(list)
    else:
        return print('Invalid date')