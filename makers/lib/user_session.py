from datetime import datetime

from flask import g
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from functools import wraps

from makers.models import User


def determine_user():
  session.permanent = True
  if 'user' in session:
    # this looks fugly, ensure the user in session actually exists
    try:
      g.user = User.objects.get(id=session['user'])
    except:
      # TODO: log this, because it shouldn't happen
      g.user = None
      session.pop('user')
  else:
    g.user = None

def login_required(func):
  """
  Wraps a function to ensure it is only viewable by logged in users. If a user
  isn't logged it, they should be redirected to the login page with an
  acceptable error message
  """
  @wraps(func)
  def view_wrapper(*args, **kwargs):
    if g.user is None:
      return redirect(url_for('sessions.login', next=request.path))
    return func(*args, **kwargs)

  return view_wrapper

def login(user, redirect=True):
  session['user'] = str(user.id)
  user.last_login = datetime.now()
  user.save()
  if redirect==False:
    g.user = user
    return
  if request.args.get('next'):
    print("testttttttttttttttttttttttttttttttttttttttttt")
    return redirect(request.args['next'])
  else:
    return redirect('/')

def logout(user):
  if 'user' in session:
    session.pop('user')
  if '_flashes' in session:
    session.pop('_flashes')
  g.user = None

  session.modified = True

  return redirect('/')


