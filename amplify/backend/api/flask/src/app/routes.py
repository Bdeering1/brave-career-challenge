from app import app, db, prompt, scrape, util
from flask import request
import time


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/scrape')
def scrape_url():
    start = time.time()

    url = request.args.get('url')
    db_test = request.args.get('db-test') is not None
    force_prompt = request.args.get('force-prompt') is not None

    if url is None:
        return util.json_response('No URL provided', 400)

    url_root = util.url_root(url)
    if url_root is None:
        return util.json_response('Invalid URL', 400)

    conn, cur = db.connect()
    if conn is None:
        return util.json_response('Internal server error: failed to connect to DB', 500)

    db_entry = db.get_site_data(cur, url_root)
    if db_entry is not None:
        site_info, question = db_entry

    # Only check for db entry
    if db_test:
        db.close(conn, cur)

        if db_entry is None:
            return util.json_response(f'No entry for {url}', 200)
        return util.json_response(question.__dict__, 200)

    # No site entry found, scrape site
    if db_entry is None:
        site_info = scrape.get_data(url)

        if not site_info.success:
            db.close(conn, cur)
            return util.json_response(site_info.description, site_info.status)

        db.create_site(cur, url_root, site_info)

    # No site entry found, or re-prompt requested
    if db_entry is None or question is None or force_prompt:
        question = prompt.get_question(site_info.name, site_info.description, site_info.offerings)
        if question is None:
            return util.json_response('Internal server error: failed to connect to ChatGPT', 500)

        db.update_question(cur, url_root, question)

    db.close(conn, cur)

    elapsed = time.time() - start
    print(f'Response time: {elapsed}', flush=True)

    return util.json_response(question.__dict__, 200)
