"""Contains methods to interact with sMAP interface to pull data according to
sMAP query language"""

import requests
import pandas as pd
from nilmtk.sensors.electricity import Measurement


def to_pd_series(smap_data):
    df = pd.DataFrame(
        smap_data, columns=['timestamp', Measurement('power', 'active')])
    df.index = pd.to_datetime(df.timestamp, unit='ms')
    df = df.drop('timestamp', 1)
    return df


class SMAP(object):

    def __init__(self, base_url, query_path="/api/query/", data_path="backend/api/data/"):
        self.post_url = "".join([base_url, query_path])
        self.data_path = "".join([base_url, data_path])

    def get_readings(self, uuid, start_time, end_time):
        query = "{}uuid/{}?starttime={}&endtime={}".format(self.data_path,
                                                           uuid, start_time, end_time)
        response = requests.get(query).json()
        data = response[0]['Readings']
        return data
