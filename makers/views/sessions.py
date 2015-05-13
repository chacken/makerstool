from pprint import pprint
import json
import random
import string
import httplib2
import wtforms as wtf

from flask import Blueprint
from flask import abort
from flask import g
from flask import make_response
from flask import render_template
from flask import request
from flask import session
from flask import jsonify
#from googleapiclient import discovery
from oauth2client import client
from oauth2client.crypt import AppIdentityError
from urllib.parse import urlencode

from makers.lib.analytics import google_auth
from makers.lib.analytics import sync_analytics
from makers.lib.rest_api import form_error
from makers.lib.rest_api import rest_view
from makers.lib.user_session import login as login_user
from makers.lib.user_session import login_required
from makers.lib.user_session import logout as logout_user
from makers.models import User

sessions = Blueprint('sessions', __name__)

class AccountForm(wtf.Form):
  email = wtf.TextField('Email', [
    wtf.validators.Email(),
    wtf.validators.Required()
  ])

class LoginForm(wtf.Form):
  """
  A self-validating login form. This will require present and valid fields as
  well as query the datastore to ensure the user is properly authenticated. If
  the user has ented valid fields, but is not authenticated, this will attach
  the error to the password field.
  """
  email = wtf.TextField('Email', [
    wtf.validators.Email(),
    wtf.validators.Required()
  ])

  password = wtf.PasswordField('Password', [
    wtf.validators.Required()
  ])

  def validate_password(self, field):
    user = User.authenticate(self.email.data, self.password.data)
    if user is None:
      raise wtf.ValidationError('Invalid Login')

    self.user = user


@sessions.route('/login', methods=['GET', 'POST'])
def login():
  # Create a state token to prevent request forgery.
  # Store it in the session for later validation.
  csrf = ''.join(random.choice(string.ascii_uppercase + string.digits)
                  for x in range(32))
  session['_csrf_token'] = csrf
  # Set the Client ID, Token State, and Application Name in the HTML while
  # serving it.
  form = LoginForm(request.form)
  #if request.method == 'POST' and form.validate():
  #  user = form.user
  #  if user:
  #    return login_user(user)

  return render_template('sessions/login.html',
      form=form,
      csrf=csrf,
      login_redirect=g.config['SYNC_REDIRECT'],
      client_id=g.config['CLIENT_ID'])

@sessions.route('/analytics')
@google_auth
@login_required
def analytics():
  sync_analytics()
  return jsonify(response='success')

@sessions.route('/sync')
@login_required
def sync():
  return render_template('sessions/sync.html',
      login_redirect=g.config['LOGIN_REDIRECT'])

@sessions.route('/logout')
def logout():
  return logout_user(g.user)


@sessions.route('/', methods=['POST'])
@rest_view
@login_required
def create(data):
  form = AccountForm(data)

  if form.validate():
    user = User(**form.data)
    user.put()
    return user

  return form_error(form)

@sessions.route('/<id>', methods=['PUT'])
@rest_view
@login_required
def update(id, data):
  user = User.get(id) or abort(404)
  form = AccountForm(data, obj=user)

  if form.validate():
    form.populate_obj(user)
    user.put()
    return user

  return form_error(form)

@sessions.route('/<id>', methods=['DELETE'])
@rest_view
@login_required
def delete(id):
  user = User.get(id) or abort(404)
  user.delete()
  return user


