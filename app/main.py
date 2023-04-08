from flask  import Flask

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    content = '''
    Hello World.
    '''
    return content

if __name__ == "__main__" and app.config['APP_ENV']== "development":
    app.run(host='0.0.0.0')