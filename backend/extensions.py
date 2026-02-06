import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import pymysql

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# pymysql is used as MySQLdb
pymysql.install_as_MySQLdb()

# Retrieve environment variables
# Support both standalone deployment (.env) and addon deployment (MYSQL_* vars)
username = os.getenv("MYSQL_USER") or os.getenv("root_username")
password = os.getenv("MYSQL_PASSWORD") or os.getenv("password")
hostname = os.getenv("MYSQL_HOST") or os.getenv("hostname", "db")
port = os.getenv("port", "3306")
database = os.getenv("MYSQL_DATABASE") or os.getenv("database")
email = os.getenv("email")
email_password = os.getenv("email_password")

# Database URL
url = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}'

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(url)
Session = sessionmaker(bind=engine)

db = SQLAlchemy()
print("Initialized SQLAlchemy")

# Uncomment this if you want to create tables at startup
# Base.metadata.create_all(bind=engine)

session = Session()

def get_session():
    return Session()
