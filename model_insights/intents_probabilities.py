import requests
import json
import csv, time

host_url = "http://localhost:5005/model/parse"   #to determine the host port, refer to endpoint.yml

# read examples of each intents from file
with open('all_intents.txt') as f:
    intents = f.read().splitlines()

with open('all_messages.txt', encoding="UTF-8") as f:
    messages = f.read().splitlines()

for message in messages:
    time.sleep(1)
    # get intent confidence scores for message
    nlu_data = json.dumps({'text': f"{message}"})
    nlu_resp = requests.post(host_url, data=nlu_data).json()
    intent_ranking = nlu_resp['intent_ranking']

    # write intent confidence scores to CSV
    with open('intent_confidences.csv', mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writerow(['Intent', 'Confidence'])
        for intent in intent_ranking:
            if intent['name'] in intents:
                writer.writerow([intent['name'], intent['confidence']])
            continue
