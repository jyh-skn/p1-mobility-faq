# CONFIG
# .env 파일을 읽어 객체로 변환.
import os
import json
from dotenv import load_dotenv
import sys
from pathlib import Path

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    DB = json.loads(os.getenv('DB_CONFIG', '{}'))
    OPINET = os.getenv("OPINET")

config_db = Config.DB
config_api_key = Config.API_KEY
config_opinet = Config.OPINET
# root directory
config_base_dir = Path(__file__).resolve().parent.parent

