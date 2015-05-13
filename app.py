import argparse
import os
import sys

from makers import create_app
from makers import setup_db


def main(args=sys.argv):
  #os.environ['BOTO_CONFIG'] = 'config/boto.cfg'
  app = create_app('config/development.py')
  port = int(os.environ.get("PORT", 5000))

  parser = argparse.ArgumentParser(description='Run the Makers app')
  parser.add_argument('--setup', dest='run_setup', action='store_true')

  args = parser.parse_args()
  if args.run_setup:
    setup_db(app)
  else:
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
  sys.exit(main(sys.argv))


#from flask import Flask
#from redis import Redis
#import os
#app = Flask(__name__)
#redis = Redis(host='redis', port=6379)
#
#if __name__ == "__main__":
#    app.run(host="0.0.0.0", debug=True)
