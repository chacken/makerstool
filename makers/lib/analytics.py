from pprint import pprint
import httplib2
from datetime import datetime
from datetime import timedelta
from flask import g
from flask import Response
from flask import json
from flask import request
from functools import wraps
from time import sleep
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.client import OAuth2Credentials
from oauth2client import GOOGLE_TOKEN_URI

from werkzeug.datastructures import MultiDict

from makers.models import Account
from makers.models import WebProperty
from makers.models import Project
from makers.models import Medium
from makers.models import DataPoint
from makers.lib import day
from makers.lib import today
from makers.lib import yesterday

def gapi_backoff(query):
  # TODO: fix this?.. each query waits 15 seconds before quitting
  # if multiple queries are stacked/waiting... we might run into problems
  # b.c. browser timeouts default to around 30 seconds

  for n in range(0, 4):
    try:
      return query.execute()
    except HttpError as e:
      error = json.loads(e.content)
      sleep(2 ** n)

  return None #gave up




def sync_analytics():
  accounts = sync_accounts()
  for act in g.user.accounts:
    for wp in act.webproperties:
      for project in wp.projects:
        _trends(project)
        #_projections(project)
        #_ltv(project)
  
  return accounts
  #project.update(add_to_set__groups__owners=[g.user.id])

def remove_matching_values_from_list(l1, l2):
   return [val for val in l1 if val not in l2]

def _trends(project):
  trend = Medium.objects(project=project,type="trends").first()
  if trend is None:
    pprint('CREATE MEDIUM')
    trend = Medium(name='Trends',type='trends',project=project)
    trend.save()


  latest_dp = DataPoint.objects(medium=trend).order_by('-date').first()
  latest_date = datetime.today().date() - timedelta(days=5)
  if latest_dp != None and (latest_dp.date.date() > latest_date):
    latest_date = latest_dp.date.date()

  while latest_date <= today:
    l1 = []
    l2 = []
    d = latest_date
    data = gapi_backoff(g.service.data().ga().get(
      ids='ga:'+project.id,
      start_date=latest_date.strftime('%Y-%m-%d'),
      end_date=latest_date.strftime('%Y-%m-%d'),
      metrics='ga:visits',
      dimensions='ga:source',
      sort='-ga:visits',
      filters='ga:medium==referral',
      start_index='1'))

    if data.get('rows', []):
      for item in data.get('rows'):
        dp_data = {}
        dp_data['source'] = item[0]
        dp_data['visits'] = item[1]
        dp = DataPoint(medium=trend,data=dp_data,type='trend',date=datetime(d.year,d.month,d.day))
        dp.save()
        l2.append(item[0])
    else:
      print('No Rows Found')


    existing_dps = DataPoint.objects(medium=trend)
    for dp in existing_dps:
      l1.append(dp.data['source'])
    ##today_dps = DataPoint.objects(medium=trend,date=datetime.today().date())
    es = list(set(l1)-set(l2))
    for e in es:
      tmp_data={}
      tmp_data['source']=e
      tmp_data['visits']=0
      DataPoint(medium=trend,date=datetime(d.year,d.month,d.day),type='trend',data=tmp_data).save()


    latest_date += timedelta(days=1)


  #pprint(project)
  #pprint(existing_dps)
  #pprint(today_dps)

  return


def sync_accounts():
  return _accounts()
  #project.update(add_to_set__groups__owners=[g.user.id])

def _accounts():
  g_accounts = gapi_backoff(g.service.management().accounts().list())
  accounts = []
  if isinstance(g_accounts, dict):
    g_accounts = g_accounts.get('items', [])
    for g_account in g_accounts:
      account = Account.get(id=g_account['id'])

      if not account:
        account = Account()
        setattr(account, 'is_new', True)
      account.dict_to_attr(g_account)
      account.webproperties = _webproperties(account.id)
      account.updated = datetime.now()
      account.save()
      accounts.append(account)

      if getattr(account, 'is_new', False):
        g.user.update(add_to_set__accounts=[account])

  return accounts

def _webproperties(account_id):
  g_properties = gapi_backoff(g.service.management().webproperties().list(
      accountId=account_id
    ))
  properties = []
  if isinstance(g_properties, dict):
    g_properties = g_properties.get('items', [])
    for g_property in g_properties:
      property = WebProperty.get(id=g_property['id'])

      if not property:
        property = WebProperty()
      property.dict_to_attr(g_property)
      property.projects = _projects(account_id, property.id)
      property.updated = datetime.now()
      property.save()
      properties.append(property)

  return properties

def _projects(account_id, webproperty_id):
  profiles = gapi_backoff(g.service.management().profiles().list(
    accountId=account_id,
    webPropertyId=webproperty_id
    ))
  projects = []
  if isinstance(profiles, dict):
    profiles = profiles.get('items', [])
    for profile in profiles:
      project = Project.get(id=profile['id'])
      if not project:
        project = Project()
      project.dict_to_attr(profile)
      project.updated = datetime.now()
      project.save()
      projects.append(project)

  return projects



def google_auth(func):
  @wraps(func)
  def view_wrapper(*args, **kwargs):
    print(g.user.email)
    if not getattr(g, 'user', None):
      print("no user")
    if not g.user.refresh_token:
      # TODO: get one
      return false
    if not getattr(g, 'credentials', None):
      print(g.user.refresh_token)
      g.credentials = OAuth2Credentials(None,
                 g.config['CLIENT_ID'],
                 g.config['CLIENT_SECRET'],
                 g.user.refresh_token,
                 None,
                 #g.user.token_expiry,
                 GOOGLE_TOKEN_URI,
                 None)
    pprint(g.credentials)
    #credentials.refresh(http = httplib2.Http()) #does this in authorize()
    http = g.credentials.authorize(http = httplib2.Http())
    g.service = discovery.build('analytics', 'v3', http=http)
    return func(*args, **kwargs)
  return view_wrapper


def force_authentication():
 # TODO: redirect to an auth page
 # remove force from sessions/login.html
 return None



def get_ltvs(project):
  return
  #data = None
  #try:
  #  data = g.service.data().ga().get(
  #    ids='ga:36107208',
  #    start_date='7daysAgo',
  #    end_date='today',
  #    metrics='ga:visits',
  #    dimensions='ga:source,ga:keyword',
  #    sort='-ga:visits',
  #    filters='ga:medium==organic',
  #    start_index='1',
  #    max_results='25').execute()
  #except GHttpError as error:
  #  print(error)


  #query = data.get('query')
  #pprint(query)
  #keys = query.keys()
  #for key in keys:
  #  pprint(query[key])






