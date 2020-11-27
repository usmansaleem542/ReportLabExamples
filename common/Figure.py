from common.CanvasFigure import CanvasFigure
import numpy as np
import math
import sys


class CGFigure:
    def __init__(self, figure_size, title=None, xlabel=None, ylabel=None, boundary=False):
        self.FigSize = figure_size
        self.Title = title
        self.xLabel = xlabel
        self.yLabel = ylabel
        self.Boundary = boundary
        self.Plots = []
        self.DataStats = {'xMin': sys.maxsize, "xMax": -sys.maxsize, "yMin": sys.maxsize, "yMax": -sys.maxsize}
        self.xAxisDataFormator = None
        self.yAxisDataFormator = None
        self.Stats = {}
        self.Init()

    def Init(self):
        self.Stats['xAxis'] = {}
        self.Stats['yAxis'] = {}
        self.setpadding()
        self.pWidth = self.FigSize[0] - (self.PLeft + self.PRight)
        self.pHeight = self.FigSize[1] - (self.PTop + self.PBottom)

    def setsuptitle(self, title):
        self.Title = title

    def setxlabel(self, label):
        self.xLabel = label

    def setpadding(self, top=50, left=50, right=50, bottom=50):
        self.PTop = top
        self.PLeft = left
        self.PRight = right
        self.PBottom = bottom

    def setylabel(self, label):
        self.yLabel = label

    def calculateMajorsY(self, minStep=50):

        minV = math.floor(self.DataStats['yMin']/minStep)*minStep
        maxV = math.ceil(self.DataStats['yMax']/minStep)*minStep
        if minV == maxV:
            print("There is Issue in Given Data For Y Axis")
            exit()

        self.Stats['yAxis']['min'] = minV
        self.Stats['yAxis']['max'] = maxV
        step =  math.ceil(((maxV - minV)*.10)/minStep) * minStep
        pos = list(range(minV, maxV+1, step))
        self.Stats['yAxis']['major'] = pos

    def calculateMajorsX(self, minStep=50):

        minV = math.floor(self.DataStats['xMin']/minStep)*minStep
        maxV = math.ceil(self.DataStats['xMax']/minStep)*minStep
        if minV == maxV:
            print("There is Issue in Given Data For Y Axis")
            exit()

        self.Stats['xAxis']['min'] = minV
        self.Stats['xAxis']['max'] = maxV
        step =  math.ceil(((maxV - minV)*.10)/minStep) * minStep
        pos = list(range(minV, maxV+1, step))
        self.Stats['xAxis']['major'] = pos

    def plot(self, x, y):
        self.Plots.append({"type": "lineplot", "x": x, "y": y})
        return self.Plots[-1]

    def fillbetween(self, x, y):
        self.Plots.append({"type": "fillbetween", "x": x, "y": y})
        return self.Plots[-1]

    def fillabove(self, ref, y=None):
        self.Plots.append({"type": "fillabove", "ref": ref, "x": None,  "y": y})
        return self.Plots[-1]

    def fillbelow(self, ref, y=None):
        self.Plots.append({"type": "fillbelow", "ref": ref, "x": None,  "y": y})
        return self.Plots[-1]

    def plotrange(self, range):
        self.Plots.append({"type": "range", "x": None, "y": range})
        return self.Plots[-1]

    def calcDataStats(self):
        for plData in self.Plots:
            x = plData.get('x', None)
            y = plData.get('y', None)
            if x is not None:
                x = np.array(x)
                self.DataStats['xMin'] = min(self.DataStats['xMin'], x.min())
                self.DataStats['xMax'] = max(self.DataStats['xMax'], x.max())
            if y is not None:
                y = np.array(y)
                self.DataStats['yMin'] = min(self.DataStats['yMin'], y.min())
                self.DataStats['yMax'] = max(self.DataStats['yMax'], y.max())

    def render(self):
        self.calcDataStats()
        self.calculateMajorsX(minStep=50)
        self.calculateMajorsY(minStep=50)

        print(self.DataStats)
        cf = CanvasFigure(self)
        return cf