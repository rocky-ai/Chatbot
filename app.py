import requests
from flask import Flask, request
from nltk.tokenize import word_tokenize
import nltk
import json

app = Flask(__name__)

# Adds support for GET requests to our webhook
FB_ACCESS_TOKEN = "EAAs93VcwujcBAI7VF6hV4PhLyR9ngOs78qc1Yah91WHzY0DXZBZBF9VHEQwrGWmU9NDFv89faeF4Vjh7SYUEY1XppIv3Bg3toZBmqg68rThmrU8pGZC5nP7xC6dEbsZCQTMcWXqQPLIK7f1BP14zDgF0IuW8WAvA1Ay1ZBevtpNnbFjj1JMdtJ"

URL = "https://graph.facebook.com/v8.0/me/messages?access_token=" + FB_ACCESS_TOKEN

def send(text, user) :
	#print(user)
	data = {
		"messaging_type" : "RESPONSE",
		"recipient" : {
			"id" : user
		},
		"message" : {
			"text" : text
		}
	}
	headers = {
		"Content-Type" : "application/json"
	}
	response = requests.post(URL, data = json.dumps(data), headers = headers)	
	print(response)

def hello(user) :
	send("Hello", user)

def unknown(user) :
	send("unknown", user)

intent_map = {
	"hi" : hello,
	"unknown" : unknown
}

def get_intent(text, user) :
	tokens = word_tokenize(text)
	flag = 0
	for token in tokens :
		for key in intent_map :
			if token.lower() == key :
				intent_map[key](user)
				flag = 1
	if flag == 0 :
		intent_map["unknown"](user)

def process_message(request) :
	#nltk.download("punkt")
	entry = request.get("entry")
	message_details = entry[0]['messaging'][0]
	sender = message_details['sender']['id']
	text = message_details['message']['text']
	get_intent(text, sender)

@app.route('/webhook',methods=['GET'])
def webhook():
    verify_token = request.args.get("hub.verify_token")
    # Check if sent token is correct
    print(request)
    if verify_token == "abcdefh" :
    	return request.args.get("hub.challenge")
    return "Unrecognised"

@app.route("/webhook", methods=['POST'])
def webhook_handle():
    output = request.get_json()
    #print(type(output))
    process_message(request.get_json())
    #print(output)
    return 'ok'

if __name__ == "__main__":
    app.run(threaded=True, port=80, debug = True)