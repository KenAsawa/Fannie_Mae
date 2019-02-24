from os import getenv

from dotenv import load_dotenv
from flask import Flask, jsonify
from requests import get

# Load environment variables
load_dotenv()

app = Flask(__name__)

# The endpoint for retrieving loan information from the Fannie Mae API, ordered by state
loans_endpoint = "https://api.theexchange.fanniemae.com/v1/manufactured-housing-loans/calculations-by-state"


# [GET] /loans
# Retrieves and sends loan information from the Fannie Mae API
@app.route("/loans")
def get_loans():
    # Retrieve data from the Fannie Mae API loans endpoint
    headers = {'Authorization': getenv('USER_TOKEN')}
    data = get(loans_endpoint, headers=headers)

    # Proxy the data response to the original request
    return jsonify(data.json())


if __name__ == "__main__":
    app.run(debug=True)
