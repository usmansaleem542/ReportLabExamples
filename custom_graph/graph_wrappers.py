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
    ax = CGFigure(size, title=title, xlabel=xlabel, ylabel=ylabel, boundary=boundary)
    ax.xAxisDataFormator = dataXFormater
    ax.yAxisDataFormator = dataYFormater
    ax.fillbetween(data['data']['time'], data['data']['Q1'])
    ax.fillbetween(data['data']['time'], data['data']['Q2'])
    ref = ax.plot(data['data']['time'], data['data']['value'])
    ax.fillbelow(ref,  np.array(data['data']['value']) + 70)
    ax.fillabove(ref, 100)
    ax.plotrange(data['normal_range'])
    graph = ax.render()
    return graph