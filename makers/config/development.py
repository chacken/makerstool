import os
DEBUG = True
SECRET_KEY = '91449607900ecb9513bdac560bda5cbc'
AUTH_SCOPE = 'https://www.googleapis.com/auth/analytics https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
CLIENT_ID = '663782627784-nkh1jbfiqk1fbnk11grlrjl1jq9v1mf4.apps.googleusercontent.com'
CLIENT_SECRET = 'mJQqkpgD_RnGObCcDpkBxUdO'

SYNC_REDIRECT = 'http://dev.makerstool.com:5000/session/sync'
LOGIN_REDIRECT = 'http://dev.makerstool.com:5000/'

MONGODB_SETTINGS = {
  'db':   'test',
  'host': 'mongodb',
  'port': 27017
}

RDB_HOST = os.environ.get('RDB_HOST') or 'rethinkdb'
RDB_PORT = os.environ.get('RDB_PORT') or 28015
