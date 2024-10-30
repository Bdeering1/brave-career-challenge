#!/usr/bin/env python3

from flask import Flask, request, json

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/scrape')
def scrape_url():
    url = request.args.get('url')
    data = f"received request to scrape '{url}'"

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run(debug=True)
