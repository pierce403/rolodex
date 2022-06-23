import flask
from flask import render_template, redirect, request, Flask, g, send_from_directory, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy

import random, string, time

import os
import json
import sys
import traceback

import rolodata as rolodata

from datetime import datetime

app = Flask(__name__,static_url_path='/static')

app.jinja_env.add_extension('jinja2.ext.do')

import rolodata
rolodata.setup(app)

@app.before_first_request
def setup():
  print("[+] running setup")
  try:
    rolodata.init()
    print("[+] created people db")
  except:
    print("[+] people db already exists")

@app.route('/')
def test():
  return render_template("index.html")

@app.route('/testing')
def testing():
  new_person={}
  new_person['first_name'] = "HEY"
  new_person['last_name'] = "YOU"
  rolodata.new_person(new_person)
  return "hi"

@app.route('/dump')
def dump():
  return json.dumps(rolodata.search("hi"))

@app.route('/')
def home():
  return render_template("index.html")

@app.route('/search')
def search():
  query = request.args.get('q', '')
  page = int(request.args.get('p', 1))
  format = request.args.get('f', "")

  results_per_page = 20 # TODO maybe tweak as a premium feature?
  searchOffset = results_per_page * (page-1)
  count,context = rolodata.search(query,results_per_page,searchOffset)
  
  if not isinstance(count,int):
    count = count['value']

  next_url = url_for('search', q=query, p=page + 1) \
      if count > page * results_per_page else None
  prev_url = url_for('search', q=query, p=page - 1) \
      if page > 1 else None

  # what kind of output are we looking for?
  if format == 'hostlist':
    return render_template("hostlist.html",query=query, numresults=count, page=page, hosts=context)
  if format == 'json':
    return render_template("json.html",query=query, numresults=count, page=page, hosts=context)
  return render_template("search.html",query=query, numresults=count, page=page, hosts=context, next_url=next_url, prev_url=prev_url)

@app.route('/submit',methods=['POST'])
def submit():

  data = request.get_json()

  print("!!! SUBMITING DATA")
  newhost={}
  newhost=json.loads(data)
  if 'submit_token' not in newhost:
    return "no submit token supplied"

  try:
    newhost['ip'] = get_ip(newhost['nmap_data'])
    newhost['hostname'] = get_hostname(newhost['nmap_data'])
    newhost['ports'] = str(get_ports(newhost['nmap_data']))
    newhost['timestamp'] = datetime.now()
  except Exception as e:
    return "[!] Couldn't find necessary data: "+str(e)

  if len(newhost['ports']) == 2: # this is a string []
    return "[!] No open ports found!"
  
  if len(newhost['ports']) > 500:
    return "[!] More than 500 ports found. This is probably an IDS/IPS. We're going to throw the data out."

  try:
    print("[+] nmap successful and submitted for ip: "+str(newhost['ip'])+"\nhostname: "+str(newhost['hostname'])+"\nports: "+str(newhost['ports']))    

    print("submit token is "+str(newhost['submit_token']))
    newhost['user']=users.bump_user(str(newhost['submit_token']))
    del newhost['submit_token'] # make sure not to leak the submit tokens (anymore)

    nweb.newhost(newhost)

  except Exception as e:
    print("[EE] BAD SUBMISSION ERROR!!")
    print(e.__traceback__.tb_lineno)
    print(e)
    return "[-] bad submission data : "+str(e)

  #return str(newhost)
  return "[+] nmap successful and submitted for ip: "+str(newhost['ip'])+"\nhostname: "+str(newhost['hostname'])+"\nports: "+str(newhost['ports'])


