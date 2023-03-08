#from http import HTTPStatus
#from imp import init_builtin
#from typing import List
from flask import render_template, flash, redirect, url_for,Response,request  # type: ignore
from app import app, Log
from app.models import db, MEAS_CONT_VALUE_TAB
#import pandas as pd
import json, time
from datetime import datetime,timedelta
from sqlalchemy import func, distinct

timeList=[]
dataList=dict()
alreadyStarted = False
databaseStarted = False
# Constants
MAX_DURATION = 10
TIME_FORMAT = "%H:%M:%S"
DB_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

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
    user = {'username': 'Everybody'}
    posts = [
        {
            'author': {'username': 'A1'},
            'body': 'Welcome to Real Time Trend'
        },
        {
            'author': {'username': 'A2'},
            'body': 'Have a Nice Day'
        }
    ]
    return render_template('index.html', pagetitle='Home', user=user, posts=posts)

#realtime_trend
@app.route('/realtime-trend', methods=['GET', 'POST'])
def realtime_trend():
    return render_template('realtime_trend.html', pagetitle='Realtime Trend')

#history_trend
@app.route('/history-trend', methods=['GET', 'POST'])
def history_trend():
    end_date = datetime.now()
    start_date =end_date - timedelta(minutes=15)
    if request.method == "POST":
        filter = json.loads(request.get_data())        
        start_date = datetime.strptime(filter['start'].replace("T", " "), DATETIME_FORMAT)
        end_date = datetime.strptime(filter['end'].replace("T", " "), DATETIME_FORMAT)
        print(start_date)
        print(end_date)
        cols = [func.avg(getattr(MEAS_CONT_VALUE_TAB, name)).label(name) for name in app.config['DB_COLUMNS']]
        cols.append(MEAS_CONT_VALUE_TAB.dtactual)

        data = MEAS_CONT_VALUE_TAB.query.filter(MEAS_CONT_VALUE_TAB.dtactual > start_date, MEAS_CONT_VALUE_TAB.dtactual < end_date)\
                    .order_by(MEAS_CONT_VALUE_TAB.dtactual)\
                    .with_entities(*cols)\
                    .group_by(MEAS_CONT_VALUE_TAB.dtactual).all()    

        dataList = dict()
        for col in app.config['DB_COLUMNS']:
            dataList[col] = list()
        dataList['time'] = list()
        try:
            for item in data:
                for col in app.config['DB_COLUMNS']:
                    dataList[col].append(float(dict(item)[col]))
                dataList['time'].append(item.dtactual.strftime(TIME_FORMAT))
        except Exception as ex:
            Log.exception(f"Exception:{ex}")
        return json.dumps(dataList)

    return render_template('history_trend.html', pagetitle='History Trend', start_date = start_date.strftime(DATETIME_FORMAT), end_date = end_date.strftime(DATETIME_FORMAT))

#coilwise_trend
@app.route('/coilwise-trend', methods=['GET', 'POST'])
def coilwise_trend():
    return render_template('coilwise_trend.html', pagetitle='Coilwise Trend')

@app.route('/coilwise-trend/<coilId>')  # type: ignore
def coilwise_trend_with_arg(coilId):
    Log.debug(f"Coil ID: {coilId}")
    
    cols = [func.avg(getattr(MEAS_CONT_VALUE_TAB, name)).label(name) for name in app.config['DB_COLUMNS']]
    cols.append(MEAS_CONT_VALUE_TAB.dtactual)

    data = MEAS_CONT_VALUE_TAB.query.filter(MEAS_CONT_VALUE_TAB.coilidout == coilId).order_by(MEAS_CONT_VALUE_TAB.dtactual).with_entities(*cols).group_by(MEAS_CONT_VALUE_TAB.dtactual).all()  
    Log.debug(f"@@coilwise trend: {coilId}")
    coilDataList = dict()
    for col in app.config['DB_COLUMNS']:
        coilDataList[col] = list()
    coilDataList['time'] = list()
    try:
        for item in data:
            for col in app.config['DB_COLUMNS']:
                coilDataList[col].append(float(dict(item)[col]))
            coilDataList['time'].append(item.dtactual.strftime(TIME_FORMAT))
    except Exception as ex:
        Log.exception(f"Exception:{ex}")
    return json.dumps(coilDataList)
    
    
