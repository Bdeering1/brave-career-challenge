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
    scrape_only = request.args.get('scrape-only') is not None

    scrape_res = scrape.get_data(url)
    if not scrape_res.success:
        return app.response_class(
            response=json.dumps(scrape_res.description),
            status=scrape_res.status,
            mimetype='application/json'
        )

    if scrape_only:
        res = scrape_res
    else:
        res = prompt.get_question(scrape_res.name, scrape_res.description, scrape_res.offerings)

    elapsed = time.time() - start
    print(f'Response time: {elapsed}', flush=True)

    response = app.response_class(
        response=json.dumps(res.__dict__),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
