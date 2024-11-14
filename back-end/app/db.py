from app import config
from app.scrape import SiteInfo
from pydantic import BaseModel
import psycopg2


class SurveyQuestion(BaseModel):
    prompt: str
    options: list[str]


def connect():
    conn = psycopg2.connect(
        database=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT
    )
    cur = conn.cursor()

    return [conn, cur]


def get_site_data(cur, url):
    cur.execute('''select name, description, offerings, prompt, options
                   from site
                   where url_root = %s''',
                [url])
    res = cur.fetchone()

    if res is None:
        return None
    return (SiteInfo(name=res[0], description=res[1], offerings=res[2]),
            SurveyQuestion(prompt=res[3], options=res[4]))


def create_site(cur, url_root, site_info):
    cur.execute('''insert into site (url_root, name, description, offerings)
                    values (%s, %s, %s, %s)''',
                [url_root, site_info.name, site_info.description, site_info.offerings])


def update_question(cur, url_root, question):
    cur.execute('''update site
                   set prompt = %s, options = %s
                   where url_root = %s''',
                [question.prompt, question.options, url_root])


def close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()
