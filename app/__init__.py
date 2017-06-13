from flask import Flask

app = Flask(__name__, static_url_path = "", static_folder = "tmp/")

app.config.from_object('config')
app.config['STATIC_FOLDER'] = 'tmp'