
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from database.config import config


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config_name='default'):
    from flask import Flask
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    return app