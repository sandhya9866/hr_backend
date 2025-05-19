import nepali_datetime
from datetime import datetime,timedelta,date

def nepali_str_to_english(string_date):
    string_date_split=string_date.split("-")
    np_date = (nepali_datetime.date(int(string_date_split[0]),int(string_date_split[1]),int(string_date_split[2])))
    date = np_date.to_datetime_date()
    return date


def english_to_nepali(string_date):
    return nepali_datetime.date.from_datetime_date(string_date)

def nepali_to_english(date):
    # return date.np_date.to_datetime_date()
    return date.to_datetime_date()

def get_last_day():
    today = (nepali_datetime.date.today())
    first_day = nepali_datetime.date(today.year, today.month, 1)
    lastdate = first_day - timedelta(days=1)
    last_day = lastdate.day
    return last_day

def get_last_day_of_month(month_, year):
    month = str(month_)
    if month == 'BAISHAKH':
        month_num = 1
    elif month == 'JESTHA':
        month_num = 2
    elif month == 'ASAR':
        month_num = 3   
    elif month == 'SHRAWAN':
        month_num = 4   
    elif month == 'BHADAU':
        month_num = 5 
    elif month == 'ASWIN':
        month_num = 6 
    elif month == 'KARTIK':
        month_num = 7
    elif month == 'MANGSHIR':
        month_num = 8
    elif month == 'POUSH':
        month_num = 9   
    elif month == 'MAGH':
        month_num = 10 
    elif month == 'FALGUN':
        month_num = 11 
    elif month == 'CHAITRA':
        month_num = 12 
    else:
        month_num = month_
    next_month =  month_num + 1


    if next_month>12:
        next_month=1
        year = int(year)+1

    next_month_first_day = nepali_datetime.date(int(year), next_month, 1)
    lastdate = next_month_first_day - timedelta(days=1)
    lastday = lastdate.day
    firstdate = lastdate - timedelta(days=int(lastdate.day-1))
    start_end_dates = (firstdate,lastdate, lastday, month_num)
    return start_end_dates

def finding_fiscal_date(year, month):
    if month in [1,2,3,4]:
        current_fiscal_year = year - 1

        return {"start_year":current_fiscal_year, "start_month":4, "start_day":1, "end_year":year, "end_month":3, "end_day":30}
    
    else:
        current_fiscal_year = year + 1
        return {"start_year":year, "start_month":4, "start_day":1, "end_year":current_fiscal_year, "end_month":3, "end_day":30}