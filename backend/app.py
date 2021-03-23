from collections import defaultdict
import requests
import os
from flask import Flask, jsonify
from flask_cors import CORS
import botometer

rapidapi_key = os.environ.get("RAPID_API_KEY")

twitter_app_auth = {
    'consumer_key': os.environ.get("TWITTER_API_KEY"),
    'consumer_secret': os.environ.get("TWITTER_API_SECRET"),
    'access_token': os.environ.get("TWITTER_ACCESS_TOKEN"),
    'access_token_secret': os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          rapidapi_key=rapidapi_key,
                          **twitter_app_auth)

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


def check_accounts(followers):
    results = defaultdict(int)
    try:
        for screen_name, scores in bom.check_accounts_in(followers):
            print(f'screen_name: {screen_name}')
            print(f'scores: {scores}')
            if scores:
                e_cap = scores.get('cap').get('english')
                u_cap = scores.get('cap').get('universal')
                cap_mean = (e_cap + u_cap) / 2
                if cap_mean >= 0.8:
                    results['bot'] += 1
                elif 0.5 <= cap_mean < 0.8:
                    results['unsure'] += 1
                else:
                    results['human'] += 1
            else:
                results['unsure'] += 1
    except:
        results['unsure'] += 1
    return results


@app.route("/username/<username>", methods=['GET'])
def calculate_human_likelihood(username):
    followers = get_followers(username)
    results = check_accounts([int(f) for f in followers])
    print(results)
    return jsonify(**results)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)