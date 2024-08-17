import os
from dotenv import load_dotenv, find_dotenv
import openai
from distutils.util import strtobool


class Config:
    #API_KEY = os.environ.get("API_KEY", "default_key")
    #DATABASE_URL = os.environ.get("DATABASE_URL", "default_db_url")
    #DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "t")

    _ = load_dotenv(find_dotenv()) 
    #openai.api_key  = os.getenv('OPENAI_API_KEY')
    LOG_STATE_DATA=bool(strtobool(os.getenv('LOG_STATE_DATA')))

    print("xxxxxxxx Configuration Settings xxxxxxxxxxxx")
    print("Debug log: ",LOG_STATE_DATA)
    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    

config = Config()