"""Contains methods to interact with sMAP interface to pull data according to
sMAP query language"""

import requests
import pandas as pd
from nilmtk.sensors.electricity import Measurement


def to_pd_series(smap_data):
    """Converts sMAP like data to a pandas DataFrame

    Parameters
    ---------
    smap_data: List of Lists
        Contains data in sMAP format as follows: [[timestamp (ms), power]]

    Returns
    -------
    df: pandas.DataFrame
        index: datetime, columns=nilmtk.Measurement
    """
    df = pd.DataFrame(
        smap_data, columns=['timestamp', Measurement('power', 'active')])
    df.index = pd.to_datetime(df.timestamp, unit='ms')
    df = df.drop('timestamp', 1)
    return df


class SMAP(object):

    """sMAP interface
    """

    def __init__(self, base_url, query_path="/api/query/", data_path="backend/api/data/", uuid_path="backend/api"):
        """
        Parameters
        ----------
        base_url : string
            URL where sMAP instance is running
        query_path : string
            API query path
        data_path : string
            Path to `get` data
        """
        self.base_url = base_url
        self.query_path = query_path
        self.data_path = data_path
        self.uuid_path = uuid_path
        self.uuid_path = "".join([self.base_url, self.uuid_path])
        self.post_url = "".join([self.base_url, self.query_path])
        self.data_path = "".join([self.base_url, self.data_path])

    def get_readings(self, uuid, start_time, end_time):
        """Get readings from sMAP server for a `uuid` between 
        start_time and end_time

        Parameters
        ---------
        uuid : string
            Unique identifier for the sMAP channel
        start_time : long int
            Timestamp in milliseconds
        end_time : long int
            Timestamp in milliseconds

        Returns
        -------
        smap_data : List of Lists
            Contains data in sMAP format as follows: [[timestamp (ms), power]]
        """
        query = "{}uuid/{}?starttime={}&endtime={}".format(self.data_path,
                                                           uuid, start_time, end_time)
        response = requests.get(query).json()
        smap_data = response[0]['Readings']
        return smap_data

    def find_uuid(self, home_number):
        """Returns the UUID corresponding to a home"""

        query = """select * where Metadata/Instrument/LoadType =
                "Apartments" and (Metadata/LoadLocation/Building=
                "Faculty Housing") and Metadata/Instrument/SubLoadType =
                "Apartment {}" and Metadata/Instrument/SupplyType = "Power"
                and Metadata/Extra/PhysicalParameter = 'Power'""".format(home_number)

        response = requests.post(self.uuid_path, query)
        uuid = response.json()[0]["uuid"]
        return uuid