#query-database
@app.route('/query-database', methods=['GET', 'POST'])  # type: ignore
def query_database():
    global timeList
    global dataList
    global databaseStarted

    Log.debug(f"@@query_database api called")
    if(databaseStarted != True):
        init_List()
        databaseStarted = True
        Log.debug(f"@@query_database starting")
        while (app.config['shutdown'] == False):  # type: ignore
            dataListTemp = dict()
            for col in app.config['DB_COLUMNS']:
                dataListTemp[col] = list()

            dataListTemp['time'] = list()
            timeListTemp = list()
            dtLagging = datetime.now() - timedelta(minutes=MAX_DURATION)
            cols = [func.avg(getattr(MEAS_CONT_VALUE_TAB, name)).label(name) for name in app.config['DB_COLUMNS']]
            cols.append(MEAS_CONT_VALUE_TAB.dtactual)

            data = MEAS_CONT_VALUE_TAB.query.filter(MEAS_CONT_VALUE_TAB.dtactual > dtLagging).order_by(MEAS_CONT_VALUE_TAB.dtactual).with_entities(*cols).group_by(MEAS_CONT_VALUE_TAB.dtactual).all()    
            try:
                for item in data:
                    for col in app.config['DB_COLUMNS']:
                        dataListTemp[col].append(float(dict(item)[col]))
                    timeListTemp.append(item.dtactual)
                    dataListTemp['time'].append(item.dtactual.strftime(DB_TIME_FORMAT))
                # Fill up global list
                dataList = dataListTemp
                timeList = timeListTemp
            except Exception as ex:
                Log.exception(f"Exception:{ex}")
            time.sleep(1)
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
    startTime = datetime.now() - timedelta(seconds=duration)
    def generate_data():
        global timeList
        global dataList

        timeout = 10
        index = 0
        # if(duration==MAX_DURATION):
        #     consolidatedData = dataList
        # else:
        #     for item in timeList:
        #         if(item >= startTime):
        #             #print(f"item:{item} startTime:{startTime}")
        #             break
        #         else:
        #             index += 1
        #     consolidatedData = dataList
        #     if index > 0:
        #         for col in consolidatedData:
        #             consolidatedData[col] = consolidatedData[col][index:]
                  
        # #debug start
        # datalength = len(consolidatedData.get('time', list()))
        # if datalength == 0:
        #     Log.debug(f"index:{index} datalength: {datalength}")
        #     Log.debug(f"dataList length: {len(dataList.get('time', list()))}")
        # if len(timeList) > 0:
        #     timeLagg = (datetime.now() - timeList[len(timeList) - 1]).total_seconds()
        
        #     while timeLagg > 2 * float(app.config['SAMPLING_RATE']):
        #         for col in consolidatedData:
        #             consolidatedData[col].append(None)  # type: ignore
        #         timeList.append(timeList[len(timeList) - 1] + timedelta(seconds=float(app.config['SAMPLING_RATE'])))
        #         consolidatedData['time'][len(consolidatedData['time'])-1] = timeList[len(timeList) - 1].strftime(TIME_FORMAT)
        #         timeLagg = (datetime.now() - timeList[len(timeList) - 1]).total_seconds()
        #     timeLagg = (datetime.now() - timeList[len(timeList) - 1]).total_seconds()
        #     Log.debug(f"timeLagg: {timeLagg}")
        #     Log.debug(f"SAMPL_RATE:{float(app.config['SAMPLING_RATE'])}")
        #debug end
        consolidatedData = dataList
        json_data = json.dumps(consolidatedData)
        msg = f"data:{json_data}\n\n"
        yield f'retry: {timeout}\n{msg}'
        #Log.debug(f"trend_data sent: {datetime.now().strftime(DATETIME_FORMAT)}, duration: {duration}")

        # if len(dataList.get('time', list()))>0:
        #     yield f'retry: {timeout}\n{msg}'
        time.sleep(float(app.config['SAMPLING_RATE']))

    return Response(generate_data(), mimetype='text/event-stream')


#coilwise_trend
@app.route('/signal-config', methods=['GET'])
def get_signal_config():
    config = list()
    config.append({
        'signalName':'length',
        'min':0,
        'max':800,
        'show':True
    })
    config.append({
        'signalName':'stripspeed',
        'min':0,
        'max':1,
        'show':True
    })
    config.append({
        'signalName':'thickness',
        'min':0,
        'max':2,
        'show':True
    })
    return json.dumps(config)

@app.route('/signal-options', methods=['GET'])
def get_signal_options():
    options = list()
    for col in app.config['DB_COLUMNS']:
        options.append(col)
    return json.dumps(options)

#flatness_trend
@app.route('/flatness-trend', methods=['GET', 'POST'])
def flatness_trend():
    return render_template('flatness_trend.html', pagetitle='Flatness Trend')


@app.route('/flatness-trend/<coilId>')  # type: ignore
def flatness_trend_with_arg(coilId):
    Log.debug(f"Coil ID: {coilId}")
    data = db.session.query(MEAS_CONT_VALUE_TAB).filter(MEAS_CONT_VALUE_TAB.coilidout == coilId).order_by(MEAS_CONT_VALUE_TAB.length).all()
    data_list = list()
    flatness_col = list()
    formatted_data = dict()
    formatted_data["x"] = list()    #length
    formatted_data["y"] = list()    #flatness_col
    formatted_data["z"] = list()    #value
    for row in data:
        data_list.append(row2dict(row))
    for key in data_list[0]:
        tempList = list()
        if 'flatness' in key and 'dev' not in key:
            flatness_col.append(key)
    for col in flatness_col:
        tempList = [float(x[col]) for x in data_list]
        formatted_data["z"].append(tempList)
    formatted_data["y"] = flatness_col
    formatted_data["x"] = [float(x["length"]) for x in data_list]
        
    return json.dumps(formatted_data)


@app.route('/coil-options', methods=['GET'])
def get_coil_options():
    query = MEAS_CONT_VALUE_TAB.query.with_entities(MEAS_CONT_VALUE_TAB.coilidout).distinct()
    data = [row.coilidout for row in query.all()]
    print(data)
    return json.dumps(data)