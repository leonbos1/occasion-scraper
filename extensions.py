import json
import pymysql
from sqlalchemy.ext.declarative import declarative_base

CREDENTIALS = json.load(open("credentials.json"))

username = CREDENTIALS["username"]
password = CREDENTIALS["password"]
hostname = CREDENTIALS["hostname"]
port = CREDENTIALS["port"]
database = CREDENTIALS["database"]

pymysql.install_as_MySQLdb()

url = f'mysql://{username}:{password}@{hostname}:{port}/{database}'

Base = declarative_base()