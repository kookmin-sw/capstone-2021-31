import datetime
def get_yester_day():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(1)

    res = yesterday.strftime('%y-%m-%d')

    return res

