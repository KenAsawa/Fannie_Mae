import os
from os import getenv

from dotenv import load_dotenv
from flask import Flask, jsonify, session
from flask_cors import CORS
from requests import get

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
CORS(app, supports_credentials=True)
app.config.update(
    DEBUG=True,
    JSON_SORT_KEYS=False,
    JSONIFY_PRETTYPRINT_REGULAR=False
)

# The endpoint for retrieving loan information from the Fannie Mae API, ordered by state
loans_endpoint = "https://api.theexchange.fanniemae.com/v1/manufactured-housing-loans/calculations-by-state"


# [GET] /loans
# Retrieves and sends loan information from the Fannie Mae API
@app.route("/api/get-loans/")
def get_loans():
    # Retrieve data from the Fannie Mae API loans endpoint
    headers = {'Authorization': getenv('USER_TOKEN')}
    data = get(loans_endpoint, headers=headers)

    # Proxy the data response to the original request
    return jsonify(data.json())


# [GET] /loans
# Retrieves and sends loan information from the Fannie Mae API
@app.route("/api/get-counties/<state_id>")
def get_counties(state_id):
    endpoint = "https://search.onboard-apis.com/areaapi/v2.0.0/county/lookup?StateId=ST" + state_id
    headers = {'apikey': getenv('API_KEY'), 'accept': 'application/json'}
    app.logger.info(session.get("state_ids", []))
    response = get(endpoint, headers=headers)
    data = response.json()
    data = data["response"]["result"]["package"]["item"]
    # Proxy the data response to the original request
    return jsonify(data)


@app.route("/")
def get_state_ids():
    app.logger.info('Getting State ID\'s')
    endpoint = "https://search.onboard-apis.com/areaapi/v2.0.0/state/lookup"
    headers = {'apikey': getenv('API_KEY'), 'accept': 'application/json'}
    response = get(endpoint, headers=headers)
    if response.status_code != 200:
        app.logger.error('Could not retrieve State ID\'s')
        state_ids = []
    else:
        data = response.json()
        state_ids = data["response"]["result"]["package"]["item"]
        app.logger.info('State ID\'s Retrieved')
    session["state_ids"] = state_ids
    return jsonify(state_ids)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8000), debug=True)
    get_state_ids()
