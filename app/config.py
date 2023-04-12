from os      import environ
from os.path import join, dirname
from dotenv  import load_dotenv

#### load .env
env = join(dirname(__file__), ".env")
load_dotenv(env)

#### Reads shell variables (returns None if not defined)
APP_ENV           = environ.get('APP_ENV')
GOOGLE_CLIENT_ID  = environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SEC = environ.get('GOOGLE_CLIENT_SEC')