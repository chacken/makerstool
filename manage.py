from flask.ext.assets import ManageAssets
from flask.ext.script import Manager

from makers import create_app

app = create_app('config/development.py')
manager = Manager(app)

manager.add_command("assets", ManageAssets(app.environment))

if __name__ == '__main__':
  manager.run()

