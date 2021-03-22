import requests
import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

TWITTER_BEARER_AUTH_TOKEN = os.environ.get("TWITTER_AUTH_BEARER_TOKEN")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


def create_headers(bearer_token):
    headers = {"authorization": f"Bearer {bearer_token}"}
    return headers


def get_followers(username):
    api_path = f'https://api.twitter.com/1.1/followers/ids.json?screen_name={username}'
    headers = create_headers(TWITTER_BEARER_AUTH_TOKEN)
    response = requests.get(
        api_path,
        headers=headers
    )
    response_json = response.json()
    followers = response_json['ids']
    while response_json.get("next_cursor"):
        print('calling twitter server again....\n')
        response = requests.get(
            f'{api_path}&cursor={response_json.get("next_cursor_str")}',
            headers=headers
        )
        response_json = response.json()
        followers.extend(response_json['ids'])
        print(f'increasing followers to {len(followers)}')
    return followers


@app.route("/username/<username>", methods=['GET'])
def calculate_human_likelihood(username):
    print(username)
    followers = get_followers(username)
    print(len(followers))




    return jsonify(followers="ok")


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)