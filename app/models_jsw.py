import os
from flask_sqlalchemy import SQLAlchemy
from app import app
#from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, request, url_for
from app.tools import get_config
import configparser



DIALECT = get_config(app.config['CONFIG_FILE'], 'database', 'DIALECT') #'oracle'
SQL_DRIVER = get_config(app.config['CONFIG_FILE'], 'database', 'SQL_DRIVER') #'cx_oracle'
USERNAME = get_config(app.config['CONFIG_FILE'], 'database', 'USERNAME') #'RTDB' #enter your username
PASSWORD = get_config(app.config['CONFIG_FILE'], 'database', 'PASSWORD') #'RTDB' #enter your password
HOST = get_config(app.config['CONFIG_FILE'], 'database', 'HOST') #'10.182.52.80' #enter the oracle db host url
PORT = get_config(app.config['CONFIG_FILE'], 'database', 'PORT') #1521 # enter the oracle port number
SERVICE = get_config(app.config['CONFIG_FILE'], 'database', 'SERVICE') #'RTDB' # enter the oracle db service name

app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = f'oracle+cx_oracle://RTDB:RTDB@10.182.52.80:1521/RTDB'
app.config['SQLALCHEMY_DATABASE_URI'] = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE
 
db = SQLAlchemy(app, session_options={"autoflush": False})

try:
    with app.app_context():
        a = 1
        db.reflect()
        db.engine.dialect._to_decimal = float   # type: ignore
        print("DB Session Created")

except Exception as e:
    print(f'error:{e}')


class MEAS_CONT_VALUE_TAB(db.Model):  # type: ignore
    __table__ = db.Model.metadata.tables['meas_cont_value_tab']  # type: ignore
    
    def __repr__(self):
         return f'<meas_cont_value_tab {self.coilidout}-{self.dtactual}-{self.nsample}>'
     
     
columnList = list()
index = 1
config = configparser.ConfigParser()
config.read(app.config['CONFIG_FILE'], encoding='utf-8')
databaseColumnList = dict(MEAS_CONT_VALUE_TAB.__table__.c)

app.config['DB_COL_AVAILABLE'] = True
db_columns = list()
for item in dict(config.items('column')):
    if dict(config.items('column'))[item] not in databaseColumnList:
        app.config['DB_COL_AVAILABLE'] = False
        print(f"'{item}' column not available in database")
    else:
        db_columns.append(dict(config.items('column'))[item])
if app.config['DB_COL_AVAILABLE']:
    print(f"All columns available in database")
    app.config['DB_COLUMNS'] = db_columns