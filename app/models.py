import redis, os
from app import app, Log
from app.tools import get_config

try:
    redis_host = get_config(app.config['CONFIG_FILE'], 'connection', 'REDIS_HOST')
except:
    Log.warning(f"Failed to read REDIS_HOST from config:{app.config['CONFIG_FILE']}")
    redis_host = 'localhost'

try:
    redis_port = int(get_config(app.config['CONFIG_FILE'], 'connection', 'REDIS_PORT'))
except:
    Log.warning(f"Failed to read REDIS_PORT from config:{app.config['CONFIG_FILE']}")
    redis_port = 6379
    
try:
    ARCHIVE_LOCATION = get_config(app.config['CONFIG_FILE'], 'data', 'ARCHIVE_LOCATION')
    if not os.path.exists(ARCHIVE_LOCATION):
        ARCHIVE_LOCATION = './'
except:
    Log.warning(f"Failed to read ARCHIVE_LOCATION from config:{app.config['CONFIG_FILE']}")
    ARCHIVE_LOCATION = './'

try:
    MAX_CHART_COUNT = int(get_config(app.config['CONFIG_FILE'], 'trend', 'MAX_CHART_COUNT'))
except:
    Log.warning(f"Failed to read MAX_CHART_COUNT from config:{app.config['CONFIG_FILE']}")
    MAX_CHART_COUNT = 12
    
Log.debug(f"Archive Location:{ARCHIVE_LOCATION}")
Log.debug(f"Creating redis connection with Host:{redis_host}, Port:{redis_port}")
RCLIENT = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses = True)
TAG_MAP = RCLIENT.hgetall('tagdb')
TAG_ADDRESS = RCLIENT.hgetall('tagdb_addr')
signal_list =list()
for signal in TAG_ADDRESS:
    signal_list.append(TAG_ADDRESS[signal])
app.config['DB_COLUMNS'] = signal_list

def map_tag(tagdict):
    retdict = dict()
    for key in tagdict:
        if key in TAG_ADDRESS:
            retdict[TAG_ADDRESS[key]] = tagdict[key]
        else:
            retdict[key] = tagdict[key]
    return retdict