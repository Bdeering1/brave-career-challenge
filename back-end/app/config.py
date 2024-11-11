from os import environ
from dotenv import load_dotenv

load_dotenv()

DB_NAME = environ.get('DB_NAME')
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_HOST = environ.get('DB_HOST')
DB_PORT = environ.get('DB_PORT')

OPENAI_API_KEY = environ.get('OPENAI_API_KEY')
ORGANIZATION_ID = environ.get('ORGANIZATION_ID')
PROJECT_ID = environ.get('PROJECT_ID')
