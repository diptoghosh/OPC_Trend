from datetime import datetime, timedelta
# from sqlalchemy import func
# from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler
import configparser, os, sys, logging

def get_config(filepath,section,key):
    config = configparser.ConfigParser()
    config.read(filepath,  encoding='utf-8')
    return config.get(section, key)

def offset_time(hours=0, minutes=0, seconds=0):
    return datetime.now() - timedelta(hours=hours, minutes=minutes, seconds=seconds)

def form_datetime_load(string, format):
    datetime.strptime(string.replace("T", " "), format)

def get_single_column_obj(tableClass, column):
    return getattr(tableClass, column)

# def get_column_objs(tableClass, columnList):
#     return [func.avg(getattr(tableClass, name)).label(name) for name in columnList]

# def flask_oracle(app):
#     DIALECT = get_config(app.config['CONFIG_FILE'], 'database', 'DIALECT') #'oracle'
#     SQL_DRIVER = get_config(app.config['CONFIG_FILE'], 'database', 'SQL_DRIVER') #'cx_oracle'
#     USERNAME = get_config(app.config['CONFIG_FILE'], 'database', 'USERNAME') #'RTDB' #enter your username
#     PASSWORD = get_config(app.config['CONFIG_FILE'], 'database', 'PASSWORD') #'RTDB' #enter your password
#     HOST = get_config(app.config['CONFIG_FILE'], 'database', 'HOST') #'10.182.52.80' #enter the oracle db host url
#     PORT = get_config(app.config['CONFIG_FILE'], 'database', 'PORT') #1521 # enter the oracle port number
#     SERVICE = get_config(app.config['CONFIG_FILE'], 'database', 'SERVICE') #'RTDB' # enter the oracle db service name

#     app.config['SQLALCHEMY_ECHO'] = False
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE
    
#     db = SQLAlchemy(app, session_options={"autoflush": False})
#     error = ""
#     status = False
#     try:
#         with app.app_context():
#             db.reflect()
#             db.engine.dialect._to_decimal = float   # type: ignore
#             status = True
#     except Exception as e:
#         error = str(e)
#     finally:
#         return db, status, error
    
    
# def get_database_status(db):
#     output = "Database connected"
#     is_database_working = True
#     try:
#         # to check database we will execute raw query
#         db.session.execute('SELECT 1 FROM DUAL')
#     except Exception as e:
#         output = str(e)
#         is_database_working = False

#     return is_database_working, output


def flask_startup():
    if getattr(sys, 'frozen', False):
        _working_directory = os.path.dirname(os.path.realpath(sys.executable))
        template_folder = os.path.join(sys._MEIPASS, 'templates')  # type: ignore
        static_folder = os.path.join(sys._MEIPASS, 'static')  # type: ignore
    else:
        _working_directory = os.path.dirname(os.path.realpath(__file__))
        _working_directory = os.path.dirname(_working_directory)
        template_folder = None
        static_folder = None
        
    return _working_directory, template_folder, static_folder


def logging_startup():
    log_formatter = logging.Formatter('{asctime}.{msecs:03.0f} | {funcName:^16s} | {lineno:04d} | {levelname:^9s} | {message}', style='{', datefmt="%Y-%m-%d %H:%M:%S")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_formatter)
    file_handler = RotatingFileHandler('trendLog.log', mode='a', maxBytes=5242880,   # Max log file size: 5 MB (5242880 B) (5*1024*1024)
                                    backupCount=10, encoding=None, delay=False)
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)

    Log = logging.getLogger('trend')
    Log.setLevel(logging.DEBUG)

    Log.addHandler(file_handler)
    Log.addHandler(console_handler)
    Log.info(f"Logging started...")
    return Log