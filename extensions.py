import json
import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

import os
basedir = os.path.abspath(os.path.dirname(__file__))
CREDENTIALS = json.load(open(os.path.join(basedir, 'credentials.json')))

username = CREDENTIALS["username"]
password = CREDENTIALS["password"]
hostname = CREDENTIALS["hostname"]
port = CREDENTIALS["port"]
database = CREDENTIALS["database"]

pymysql.install_as_MySQLdb()

url = f'mysql://{username}:{password}@{hostname}:{port}/{database}'

Base = declarative_base()
engine = create_engine(url)
Session = sessionmaker(bind=engine)

db = SQLAlchemy()

engine = sqlalchemy.create_engine(url)

#Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_session():
    return Session()