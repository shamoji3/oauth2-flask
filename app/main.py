import json, requests, secrets
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from user import User

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = secrets.token_urlsafe(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

GOOGLE_CLIENT_ID     = app.config['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SEC    = app.config['GOOGLE_CLIENT_SEC']
GOOGLE_DISCOVERY_URL = (
  "https://accounts.google.com/.well-known/openid-configuration"
)
## global value as temporary user db
CURRENT_USERS = list()

client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
  return requests.get(GOOGLE_DISCOVERY_URL).json()

@login_manager.user_loader
def load_user(uid:str):
  for user in CURRENT_USERS:
    if uid == user.uid:
      return user
  return User

@app.route("/")
def index():
  if current_user.is_authenticated:
    return (
      "<p>{} ({})</p>"
      '<div><img src="{}" alt="Google profile pic"></img></div>'
      '<a class="button" href="/logout">Logout</a>'.format(
        current_user.name, current_user.email, current_user.picture
      )
    )
  else:
      return '<a class="button" href="/login">Google Login</a>'

@app.route("/login")
def login():
  google_provider_cfg    = get_google_provider_cfg()
  authorization_endpoint = google_provider_cfg["authorization_endpoint"]
  request_uri = client.prepare_request_uri(
    authorization_endpoint,
    redirect_uri=request.base_url + "/callback",
    scope=["openid", "email", "profile"],
  )
  return redirect(request_uri)

@app.route("/login/callback")
def callback():
  code = request.args.get("code")
  google_provider_cfg = get_google_provider_cfg()
  token_endpoint      = google_provider_cfg["token_endpoint"]
  token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code,
  )
  token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SEC),
  )
  client.parse_request_body_response(json.dumps(token_response.json()))

  userinfo_endpoint  = google_provider_cfg["userinfo_endpoint"]
  uri, headers, body = client.add_token(userinfo_endpoint)
  userinfo_response  = requests.get(uri, headers=headers, data=body)

  if userinfo_response.json().get("email_verified"):
    user_id      = userinfo_response.json()["sub"]
    user_name    = userinfo_response.json()["given_name"]
    user_email   = userinfo_response.json()["email"]
    user_picture = userinfo_response.json()["picture"]
  else:
    return "User is not verified.", 400

  user = User.instaniate(uid=user_id, name=user_name, email=user_email, picture=user_picture)
  login_user(user)
  CURRENT_USERS.append(user)
  return redirect(url_for("index"))

@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in.", 403

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("index"))

if __name__ == "__main__":
  app.run(debug=True, ssl_context="adhoc")