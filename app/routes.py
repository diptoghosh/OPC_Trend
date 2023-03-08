from flask import render_template, flash, redirect, url_for,Response,request  # type: ignore
from app import app, Log
from app.tools import get_config
import json, time, zipfile, os
from datetime import datetime,timedelta
from app.models import RCLIENT, ARCHIVE_LOCATION, MAX_CHART_COUNT, map_tag

timeList=[]
dataList=dict()
alreadyStarted = False
queryStarted = False
dataStartTS = datetime.now()
# Constants
MAX_DURATION = 10
TIME_FORMAT = "%H:%M:%S"
DB_TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
sDATETIME_FORMAT = "%Y-%m-%d %H:%M"

def retreive_history_data(starttime:datetime, endtime:datetime):
    zip_file_list = list()
    data_con = dict()
    temp_dt = starttime.replace(minute=0, second=0, microsecond=0)

    while temp_dt <= endtime:
        if os.path.exists(os.path.join(ARCHIVE_LOCATION, temp_dt.strftime("%Y%m%d%H"))):
            zip_file_list.append(temp_dt.strftime("%Y%m%d%H"))
        temp_dt = temp_dt + timedelta(hours=1)
    Log.debug(f"data requested for:  {starttime.strftime('%Y%m%d%H')} to {endtime.strftime('%Y%m%d%H')}")
    Log.debug(f"zip file list: {zip_file_list}")
    for zip_file in zip_file_list:
        Log.debug(f'Loading from : {zip_file}')
        if starttime.strftime("%Y%m%d%H") == endtime.strftime("%Y%m%d%H"):
            with zipfile.ZipFile(os.path.join(ARCHIVE_LOCATION, zip_file), "r") as f:
                for i in range(starttime.minute, endtime.minute):
                    name = (str(i) if len(str(i)) > 1 else '0' + str(i) ) + '.json'
                    if name in f.namelist():
                        data = json.loads(f.read(name))
                        if len(data_con) == 0:
                            data_con = data
                        else:
                            for key in data:
                                if key in data_con:
                                    data_con[key] = data_con[key] + data[key]
        elif zip_file == starttime.strftime("%Y%m%d%H"):
            with zipfile.ZipFile(os.path.join(ARCHIVE_LOCATION, zip_file), "r") as f:
                for i in range(starttime.minute, 60):
                    name = (str(i) if len(str(i)) > 1 else '0' + str(i) ) + '.json'
                    if name in f.namelist():
                        data = json.loads(f.read(name))
                        if len(data_con) == 0:
                            data_con = data
                        else:
                            for key in data:
                                if key in data_con:
                                    data_con[key] = data_con[key] + data[key]
        elif zip_file == endtime.strftime("%Y%m%d%H"):
            with zipfile.ZipFile(os.path.join(ARCHIVE_LOCATION, zip_file), "r") as f:
                for i in range(0, endtime.minute):
                    name = (str(i) if len(str(i)) > 1 else '0' + str(i) ) + '.json'
                    if name in f.namelist():
                        data = json.loads(f.read(name))
                        if len(data_con) == 0:
                            data_con = data
                        else:
                            for key in data:
                                if key in data_con:
                                    data_con[key] = data_con[key] + data[key]
        else:
            with zipfile.ZipFile(os.path.join(ARCHIVE_LOCATION, zip_file), "r") as f:
                for i in range(0, 60):
                    name = (str(i) if len(str(i)) > 1 else '0' + str(i) ) + '.json'
                    if name in f.namelist():
                        data = json.loads(f.read(name))
                        if len(data_con) == 0:
                            data_con = data
                        else:
                            for key in data:
                                if key in data_con:
                                    data_con[key] = data_con[key] + data[key]
    return map_tag(data_con)

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

def init_List():
    global timeList
    global dataList
    for col in app.config['DB_COLUMNS']:
        dataList[col] = list()
    timeList = list()
    
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', pagetitle='Home')

#realtime_trend
@app.route('/realtime-trend', methods=['GET', 'POST'])
def realtime_trend():
    return render_template('realtime_trend.html', pagetitle='Realtime Trend')

#history_trend
@app.route('/history-trend', methods=['GET', 'POST'])
def history_trend():
    end_date = datetime.now() - timedelta(minutes=1)
    start_date =end_date - timedelta(minutes=16)
    if request.method == "POST":
        filter = json.loads(request.get_data())
        start_date = datetime.strptime(filter['start'].replace("T", " "), sDATETIME_FORMAT)
        end_date = datetime.strptime(filter['end'].replace("T", " "), sDATETIME_FORMAT)
        Log.debug(f"StartTime:{start_date}, EndTime:{end_date}")
        return json.dumps(retreive_history_data(start_date, end_date))
                    
    return render_template('history_trend.html', pagetitle='History Trend', start_date = start_date.strftime(sDATETIME_FORMAT), end_date = end_date.strftime(sDATETIME_FORMAT))

#coilwise_trend
@app.route('/coilwise-trend', methods=['GET', 'POST'])
def coilwise_trend():
    return render_template('coilwise_trend.html', pagetitle='Coilwise Trend')

