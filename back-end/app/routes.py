from app import app, prompt, scrape
from flask import request, json
import time


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/scrape')
def scrape_url():
    start = time.time()

    url = request.args.get('url')

    scrape_res = scrape.get_data(url)
    if not scrape_res.success:
        return app.response_class(
            response=json.dumps(scrape_res.description),
            status=scrape_res.status,
            mimetype='application/json'
        )

    res = ''  # prompt.get_question(site_data.name, site_data.description)

    elapsed = time.time() - start
    print(f'response time: {elapsed}', flush=True)

    response = app.response_class(
        response=json.dumps(f'{scrape_res.name}: {scrape_res.description} {res}'),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
