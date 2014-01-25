from flask import Flask, render_template, json, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import json
from mpltools import style
from mpltools import layout
import random
import datetime
import pytz
import random
import string
from threading import Lock

from iiit_disagg.smap_interface import SMAP
from iiit_disagg.smap_interface import to_pd_series
from nilmtk.building import Building
from nilmtk.sensors.electricity import MainsName, Measurement
from nilmtk.disaggregate.co_1d import CO_1d

matplotlib.use('Agg')
plt.ioff()

style.use('ggplot')
lock = Lock()

SMAP_URL = "http://nms.iiitd.edu.in:9102/"

OFFSET = 0
TIMEZONE = 'Asia/Kolkata'


def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def pd_to_higcharts(predictions):
    total_power = predictions.sum().sum()
    num_rows = len(predictions.index)
    temp = np.empty((num_rows, 2))
    times = predictions.index.astype(int) / 1e6
    temp[:, 0] = times
    time_series = []
    pie_series = []
    for appliance_name in predictions.columns:
        pie_series.append([appliance_name[0] + str(appliance_name[1]),
                          float(predictions[[appliance_name]].sum() / total_power) * 100])
        temp[:, 1] = predictions[[appliance_name]].values.reshape(num_rows,)
        time_series.append(
            {'name': appliance_name[0] + str(appliance_name[1]), 'data': temp.tolist()})
    series = {'pie': pie_series, 'timeseries': time_series}
    return json.dumps(series)


app = Flask(__name__)


def calculate_downsampling_frequency(df, threshold_points=15000):
    num_columns = df.columns.size
    num_rows = int(np.sum(df.count()))
    if num_rows > threshold_points:
        factor_in_seconds = int(num_rows / threshold_points)
        print "DOWNSAMPLING: " + str(factor_in_seconds)
        return str(factor_in_seconds) + 's'
    else:
        return None


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/visualize')
def visualize():
    return render_template('visualize.html')


@app.route('/query', methods=['POST'])
def query():
    data = json.loads(request.data)
    home_number = data["home_number"]
    start_timestamp = data['start'] * 1000
    end_timestamp = data['end'] * 1000

    # Creating a SMAP interface
    smap = SMAP(SMAP_URL)
    uuid = smap.get_uuid(home_number)
    smap_readings = smap.get_readings(uuid, start_timestamp, end_timestamp)

    df = to_pd_series(smap_readings)

    # Creating nilmtk building
    b = Building()
    # Attaching mains
    b.utility.electric.mains[MainsName(1, 1)] = df
    # Instantiating CO disaggregator
    disaggregator = CO_1d()
    # Loading model
    disaggregator.import_model('../examples/model.json')
    # Perform disaggregation
    disaggregator.disaggregate(b)
    predictions = disaggregator.predictions
    return pd_to_higcharts(predictions)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
