from os import environ
from dotenv import load_dotenv

load_dotenv()
TEST_KEY = environ.get('TEST_KEY')
