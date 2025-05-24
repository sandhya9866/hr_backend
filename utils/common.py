#calculate no_of_leave based on condition
import nepali_datetime, datetime

def point_down_round(value):
    whole = int(value)
    decimal = value - whole

    if decimal < 0.5:
        return whole
    elif 0.5 <= decimal or decimal <= 0.9:
        return whole + 0.5
    
def get_today_date(request):
    nepali_date_today = nepali_datetime.date.today().strftime('%K-%n-%D')
    english_date_today = datetime.datetime.now().strftime ("%Y-%m-%d")
    return {'nepali_date_today':nepali_date_today, 'english_date_today':english_date_today}