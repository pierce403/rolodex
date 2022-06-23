from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Float, Integer, String, DateTime, MetaData, ForeignKey, func
import os
import random
import string

from dataclasses import dataclass, asdict

db=SQLAlchemy()

@dataclass
class People(db.Model):
  id: int = db.Column(db.Integer, primary_key=True)

  # stuff to include in asdict() must be annoted like :str
  rocket_id: str = db.Column(db.String(80))
  first_name:str = db.Column(db.String(80))
  last_name: str = db.Column(db.String(80))

  personal_email = db.Column(db.String(80))
  work_email = db.Column(db.String(80))

  work_ntlm = db.Column(db.String(80))
  work_ntlmv2 = db.Column(db.String(80))
  work_password = db.Column(db.String(80))

  linkedin_url = db.Column(db.String(80))

  ctime = db.Column(DateTime, default=func.now())

def setup(app):
  print('!!! SETTING UP THE APP')
  try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rolodata.dat'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  except Exception as e:
    print("[-] DBURI invalid "+str(e))

  db = SQLAlchemy(app)

def init():
  db.create_all()

def search(query):
  people = []
  for person in People.query.all(): # TODO maybe limit by date at some point?
    print("NAME : "+person.first_name)
    print(asdict(person))
    people.append(asdict(person))

  return people

def new_person(new_data):
  new_person = People()

  for field in new_data.keys():
    print(field)
    #new_person.__table__.c[field] = new_data[field]
    setattr(new_person, field, new_data[field])

  #new_person.first_name = new_data['first_name']
  #new_person.last_name  = new_data['last_name']

  db.session.add(new_person)
  db.session.commit()
