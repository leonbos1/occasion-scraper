import json
import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CREDENTIALS = json.load(open("credentials.json"))

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

def get_session():
    return Session()