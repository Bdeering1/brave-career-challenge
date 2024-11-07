from os import environ
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = environ.get('OPENAI_API_KEY')
ORGANIZATION_ID = environ.get('ORGANIZATION_ID')
PROJECT_ID = environ.get('PROJECT_ID')
