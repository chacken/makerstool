import os
from datetime import datetime
from datetime import timedelta
from flask import abort
from flask import Flask
from flask import g
from flask import redirect
from flask import url_for
#from rethinkdb.errors import RqlRuntimeError
#from rethinkdb.errors import RqlDriverError
#from flask.ext.jasmine import Jasmine
from flask.ext.assets import Environment
from webassets.filter import Filter
from webassets.filter import register_filter
from webassets.loaders import YAMLLoader

from makers.models import db
from makers.lib.user_session import determine_user


def create_app(config_filename):
  app = Flask(__name__)

  app.config.from_pyfile(config_filename)
  configure_views(app)
  configure_application(app)
  configure_static_assets(app)
  configure_context(app)
  #configure_tests(app)

  return app

def configure_views(app):
  from makers.views.sessions import sessions
  from makers.views.users import users
  from makers.views.projects import projects
  from makers.views.client_view import client_view

  app.register_blueprint(client_view)
  app.register_blueprint(sessions, url_prefix='/session')
  app.register_blueprint(users, url_prefix='/users')
  app.register_blueprint(projects, url_prefix='/projects')
  #app.register_blueprint(client_view, url_prefix='/client')


  @app.route('/')
  def index():
    if g.user:
      #if g.user.flags['firstLogin'] == True:
      #  
      return redirect(url_for('client_view.index'))
    else:
      # TODO: remove... don't think I need this due to app.before_request(determine_user)
      return redirect(url_for('sessions.login'))

def setup_db(app):
  pass
  #g.db = MongoEngine(app)
  #try:
  #  g.db.db_create(app.config['APP_DB']).run(connection)
  #  g.db(app.config['APP_DB']).table_create('todos').run(connection)
  #  print('Database setup completed. Now run the app without --setup.')
  #except RqlRuntimeError:
  #  print('App database already exists. Run the app without --setup.')
  #finally:
  #  connection.close()


def configure_application(app):
  @app.before_request
  def before_request():
    db.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=30)
    #g.db = MongoEngine(app) or abort(503, "No database connection could be established.")
  
  @app.before_request
  def bind_configuration():
    g.config = app.config
  app.before_request(determine_user)

  @app.teardown_request
  def teardown_request(exception):
    pass
    #try:
    #  db.disconnect()
    #  print("disconnected")
    #except AttributeError:
    #  print("this doesn't work")
    #  pass


def configure_static_assets(app):

  loader = YAMLLoader('assets.yaml')
  assets = Environment(app)
  assets.manifest = None
  assets.cache = False
  assets.directory = './makers'
  assets.url = ''

  for name, bundle in loader.load_bundles().items():
    assets.register(name, bundle)

  app.environment = assets

def configure_context(app):
  import locale
  locale.setlocale(locale.LC_ALL, '')

  def cents(c):
    return locale.currency(float(c) / 100, grouping=True)

  @app.context_processor
  def add_contexts():
    return {
      'cents':  cents
    }

# def configure_tests(app):
#   jasmine = Jasmine(app)
#   jasmine.sources(
#     'gen/dashboard_lib.js',
#     'gen/templates.js',
#     'gen/dashboard.js',
#     'lib/js/sinon-1.3.1.js',
#   )
#   jasmine.specs(
#     'test/confirm_spec.js',
#     'test/models/advertisers_spec.js',
#     'test/views/campaigns_spec.js',
#   )
# 

class TemplateFilter(Filter):
  name = 'template'

  def input(self, _in, out, source_path, output_path, **kwargs):
    (part, name_with_ex) = source_path.split(os.path.sep)[-2:]
    name = '%s/%s' % (part, name_with_ex.split('.')[0])
    out.write("window.JST['%s'] = template('%s');" % (
      name,
      _in.read().replace('\n', '\\n').replace("'", r"\'")))

#class TemplateFilter(Filter):
#  name = 'template'
#
#  def input(self, _in, out, source_path, output_path, **kwargs):
#    print(source_path)
#    (part, name_with_ex) = source_path.split(os.path.sep)[-2:]
#    name = '%s/%s' % (part, name_with_ex.split('.')[0])
#    out.write("window.JST['%s'] = ECT().render('%s','%s');" % (
#      name,
#      _in.read().replace('\n', '\\n').replace("'", r"\'")))

register_filter(TemplateFilter)


