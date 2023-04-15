import requests
from datetime import datetime, timedelta
from pprint import pprint
from actions.fuzzyString import get_matched_name
# print(requests.post(
#     "https://825c-39-62-43-117.in.ngrok.io",
#     json= {
#         "sender":"test_user",
#         "message":"Hello",
#         }
#     ).text
# )

# Temporary Helping text for RASA Syntax

'''
To insert a new line in output of user response:

utter_greet:
    - text: |
        کسان آواز میں خوش آمدید
        آپ کس سروس کے متعلق جاننا چاہتے ہیں؟


'''
'''
most_matched_city = "لاہور"
received_day = "آج"
day_temp = "۲۰"
text = f"میں (city)[حیدرآباد] میں ہوں"
text = f"my account number is [1234567891](account_number)"
bot_response_to_send = f"{received_day} {most_matched_city} میں صبح کا درجہ حرارت {day_temp} ڈگری سینٹی گریڈ رہے گا۔"
print(text)
'''
def relative_day_no(day_name, DB_update_time = datetime.now().timestamp()):
    """An Intellegent Function that can return the day number
    in reference with the database update day/current day
    
    >>> 0 for today
    >>> 1 for tomorrow
    
    Similarly, day-number for current week day-name starting with today as 0

    Args:
        day_name (str): day name i.e., آج، کل، سوموار
        DB_update_time (class.datetime.timestamp, optional): Last update timestamp for database. Defaults to datetime.now().timestamp().

    Returns:
        int: day-number for datebase record reterival
    """
    relative_day = {
        "آج" : 0,
        "کل" : 1,
        "پرسوں" : 2
    }
    
    days_ur_en = {
        "پیر" : "Monday",
        "سوموار" : "Monday",
        "منگل" : "Tuesday",
        "بدھ" : "Wednesday",
        "جمعرات" : "Tursday",
        "جمعہ" : "Friday",
        "ہفتہ" : "Saturday",
        "اتوار" : "Sunday",
    }
    
    week_days = dict()
    
    for i in range(7):
        # Got date of current day and procedings
        date = datetime.fromtimestamp(DB_update_time) + timedelta(days=i)
        
        # Got today and procedings
        day = datetime.strftime(date, '%A')
        
        # print(day)
        week_days[day] = i
    
    # print(week_days)
    # pprint(days_ur_en)
    
    # {
    #     'Friday': 0,
    #     'Saturday': 1,
    #     'Sunday': 2,
    #     'Monday': 3,
    #     'Tuesday': 4,
    #     'Wednesday': 5,
    #     'Thursday': 6
    #     }
    
    if day_name in relative_day:
        # Got date of current day 
        today_name = datetime.today().strftime('%A')
        return week_days[today_name] + relative_day[day_name]
    
    if day_name in days_ur_en:
        day_en = days_ur_en[day_name]
        day_no = week_days[day_en]
        return day_no
    
    if day_name not in relative_day or day_name == None:
        return 0
    
    # # Get current TimeStamp
    # print("Current TimeStamp: ", datetime.now().timestamp())
    
    # # Get curent Time converted from current TimeStamp
    # print("curent Time converted from current TimeStamp: ", datetime.fromtimestamp(datetime.now().timestamp()))
    
    # # Get Current/ today date and time
    # print("Current/ today date and time: ", datetime.today())
    
    # # Get Current week day number
    # print("Current week day name: ", datetime.today().weekday())
    
    # # Get ToDay Name
    # print("Current week day number: ", datetime.today().strftime('%A'))
    
    # # Get Time from TimeStamp
    # print("Time from TimeStamp: ", datetime.fromtimestamp(DB_update_time))
    return None
import sys



if __name__ == "__main__":
    print("Current week day no:", datetime.today().weekday())
    print(datetime.fromtimestamp(1681455600), "Gujranwala Previous")
    print(relative_day_no("ہفتہ",1681455600))
    print(relative_day_no("آج",1681455600))
    print(relative_day_no("کل",1681455600))
    print(relative_day_no("پرسوں",1681455600))
    # print(get_matched_name("لاہو", "city"))
    # print(get_matched_name("سومو", "day"))
    # print(datetime.fromtimestamp(1678604400), "Karachi Previous")
    # print(datetime.fromtimestamp(1678863600), "Karachi New")
    