from os      import environ
from os.path import join, dirname
from dotenv  import load_dotenv

#### load shell env
env = join(dirname(__file__), ".env")
load_dotenv(env)

#### shell env as a value
if 'APP_ENV' in environ:
  APP_ENV = environ['APP_ENV']
else:
  APP_ENV = "undefined"

GOOGLE_CLIENT_ID  = environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SEC = environ['GOOGLE_CLIENT_SEC']