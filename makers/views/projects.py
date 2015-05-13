from pprint import pprint
import json
import string
import random
import httplib2
import wtforms as wtf
import string
from random import choice

from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import abort
from flask import g
from flask import make_response
from flask import request
from flask import Response
from flask import render_template
from flask import session
from googleapiclient import discovery
from oauth2client import client
from oauth2client.crypt import AppIdentityError
from urllib.parse import urlencode

#from flask.ext.triangle import Form
#from flask.ext.triangle.widgets.standard import TextInput
from makers.lib.rest_api import form_error
from makers.lib.rest_api import rest_view
from makers.lib.analytics import google_auth
from makers.lib.user_session import login as login_user
from makers.lib.user_session import login_required
from makers.lib.user_session import logout as logout_user
from makers.models import User
from makers.models import Project
from makers.models import Medium
from makers.models import DataPoint


projects = Blueprint('projects', __name__)

#class SelectProjectForm(Form):
#  id   = TextInput('project.id', required=True)
#  name = TextInput('project.name', required=False)

@projects.route('/<id>/trends', methods=['GET'])
@login_required
@google_auth
def trends(id):
  project = Project.get(id=id) or abort(404)
  accounts_json = json.dumps([a.dict() for a in g.user.accounts])
  project_json = json.dumps(project.dict())
  medium = Medium.objects(project=project, type="trends").first()
  medium_dict = {}
  if medium is not None:
    medium_dict = medium.dict()
    date = datetime.today()-timedelta(days=1)
    pprint(date)
    medium_dict['datapoints'] = [dp.dict(diff=date-timedelta(days=1)) for dp in
DataPoint.objects(medium=medium, date=datetime(date.year,date.month,date.day))]
  medium_json = json.dumps(medium_dict)

  return render_template('projects/overview.html',
           user=g.user,
           mediums_json=medium_json,
           project_json=project_json,
           projects_json=accounts_json)

@projects.route('/<id>', methods=['GET'])
@login_required
@google_auth
def view(id):
  project = Project.get(id=id) or abort(404)
  mediums = Medium.objects(project=project)

  accounts_json = json.dumps([a.dict() for a in g.user.accounts])
  mediums_json = json.dumps([m.dict() for m in mediums])

  project_json = json.dumps(project.dict())

  ## Do this at the beginning of a session.. store in cache/database
  #data = None
  #data = g.service.data().ga().get(
  #  ids='ga:'+project.id,
  #  start_date='30daysAgo',
  #  end_date='today',
  #  metrics='ga:visits',
  #  dimensions='ga:source,ga:keyword',
  #  sort='-ga:visits',
  #  filters='ga:medium==referral',
  #  start_index='1',
  #  max_results='25').execute()
  #pprint(data.get('rows'))
  #results = json.dumps(data.get('rows'))

  return render_template('projects/overview.html',
           user=g.user,
           mediums_json=mediums_json,
           project_json=project_json,
           projects_json = accounts_json)

@projects.route('/save/<id>', methods=['PUT'])
@login_required
@google_auth
def save(id):
  project = Project.objects.get(id=id) or abort(404)
  project.update(set__saved=True)
  return

################
#### (I THINK) everything below this needs to be removed/updated
###############
@projects.route('/pull', methods=['GET'])
@login_required
@google_auth
def pull():
  accounts = g.service.management().accounts().list().execute()
  #accounts_json = json.dumps(accounts.get('items'))
  accounts_json = accounts.get('items')
  print(accounts_json)
  return accounts_json


@projects.route('/create', methods=['GET'])
@login_required
@google_auth
def create():
  accounts = g.service.management().accounts().list().execute()
  #accounts_json = json.dumps(accounts.get('items'))
  accounts_json = accounts.get('items')
  print(accounts_json)
  return render_template('projects/create.html',
           user=g.user,
           accounts=accounts_json)

@projects.route('/<id>', methods=['PUT'])
@rest_view
@login_required
def update(id, data):
  project = Project.objects.get(id=id) or abort(404)

@projects.route('/<id>', methods=['DELETE'])
@rest_view
@login_required
def delete(id):
  project = Project.objects.get(id=id) or abort(404)
  project.delete()
  return project


