from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    ForeignKey,
    func)

from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    scoped_session)

from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import NVARCHAR
import config
from datetime import datetime
from passlib.hash import sha256_crypt
from config import config 



#SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost:3306/users'
SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://'+config.dbuser+":"+config.dbpass+"@"+config.dburl+":"+config.dbport+"/"+config.db
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
class Todoitem(Base):
    __tablename__ = 'todoitems'
    # A  class defination to each todo item
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    comment = Column(NVARCHAR(360))
    date_added = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, onupdate=datetime.utcnow)

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'added_date': self.date_added,
            'updated_date': self.date_updated
        }


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255), unique=False, nullable=True)
    last_name = Column(String(255), unique=False, nullable=True)
    password = Column(String(255), unique=False, nullable=False)
    authenticated = Column(Boolean, default=False)
    api_key = Column(String(255), unique=True, nullable=True)
    date_added = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, onupdate=datetime.utcnow)
    def encode_api_key(self):
        self.api_key = sha256_crypt.hash(self.username + str(datetime.utcnow))

    def encode_password(self):
        self.password = sha256_crypt.hash(self.password)

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    def get_username(self):
        return self.username
    def __repr__(self):
        return '<User %r>' % (self.username)


    def to_json(self):

        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'id': self.id,
            'api_key': self.api_key,
            'is_active': True
        }
# create tables
Base.metadata.create_all(bind=engine)

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

