from pprint import pprint
import json
import string
import random
import httplib2
import wtforms as wtf
import string
from random import choice

from flask import Blueprint
from flask import abort
from flask import g
from flask import make_response
from flask import request
from flask import Response
from flask import session
from googleapiclient import discovery
from oauth2client import client
from oauth2client.crypt import AppIdentityError
from urllib.parse import urlencode

from makers.lib.rest_api import form_error
from makers.lib.rest_api import rest_view
from makers.lib.user_session import login as login_user
from makers.lib.user_session import login_required
from makers.lib.user_session import logout as logout_user
from makers.models import User


users = Blueprint('users', __name__)

class UserForm(wtf.Form):

  first_name = wtf.TextField('First Name', [
    wtf.validators.Required()
  ])
  last_name = wtf.TextField('Last Name', [
    wtf.validators.Required()
  ])

  active = wtf.BooleanField('Active')
  admin = wtf.BooleanField('Active')
  email = wtf.TextField('Email', [
    wtf.validators.Email("Invalid Email Format"),
    wtf.validators.Required()
  ])

  #def validate_email(form, field):
  #  print form.data
  #  for user in g.user.account.user_account_set:
  #    if user.email == field.data.lower():
  #      # need to check if user is the one we're editing
  #      raise ValueError("Email already in use.")

@users.route('/')
@rest_view
@login_required
def list():
  return #g.user.account.user_account_set

@users.route('/authenticate', methods=['POST'])
def authenticate():
  response_data = dict()
  code = request.data.decode('utf-8')

  csrf=request.args.get('_csrf_token', None) or abort(404)
  if csrf != session['_csrf_token']:
    return Response('Invalid state Parameter', status=401, content_type='application/json')

  if 'error' in request.args:
    return Response(json.dumps(dict(error=request.args['error'])),
          status=400,
          content_type='application/json')

  h = httplib2.Http()
  credentials = client.credentials_from_code(g.config['CLIENT_ID'],
        g.config['CLIENT_SECRET'],
        g.config['AUTH_SCOPE'],
        code,
        http=h)
  #pprint(credentials.refresh_token)
  h = credentials.authorize(http=h)

  service = discovery.build('plus', 'v1', http=h)
  person = None
  try:
    person = service.people().get(userId='me').execute()
  except client.AccessTokenRefreshError:
    return make_response('The credentials have been revoked or expired.',400)

  #pprint(person)
  try:
    user = User.objects.get(id=person['id'])
    # TODO: update if changed
    #pprint(user)
  except User.DoesNotExist:
    user = User(id=person['id'],
          given_name=person['name']['givenName'],
          family_name=person['name']['familyName'],
          display_name=person['displayName'],
          flags=dict(firstLogin=True))
    for email in person['emails']:
      if email['type'] == 'account':
        user.email = email['value']

  refresh_token = getattr(credentials, 'refresh_token', None)
  if refresh_token != None:
    user.refresh_token = refresh_token

  user.save()

  if user:
    #pprint(user.dict())
    login_user(user, redirect=False)

  # TODO: check for errors or something, respond with 400

  response = make_response(json.dumps(dict(user=user.dict()), 200))
  response.headers['Content-Type'] = 'application/json'
  return response



#@users.route('/', methods=['POST'])
#@rest_view
##@login_required
#def create(data):
#  form = UserForm(data)
#
#  if form.validate():
#    account = Account().put()
#    password = ''.join([choice(string.letters + string.digits) for i in range(9)])
#    user = User(account=account, **form.data)
#    user.set_password(password)
#    user.put()
#    session['user'] = str(user.id)
#    session['account'] = str(user.account.id)
#    session.modified = True
#    #g.user = user
#    return user
#
#  return form_error(form)

#@users.route('/login', methods=['POST'])
#@rest_view
#def login(data):
#  print data
#  
#  result = False
#  return result

@users.route('/<id>', methods=['PUT'])
@rest_view
@login_required
def update(id, data):
  user = User.objects.get(id=id) or abort(404)
  form = UserForm(data, obj=user)

  if form.validate():
    form.populate_obj(user)
    user.put()
    return user

  return form_error(form)

@users.route('/<id>', methods=['DELETE'])
@rest_view
@login_required
def delete(id):
  user = User.objects.get(id=id) or abort(404)
  user.delete()
  return user


