from common import CGFigure
import numpy as np
from datetime import datetime
from collections import OrderedDict

def dataXFormater(val):
    val = str(datetime.fromtimestamp(val).strftime('%I %P') + "---")
    return val

def dataYFormater(val):
    number_string = hex(val)

    return "".join(number_string)

def GetBloodGlucoseGraph(data, size, title="Graph Title", xlabel='Time', ylabel="Blood Sugar", boundary=False):
    ti = [data['data']['time'][0], data['data']['time'][-1]]
    vals = [[100, 130], [100, 130]]
    ax = CGFigure(size, title=title, xlabel=xlabel, ylabel=ylabel, boundary=boundary)
    ax.xAxisDataFormator = dataXFormater
    ax.yAxisDataFormator = dataYFormater
    ax.fillbetween(data['data']['time'], data['data']['Q2'], color=(0.0, 0.9, 0.0, 1))
    ax.fillbetween(data['data']['time'], data['data']['Q1'], color=(0.9, 0.0, 0.0, 1))
    ax.fillbetween(ti, vals, color=(0.1, 0.1, 0.1, 0.5))
    ref = ax.plot(data['data']['time'], data['data']['value'])
    ax.fillbelow(ref['x'], ref['y'],  np.array(data['data']['value']) + 70)
    ax.fillabove(ref['x'], ref['y'], 100)
    ax.plotrange(data['normal_range'])
    graph = ax.render()
    return graph