import os
from dotenv import load_dotenv


load_dotenv('database/envs/.env')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG=True

config = {
    'default': Config
}