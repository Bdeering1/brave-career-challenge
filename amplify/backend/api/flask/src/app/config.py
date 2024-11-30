from os import environ
from dotenv import load_dotenv


def get_secret(name):
    secret = environ.get(name) or open(f'/run/secrets/{name}').read()
    return secret.rstrip('\n')


load_dotenv()

POSTGRES_DB = environ.get('POSTGRES_DB')
POSTGRES_USER = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = get_secret('POSTGRES_PASSWORD')
POSTGRES_HOST = environ.get('POSTGRES_HOST')
POSTGRES_PORT = environ.get('POSTGRES_PORT')

OPENAI_API_KEY = get_secret('OPENAI_API_KEY')
ORGANIZATION_ID = environ.get('ORGANIZATION_ID')
PROJECT_ID = environ.get('PROJECT_ID')
