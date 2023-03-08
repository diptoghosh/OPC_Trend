#from http import HTTPStatus
#from imp import init_builtin
#from typing import List
from flask import render_template, flash, redirect, url_for,Response,request  # type: ignore
from app import app, Log
from app.models import db, MEAS_CONT_VALUE_TAB
#import pandas as pd
import json, time
from datetime import datetime,timedelta
from sqlalchemy import func

timeList=[]
dataList=dict()
alreadyStarted = False
databaseStarted = False

def getSignalList():
    global dataList
    dataList['length_coil_exit'] = list()
    dataList['speed_strip_exit'] = list()
    dataList['elongation_trg'] = list()
    dataList['elongation'] = list()
    dataList['flag_accel'] = list()
    dataList['gcs_active'] = list()
    dataList['fcs_active'] = list()
    dataList['thick_exit_trg'] = list()
    dataList['thick_exit_meas'] = list()
    dataList['flat_exit_meas_dev'] = list()
    dataList['flat_exit_meas_1'] = list()

def init_List():
    global timeList
    global dataList
    for col in app.config['DB_COLUMNS']:
        dataList[col] = list()
    # dataList['length_coil_exit'] = list()
    # dataList['speed_strip_exit'] = list()
    # dataList['elongation_trg'] = list()
    # dataList['elongation'] = list()
    # dataList['flag_accel'] = list()
    # dataList['gcs_active'] = list()
    # dataList['fcs_active'] = list()
    # dataList['thick_exit_trg'] = list()
    # dataList['thick_exit_meas'] = list()
    # dataList['flat_exit_meas_dev'] = list()
    # dataList['flat_exit_meas_1'] = list()
    # dataList['time'] = list()
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
        start_date = datetime.strptime(filter['start'].replace("T", " "), "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(filter['end'].replace("T", " "), "%Y-%m-%d %H:%M:%S")
        print(start_date)
        print(end_date)
        data = MEAS_CONT_VALUE_TAB.query.filter(MEAS_CONT_VALUE_TAB.dtactual > start_date, MEAS_CONT_VALUE_TAB.dtactual < end_date)\
                    .order_by(MEAS_CONT_VALUE_TAB.dtactual).with_entities(MEAS_CONT_VALUE_TAB.dtactual,\
                    func.avg(MEAS_CONT_VALUE_TAB.length_coil_exit).label('length_coil_exit'),\
                    func.avg(MEAS_CONT_VALUE_TAB.speed_strip_exit).label('speed_strip_exit'),\
                    func.avg(MEAS_CONT_VALUE_TAB.elongation_trg).label('elongation_trg'),\
                    func.avg(MEAS_CONT_VALUE_TAB.elongation).label('elongation'),\
                    func.avg(MEAS_CONT_VALUE_TAB.flag_accel).label('flag_accel'),\
                    func.avg(MEAS_CONT_VALUE_TAB.gcs_active).label('gcs_active'),\
                    func.avg(MEAS_CONT_VALUE_TAB.fcs_active).label('fcs_active'),\
                    func.avg(MEAS_CONT_VALUE_TAB.thick_exit_trg).label('thick_exit_trg'),\
                    func.avg(MEAS_CONT_VALUE_TAB.thick_exit_meas).label('thick_exit_meas'),\
                    func.avg(MEAS_CONT_VALUE_TAB.flat_exit_meas_dev).label('flat_exit_meas_dev'),\
                    func.avg(MEAS_CONT_VALUE_TAB.flat_exit_meas_1).label('flat_exit_meas_1'),\
                    func.avg(MEAS_CONT_VALUE_TAB.flat_exit_meas_2).label('flat_exit_meas_2')).group_by(MEAS_CONT_VALUE_TAB.dtactual).all()
        dataList = dict()
        dataList['length_coil_exit'] = list()
        dataList['speed_strip_exit'] = list()
        dataList['elongation_trg'] = list()
        dataList['elongation'] = list()
        dataList['flag_accel'] = list()
        dataList['gcs_active'] = list()
        dataList['fcs_active'] = list()
        dataList['thick_exit_trg'] = list()
        dataList['thick_exit_meas'] = list()
        dataList['flat_exit_meas_dev'] = list()
        dataList['flat_exit_meas_1'] = list()
        dataList['time'] = list()
        try:
            for item in data:
                dataList['length_coil_exit'].append(float(item.length_coil_exit))
                dataList['speed_strip_exit'].append(float(item.speed_strip_exit))
                dataList['elongation_trg'].append(float(item.elongation_trg))
                dataList['elongation'].append(float(item.elongation))
                dataList['flag_accel'].append(float(item.flag_accel))
                dataList['gcs_active'].append(float(item.gcs_active))
                dataList['fcs_active'].append(float(item.fcs_active))
                dataList['thick_exit_trg'].append(float(item.thick_exit_trg))
                dataList['thick_exit_meas'].append(float(item.thick_exit_meas))
                dataList['flat_exit_meas_dev'].append(float(item.flat_exit_meas_dev))
                dataList['flat_exit_meas_1'].append(float(item.flat_exit_meas_1))
                dataList['time'].append(item.dtactual.strftime('%H:%M:%S'))
        except Exception as ex:
            Log.exception(f"Exception:{ex}")
        return json.dumps(dataList)

    return render_template('history_trend.html', pagetitle='History Trend', start_date = start_date.strftime('%Y-%m-%d %H:%M:%S'), end_date = end_date.strftime('%Y-%m-%d %H:%M:%S'))

#coilwise_trend
@app.route('/coilwise-trend', methods=['GET', 'POST'])
def coilwise_trend():
    return render_template('coilwise_trend.html', pagetitle='Coilwise Trend')

@app.route('/coilwise-trend/<coilId>')  # type: ignore
def coilwise_trend_with_arg(coilId):
    Log.debug(f"Coil ID: {coilId}")
    data = MEAS_CONT_VALUE_TAB.query.filter(MEAS_CONT_VALUE_TAB.id_coil == coilId).order_by(MEAS_CONT_VALUE_TAB.dtactual).with_entities(MEAS_CONT_VALUE_TAB.dtactual,\
            func.avg(MEAS_CONT_VALUE_TAB.length_coil_exit).label('length_coil_exit'),\
            func.avg(MEAS_CONT_VALUE_TAB.speed_strip_exit).label('speed_strip_exit'),\
            func.avg(MEAS_CONT_VALUE_TAB.elongation_trg).label('elongation_trg'),\
            func.avg(MEAS_CONT_VALUE_TAB.elongation).label('elongation'),\
            func.avg(MEAS_CONT_VALUE_TAB.flag_accel).label('flag_accel'),\
            func.avg(MEAS_CONT_VALUE_TAB.gcs_active).label('gcs_active'),\
            func.avg(MEAS_CONT_VALUE_TAB.fcs_active).label('fcs_active'),\
            func.avg(MEAS_CONT_VALUE_TAB.thick_exit_trg).label('thick_exit_trg'),\
            func.avg(MEAS_CONT_VALUE_TAB.thick_exit_meas).label('thick_exit_meas'),\
            func.avg(MEAS_CONT_VALUE_TAB.flat_exit_meas_dev).label('flat_exit_meas_dev'),\
            func.avg(MEAS_CONT_VALUE_TAB.flat_exit_meas_1).label('flat_exit_meas_1'),\
            func.avg(MEAS_CONT_VALUE_TAB.flat_exit_meas_2).label('flat_exit_meas_2')).group_by(MEAS_CONT_VALUE_TAB.dtactual).all()
    Log.debug(f"@@coilwise trend: {coilId}")
    coilDataList = dict()
    coilDataList['length_coil_exit'] = list()
    coilDataList['speed_strip_exit'] = list()
    coilDataList['elongation_trg'] = list()
    coilDataList['elongation'] = list()
    coilDataList['flag_accel'] = list()
    coilDataList['gcs_active'] = list()
    coilDataList['fcs_active'] = list()
    coilDataList['thick_exit_trg'] = list()
    coilDataList['thick_exit_meas'] = list()
    coilDataList['flat_exit_meas_dev'] = list()
    coilDataList['flat_exit_meas_1'] = list()
    coilDataList['time'] = list()
    try:
        for item in data:
            coilDataList['length_coil_exit'].append(float(item.length_coil_exit))
            coilDataList['speed_strip_exit'].append(float(item.speed_strip_exit))
            coilDataList['elongation_trg'].append(float(item.elongation_trg))
            coilDataList['elongation'].append(float(item.elongation))
            coilDataList['flag_accel'].append(float(item.flag_accel))
            coilDataList['gcs_active'].append(float(item.gcs_active))
            coilDataList['fcs_active'].append(float(item.fcs_active))
            coilDataList['thick_exit_trg'].append(float(item.thick_exit_trg))
            coilDataList['thick_exit_meas'].append(float(item.thick_exit_meas))
            coilDataList['flat_exit_meas_dev'].append(float(item.flat_exit_meas_dev))
            coilDataList['flat_exit_meas_1'].append(float(item.flat_exit_meas_1))
            coilDataList['time'].append(item.dtactual.strftime('%H:%M:%S'))
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
        getSignalList()
        databaseStarted = True
        Log.debug(f"@@query_database starting")
        while (app.config['shutdown'] == False):
            dataListTemp = dict()
            for col in app.config['DB_COLUMNS']:
                dataListTemp[col] = list()
            # dataListTemp['length_coil_exit'] = list()
            # dataListTemp['speed_strip_exit'] = list()
            # dataListTemp['elongation_trg'] = list()
            # dataListTemp['elongation'] = list()
            # dataListTemp['flag_accel'] = list()
            # dataListTemp['gcs_active'] = list()
            # dataListTemp['fcs_active'] = list()
            # dataListTemp['thick_exit_trg'] = list()
            # dataListTemp['thick_exit_meas'] = list()
            # dataListTemp['flat_exit_meas_dev'] = list()
            # dataListTemp['flat_exit_meas_1'] = list()
            dataListTemp['time'] = list()
            timeListTemp = list()
            dtLagging = datetime.now() - timedelta(minutes=10)
            cols = [func.avg(getattr(MEAS_CONT_VALUE_TAB, name)).label(name) for name in app.config['DB_COLUMNS']]

            cols.append(MEAS_CONT_VALUE_TAB.dtactual)

            #cols.append(MEAS_CONT_VALUE_TAB.dtactual)
            data = MEAS_CONT_VALUE_TAB.query.filter(MEAS_CONT_VALUE_TAB.dtactual > dtLagging).order_by(MEAS_CONT_VALUE_TAB.dtactual).with_entities(*cols).group_by(MEAS_CONT_VALUE_TAB.dtactual).all()
            #test
            # data = MEAS_CONT_VALUE_TAB.query.filter(MEAS_CONT_VALUE_TAB.dtactual > dtLagging).order_by(MEAS_CONT_VALUE_TAB.dtactual).with_entities(MEAS_CONT_VALUE_TAB.dtactual,\
            #             func.avg(MEAS_CONT_VALUE_TAB.length_coil_exit).label('length_coil_exit'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.speed_strip_exit).label('speed_strip_exit'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.elongation_trg).label('elongation_trg'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.elongation).label('elongation'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.flag_accel).label('flag_accel'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.gcs_active).label('gcs_active'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.fcs_active).label('fcs_active'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.thick_exit_trg).label('thick_exit_trg'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.thick_exit_meas).label('thick_exit_meas'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.flat_exit_meas_dev).label('flat_exit_meas_dev'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.flat_exit_meas_1).label('flat_exit_meas_1'),\
            #             func.avg(MEAS_CONT_VALUE_TAB.flat_exit_meas_2).label('flat_exit_meas_2')).group_by(MEAS_CONT_VALUE_TAB.dtactual).all()
            
            try:
                for item in data:
                    for col in app.config['DB_COLUMNS']:
                        print(dict(item))
                        dataListTemp[col].append(float(dict(item)[col]))
                    # dataListTemp['length_coil_exit'].append(float(item.length_coil_exit))
                    # dataListTemp['speed_strip_exit'].append(float(item.speed_strip_exit))
                    # dataListTemp['elongation_trg'].append(float(item.elongation_trg))
                    # dataListTemp['elongation'].append(float(item.elongation))
                    # dataListTemp['flag_accel'].append(float(item.flag_accel))
                    # dataListTemp['gcs_active'].append(float(item.gcs_active))
                    # dataListTemp['fcs_active'].append(float(item.fcs_active))
                    # dataListTemp['thick_exit_trg'].append(float(item.thick_exit_trg))
                    # dataListTemp['thick_exit_meas'].append(float(item.thick_exit_meas))
                    # dataListTemp['flat_exit_meas_dev'].append(float(item.flat_exit_meas_dev))
                    # dataListTemp['flat_exit_meas_1'].append(float(item.flat_exit_meas_1))
                    timeListTemp.append(item.dtactual)
                    dataListTemp['time'].append(item.dtactual.strftime('%H:%M:%S'))
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
        timeout = 500
        index = 0
        for item in timeList:
            if(item >= startTime):
                print(f"item:{item} startTime:{startTime}")
                break
            else:
                index += 1
        consolidatedData = dataList
        if index > 0:
            for key in consolidatedData:
                consolidatedData[key] = consolidatedData[key][index:]
        json_data = json.dumps(consolidatedData)
        msg = f"data:{json_data}\n\n"
        Log.debug(f"trend_data sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, duration: {duration}")
        Log.debug(f"index:{index} datalength: {len(consolidatedData.get('time', list()))}")
        yield f'retry: {timeout}\n{msg}'
        time.sleep(float(app.config['SAMPLING_RATE']))

    return Response(generate_data(), mimetype='text/event-stream')


#coilwise_trend
@app.route('/signal-config', methods=['GET'])
def get_signal_config():
    config = list()
    config.append({
        'signalName':'length_coil_exit',
        'min':0,
        'max':100,
        'show':True
    })
    config.append({
        'signalName':'speed_strip_exit',
        'min':0,
        'max':100,
        'show':True
    })
    return json.dumps(config)

@app.route('/signal-options', methods=['GET'])
def get_signal_options():
    options = list()
    options.append('length_coil_exit')
    options.append('speed_strip_exit')
    options.append('elongation_trg')
    options.append('elongation')
    options.append('flag_accel')
    options.append('gcs_active')
    options.append('fcs_active')
    options.append('thick_exit_trg')
    options.append('thick_exit_meas')
    options.append('flat_exit_meas_dev')
    options.append('flat_exit_meas_1')
    return json.dumps(options)