#from build import _working_directory
from flask import Flask
from config import Config
from app.tools import get_config
import os
from app.tools import flask_startup, logging_startup

# logging framework loading
Log = logging_startup()

# app folder loading
_working_directory, template_folder, static_folder = flask_startup()
if(template_folder==None or static_folder==None):
    app = Flask(__name__)
else:
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)



#app = Flask(__name__)

# app configuration loading
app.config.from_object(Config)
app.config['CONFIG_FILE'] = os.path.join(_working_directory, 'config.ini')
Log.info(f"Loading config from: {app.config['CONFIG_FILE']}")
app.config['shutdown'] = False
app.config['SAMPLING_RATE'] = float(get_config(app.config['CONFIG_FILE'], 'trend', 'SAMPLING_RATE'))
Log.info(f"SAMPLING_RATE: {app.config['SAMPLING_RATE']}")


from app import routes, models
