import requests
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

most_matched_city = "لاہور"
received_day = "آج"
day_temp = "۲۰"
text = f"میں (city)[حیدرآباد] میں ہوں"
text = f"my account number is [1234567891](account_number)"
bot_response_to_send = f"{received_day} {most_matched_city} میں صبح کا درجہ حرارت {day_temp} ڈگری سینٹی گریڈ رہے گا۔"
print(text)

print(round(2.300004,3))