from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PersonBase(BaseModel):
	name: str = Field(min_length=1)
	email: str = Field(min_length=6)

	
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


# db_dependency = Annotated(Session, Depends(get_db))

# Read
@app.get("/api/user_id")
def read_person(person_id:int = None, name:str = None, email:str = None,db: Session = Depends(get_db)):
	if person_id is None and name is None and email is None:
		return db.query(models.Person).all()
	if email is not None:
		person_model = db.query(models.Person).filter(models.Person.email == email).first()
	
	elif email is None and name is not None:
		person_model = db.query(models.Person).filter(models.Person.name == name).first()
	
	else:
		person_model = db.query(models.Person).filter(models.Person.id == person_id).first()

	return person_model


# Create
@app.post("/api")
def create_name(name: str, email:str=None, db: Session = Depends(get_db)):
	person_model = models.Person()
	person_model.name = name
	person_model.email = email

	db.add(person_model)
	db.commit()

	return person_model


@app.put("/api/user_id")
def update_book(user_id: int, name:str = None, email:str = None, db: Session = Depends(get_db)):
	if user_id is not None:
		person_model = db.query(models.Person).filter(models.Person.id == user_id).first()
	elif name is not None:
		person_model = db.query(models.Person).filter(models.Person.name == name).first()
	elif email is not None:
		person_model = db.query(models.Person).filter(models.Person.email == email).first()
		

	person_model = db.query(models.Person).filter(models.Person.id == user_id).first()

	if person_model is None:
		raise HTTPException(
			status_code=404,
			detail=f"ID {user_id} : Does not exist"
		)

	if name is not None:
		person_model.name = name
		if email is not None:
			person_model.email = email
	elif email is not None:
		person_model.email = email
		if name is not None:
			person_model.name = name
	

	db.add(person_model)
	db.commit()

	return person_model


@app.delete("/api/user_id")
def delete_book(user_id: int = None, name:str = None, db: Session = Depends(get_db)):
	if user_id is not None:
		person_model = db.query(models.Person).filter(models.Person.id == user_id).first()
		if person_model is None:
			raise HTTPException(
			status_code=404,
			detail=f"ID {user_id} : Does not exist"
		)

		db.query(models.Person).filter(models.Person.id == user_id).delete()
		db.commit()
	elif name is not None:
		person_model = db.query(models.Person).filter(models.Person.name == name).first()
		if person_model is None:
			raise HTTPException(
			status_code=404,
			detail=f"ID {user_id} : Does not exist"
		)

		db.query(models.Person).filter(models.Person.name == name).delete()
		db.commit()
	
	return True