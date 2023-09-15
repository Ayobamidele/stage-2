from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from sqlalchemy_utils import EmailType
import datetime


class Person(Base):
	__tablename__ = "persons"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(50), unique=True)
	email = Column(EmailType)
	created_date = Column(DateTime, default=datetime.datetime.utcnow)
