import requests
from flask import Flask, request
app = Flask(__name__)

# Adds support for GET requests to our webhook
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
    print(output)
    return 'ok'

if __name__ == "__main__":
    app.run(threaded=True, port=80, debug = True)