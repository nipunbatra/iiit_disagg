"""Illustrates disaggregation using NILMTK CO on the command line"""

from iiit_disagg.smap_interface import SMAP
from iiit_disagg.smap_interface import to_pd_series
from nilmtk.building import Building
from nilmtk.sensors.electricity import MainsName, Measurement
from nilmtk.disaggregate.co_1d import CO_1d

FLAT_NUMBER = 101
UUID = '273e1b0f-ef25-5918-ad67-efa56a834d6e'
START = 1387996200000
END = 1388341800000
DISAGG_FEATURE = Measurement('power', 'active')

# Making SMAP connection
smap = SMAP("http://nms.iiitd.edu.in:9102/")

# Getting data for UUID
smap_readings = smap.get_readings(UUID, START, END)

# Transform to NILMTK Mains
df = to_pd_series(smap_readings)

# Creating nilmtk building
b = Building()

# Attaching mains
b.utility.electric.mains[MainsName(1, 1)] = df

# Instantiating CO disaggregator
disaggregator = CO_1d()

# Loading model
disaggregator.import_model('model.json')

# Perform disaggregation
disaggregator.disaggregate(b)
