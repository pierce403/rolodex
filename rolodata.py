from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Table, Column, Float, Integer, String, DateTime, MetaData, ForeignKey, func
from sqlalchemy import bindparam
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

  personal_email:str = db.Column(db.String(80))
  work_email:str  = db.Column(db.String(80))

  work_ntlm:str = db.Column(db.String(80))
  work_ntlmv2:str = db.Column(db.String(80))
  work_roast:str = db.Column(db.String(80))
  work_password:str = db.Column(db.String(80))

  domain_admin:bool = db.Column(db.Boolean)
  been_pwned:bool = db.Column(db.Boolean)

  linkedin_url:str = db.Column(db.String(80))
  twitter_url:str = db.Column(db.String(80))
  facebook_url:str = db.Column(db.String(80))

  # bloodhound stuff
  ad_name: str = db.Column(db.String(80))
  ad_email: str = db.Column(db.String(80))
  ad_enabled: str = db.Column(db.String(80))
  ad_title: str = db.Column(db.String(80))
  ad_displayname: str = db.Column(db.String(80))
  ad_ntlm: str = db.Column(db.String(80))
  ad_ntlmv2: str = db.Column(db.String(80))
  ad_password: str = db.Column(db.String(80))

  ctime = db.Column(DateTime, default=func.now())

def setup(app):
  print('!!! SETTING UP THE APP')
  try:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rolodata.dat'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
  except Exception as e:
    print("[-] DBURI invalid "+str(e))

  db = SQLAlchemy(app)
  migrate = Migrate(app,db)

def init():
  db.create_all()

def search(query):
  people = []
  for person in People.query.all(): # TODO maybe limit by date at some point?
    print("NAME : "+str(person.first_name))
    print(asdict(person))
    people.append(asdict(person))

  return people

def update_person(index, new_data):
  target_person = People.query.first() # TODO actually do the search

  for field in new_data.keys():
    #print(field)
    #new_person.__table__.c[field] = new_data[field]
    setattr(target_person, field, new_data[field])

  db.session.commit()
  return True


def new_person(new_data):
  new_person = People()

  for field in new_data.keys():
    #print(field)
    #new_person.__table__.c[field] = new_data[field]
    setattr(new_person, field, new_data[field])

  db.session.add(new_person)
  return True

def commit():
  print("[+] COMMITTED "+str(db.session.commit()))

def bulk_update(update_data):
  stmt = People.__table__.update().where(People.__table__.c.id == bindparam('ad_name')).values({
        'ad_name': bindparam('ad_name'),
        'ad_ntlm': bindparam('ad_ntlm'),
    })
  retval = db.engine.execute(stmt,update_data)
  print(retval)

def update_hash(name, ntlm):
  num_rows_updated = People.query.filter_by(ad_name=name).update(dict(ad_ntlm=ntlm))
  #print("UPDATED: "+str(num_rows_updated))
  #db.session.commit()

def update_crack(ntlm, password):
  num_rows_updated = People.query.filter_by(ad_ntlm=ntlm).update(dict(ad_password=password))
  #db.session.commit()


