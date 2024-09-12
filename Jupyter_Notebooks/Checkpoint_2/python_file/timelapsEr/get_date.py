import time, datetime

def get_today():
    return str(datetime.datetime.today().strftime('%d-%m-%Y'))

def get_now():
    return str(datetime.datetime.today().strftime('%Hhr%Mmin%Ssec'))