import requests
print(requests.post(
    "https://825c-39-62-43-117.in.ngrok.io",
    json= {
        "sender":"test_user",
        "message":"Hello",
        }
    ).text
)