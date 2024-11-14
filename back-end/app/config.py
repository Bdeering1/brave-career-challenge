from os import environ
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = environ.get('POSTGRES_DB')
POSTGRES_USER = environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = environ.get('POSTGRES_HOST')
POSTGRES_PORT = environ.get('POSTGRES_PORT')

OPENAI_API_KEY = environ.get('OPENAI_API_KEY')
ORGANIZATION_ID = environ.get('ORGANIZATION_ID')
PROJECT_ID = environ.get('PROJECT_ID')
