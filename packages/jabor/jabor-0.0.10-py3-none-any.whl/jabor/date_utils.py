
from datetime import datetime, timedelta

DEFAULT_DATEFORMAT ='%Y-%m-%d'

def valid_date(date_text, dateformat=DEFAULT_DATEFORMAT):
        try:
            datetime.strptime(str(date_text), dateformat)
            return True
        except ValueError:
            return False




def validate_future_date(date, dateformat=DEFAULT_DATEFORMAT):
    if valid_date(date):
        if datetime.strptime(str(date), dateformat).date() > datetime.now().date():
            return f"Date cannot be in the past"
    else:
        return print('Invalid date')




def count_days_from_today(date_to, date_from=None, dateformat=DEFAULT_DATEFORMAT):
    if valid_date(date_to) == True:
        if date_from ==None:
            date_from = datetime.now().date()
        else:
            try:
               valid_date(date_from)
               date_from = datetime.strptime(str(date_from), dateformat).date() 
            except Exception as e:
               return f'{e}'
        try:
            selecteddate = datetime.strptime(date_to, dateformat).date()
            return (selecteddate-date_from).days
        except:
            return False
    else:
        return print('Invalid date')
        




def get_week_list_for_date(date_from, date_to=None, dateformat=DEFAULT_DATEFORMAT):
    if date_to ==None:
        date_to = datetime.now().date()
    date_range_list = []
    if valid_date(date_from) == True:
        for i in reversed(range(0,3)):
            ddate = datetime.strptime(date_from, dateformat).date() - timedelta(days=i)
            if count_days_from_today(date_from) >= -1:
               date_range_list.append(ddate)
        for i in range(1,3):
            ddate = datetime.strptime(date_from, dateformat).date() + timedelta(days=i)
            if count_days_from_today(date_from) >= 0:
               date_range_list.append(ddate)
        return(date_range_list)
    else:
        return print('Invalid date')