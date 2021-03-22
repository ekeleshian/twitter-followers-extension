import requests
import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

TWITTER_BEARER_AUTH_TOKEN = os.environ.get("TWITTER_AUTH_BEARER_TOKEN")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

def create_headers(bearer_token):
    print(bearer_token)
    headers = {"authorization": f"Bearer {bearer_token}"}
    return headers

@app.route("/username/<username>", methods=['GET'])
def calculate_human_likelihood(username):
    print(username)
    headers = create_headers(TWITTER_BEARER_AUTH_TOKEN)
    response = requests.get(
        'https://api.twitter.com/1.1/followers/ids.json?screen_name=twitterdev',
        headers=headers
    )
    print(response)
    print(response.json())
    return jsonify(followers="ok")

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)