@app.route('/coilwise-trend/<coilId>')  # type: ignore
def coilwise_trend_with_arg(coilId):
    # Log.debug(f"Coil ID: {coilId}")
    
    # cols = get_column_objs(TABLE, app.config['DB_COLUMNS'])
    # id_coil = get_single_column_obj(TABLE, app.config['ID_COLUMN'])
    # dtactual = get_single_column_obj(TABLE, app.config['DATETIME_COLUMN'])
    # cols.append(dtactual)

    # data = TABLE.query.filter(id_coil == coilId).order_by(dtactual).with_entities(*cols).group_by(dtactual).all()  
    # Log.debug(f"@@coilwise trend: {coilId}")
    coilDataList = dict()
    # for col in app.config['DB_COLUMNS']:
    #     coilDataList[col] = list()
    # coilDataList['time'] = list()
    # try:
    #     for item in data:
    #         for col in app.config['DB_COLUMNS']:
    #             coilDataList[col].append(float(dict(item)[col]))
    #         coilDataList['time'].append(item.dtactual.strftime(TIME_FORMAT))
    # except Exception as ex:
    #     Log.exception(f"Exception:{ex}")
    return json.dumps(coilDataList)
    
    
#query-database
@app.route('/query-database', methods=['GET', 'POST'])  # type: ignore
def query_database():
    global timeList
    global dataList
    global queryStarted
    Log.debug(f"@@query_database api called")
    if(queryStarted != True):
        init_List()
        dataStartTS = datetime.now()
        queryStarted = True
        Log.debug(f"@@query_database starting")
        while (app.config['shutdown'] == False):  # type: ignore
            now = datetime.now()
            if (now - dataStartTS).total_seconds() > 3000:
                for key in dataList:
                    dataList[key].pop(0)
                timeList.pop(0)
                dataStartTS = now
            all_tagdata = map_tag(RCLIENT.hgetall('tagread'))
            try:
                for key in all_tagdata:
                    if key in dataList:
                        dataList[key].append(float(all_tagdata[key]))
                timeList.append(now.strftime(DB_TIME_FORMAT))
            except Exception as ex:
                Log.exception(f"Exception:{ex}")
            time.sleep(app.config['SAMPLING_RATE'])
    else:
        # send a blank response when the loop is already started
        return Response(None, mimetype='text/event-stream')
   
 
@app.route('/trend-data' )
def trend_data():
    duration = request.args.get('duration')
    if(duration == None):
        duration = 30
    else:
        duration=int(request.args.get('duration'))  # type: ignore
    def generate_data():
        global timeList
        global dataList
        dataList['time'] = timeList
        timeout = 10
        consolidatedData = dataList
        json_data = json.dumps(consolidatedData)
        msg = f"data:{json_data}\n\n"
        yield f'retry: {timeout}\n{msg}'
        time.sleep(float(app.config['SAMPLING_RATE']))

    return Response(generate_data(), mimetype='text/event-stream')


#coilwise_trend
@app.route('/signal-config', methods=['GET'])
def get_signal_config():
    config = list()
    config.append({
        'signalName':[app.config['DB_COLUMNS'][1]],
        'show':True
    })
    config.append({
        'signalName':[app.config['DB_COLUMNS'][2]],
        'show':True
    })
    config.append({
        'signalName':[app.config['DB_COLUMNS'][3],app.config['DB_COLUMNS'][4]],
        'show':True
    })
    return json.dumps(config)

@app.route('/signal-options', methods=['GET'])
def get_signal_options():
    options = list()
    for col in app.config['DB_COLUMNS']:
        options.append(col)
    return json.dumps(options)

@app.route('/max-chart-number', methods=['GET'])
def get_max_chart_number():
    options = list()
    for col in app.config['DB_COLUMNS']:
        options.append(col)
    return json.dumps({'MAX_CHART_COUNT' : MAX_CHART_COUNT})

#flatness_trend
@app.route('/flatness-trend', methods=['GET', 'POST'])
def flatness_trend():
    end_date = datetime.now() - timedelta(minutes=1)
    start_date =end_date - timedelta(minutes=16)
    if request.method == "POST":
        filter = json.loads(request.get_data())
        start_date = datetime.strptime(filter['start'].replace("T", " "), sDATETIME_FORMAT)
        end_date = datetime.strptime(filter['end'].replace("T", " "), sDATETIME_FORMAT)
        Log.debug(f"StartTime:{start_date}, EndTime:{end_date}")
        return json.dumps(retreive_history_data(start_date, end_date))
                    
    return render_template('flatness_trend.html', pagetitle='History Trend', start_date = start_date.strftime(sDATETIME_FORMAT), end_date = end_date.strftime(sDATETIME_FORMAT))


@app.route('/flatness-trend/<coilId>')  # type: ignore
def flatness_trend_with_arg(coilId):
    formatted_data = dict()        
    return json.dumps(formatted_data)


@app.route('/coil-options', methods=['GET'])
def get_coil_options():
    data = None
    return json.dumps(data)