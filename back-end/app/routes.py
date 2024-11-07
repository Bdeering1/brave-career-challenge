from app import app, prompt, scrape
from flask import request, json


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/scrape')
def scrape_url():
    url = request.args.get('url')

    site_data = scrape.get_data(url)
    res = prompt.get_question(site_data.name, site_data.description)

    response = app.response_class(
        response=json.dumps(f'{res}'),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
