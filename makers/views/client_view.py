from pprint import pprint
#from datetime import datetime
from datetime import timedelta
from flask import Blueprint
from flask import g
from flask import json
from flask import redirect
from flask import render_template
from flask import url_for


from googleapiclient.errors import HttpError as GHttpError
#from makers.lib.stripe_api import stripe
from makers.lib.analytics import google_auth
from makers.lib.analytics import sync_analytics
from makers.lib.user_session import login_required
from makers.models import Project


client_view = Blueprint('client_view', __name__)
DEFAULT_RANGE = timedelta(hours=(7 * 24))

@client_view.route('/')
@login_required
def index():
  return redirect(url_for('.dashboard'))

@client_view.route('/syncing')
@login_required
@google_auth
def syncing():
  update_projects()
  return 

@client_view.route('/dashboard')
@login_required
@google_auth
def dashboard():
  user = g.user
  # TODO: do this while starting a session
  #sync_analytics()

  accounts_json = json.dumps([p.dict() for p in g.user.accounts])
  mediums_json = json.dumps([p.dict() for p in []])

  return render_template('client_view/home.html',
           mediums_json = mediums_json,
           projects_json = accounts_json,
           user = user)

@client_view.route('/account')
@login_required
def account():
  return redirect(url_for('.billing'))

#@client_view.route('/account/billing')
#@login_required
#def billing():
#  user = g.user
#  customer = stripe.Customer.retrieve(user.customer_id)
#  charges = customer.charges()
#  charges_json = charges
#  return render_template('client_view/billing.html',
#           charges_json = charges_json,
#           user = user)

@client_view.route('/account/users')
@login_required
def users():
  user = g.user
  users = user.account.user_account_set

  users_json = json.dumps([u.dict() for u in users])

  return render_template('client_view/users.html',
           users_json = users_json,
           user = user)




