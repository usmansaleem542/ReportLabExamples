from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, time
from reportlab.platypus import (Flowable)
from reportlab.graphics.charts.axes import Color

from common import canv_utils
import numpy as np
import math


class LineGraph(Flowable):
    def __init__(self, data, width=500, height=200):
        Flowable.__init__(self)
        self.Stats = {}
        self.dataX = data['data']['time']
        self.dataY = data['data']['value']

        self.width = width
        self.height = height
        self.styles = getSampleStyleSheet()
        self.aw = 0
        self.ah = 0
        self.InitStats()
        self.mDataX = self.convert_xAxis_pixels(self.dataX)
        self.mDataY = self.convert_yAxis_pixels(self.dataY)
        # self.Padding = {"left": 0, "right": 0, "top": 0, "bottom": 0}

    def InitStats(self):
        self.Stats['xAxis'] = {}
        self.Stats['yAxis'] = {}
        self.GetVerticalPosition()
        self.GetHorizontalPosition()

    def wrap(self, available_width, available_height):
        self.aw = available_width
        self.ah = available_height
        return self.width, self.height + 50

    def GetHorizontalPosition(self, min_limit=0, max_limit=24, step=3):
        min_time = min(self.dataX)
        start = int(datetime.fromtimestamp(min_time).hour / step) * step
        end_dt = datetime.fromtimestamp(max(self.dataX))
        end = math.ceil((end_dt.hour + (end_dt.minute / 60)) / step) * step

        if end <= start:
            print("There Issue in Given Data For X Axis", start, end)
            raise Exception

        if start == min_limit:
            time_d = time.min
        else:
            time_d = time(hour=start)
        min_time = datetime.combine(datetime.fromtimestamp(min_time).date(), time_d)

        if end == max_limit:
            time_d = time.max
        else:
            time_d = time(hour=end, second=0, microsecond=0)
        max_time = datetime.combine(min_time.date(), time_d)

        self.Stats['xAxis']['min'] = min_time.timestamp()
        self.Stats['xAxis']['max'] = max_time.timestamp()
        self.Stats['xAxis']['pos'] = list(range(start, end + 1, step))

    def GetVerticalPosition(self, minLimit=None, maxLimit=None, step=50):
        max_value = max(self.dataY)
        min_value = min(self.dataY)
        min_value = math.floor(min_value / step) * step
        if minLimit is not None:
            min_value = min(minLimit, min_value)

        max_value = math.ceil(max_value / step) * step
        if maxLimit is not None:
            min_value = min(maxLimit, max_value)

        if min_value == max_value:
            print("There Issue in Given Data For Y Axis")
            exit()

        self.Stats['yAxis']['min'] = min_value
        self.Stats['yAxis']['max'] = max_value
        step = math.ceil(((max_value - min_value) * .10) / 50) * 50
        self.Stats['yAxis']['pos'] = list(range(min_value, max_value + 1, step))

    def DrawVGrid(self, grid=False):
        cols = self.Stats['xAxis']['pos']
        minTime = datetime.fromtimestamp(self.Stats['xAxis']['min'])
        maxTime = datetime.fromtimestamp(self.Stats['xAxis']['max'])
        w, h = canv_utils.GetFontWidhHeight('12', self.canv._fontname, self.canv._fontsize)
        for col in cols:
            if col == 24:
                timeD = time.max
            else:
                timeD = time(hour=col, second=0, microsecond=0)
            newT = datetime.combine(minTime.date(), timeD)
            posX = canv_utils.Point2Pixel(minTime.timestamp(), maxTime.timestamp(), 0, self.width, newT.timestamp())
            # print(newT, posX, self.width)
            pos = [posX, -(h * 2)]
            if grid: self.canv.line(pos[0], -(h / 3), pos[0], self.height)
            labelStr = newT.strftime('%I %P')
            self.canv.drawString(pos[0] - (h * 1.2), pos[1], labelStr)

    def DrawHGrid(self, grid):
        rows = self.Stats['yAxis']['pos']
        minV = self.Stats['yAxis']['min']
        maxV = self.Stats['yAxis']['max']

        w, h = canv_utils.GetFontWidhHeight('12', self.canv._fontname, self.canv._fontsize)

        for rowV in rows:
            posY = canv_utils.Point2Pixel(minV, maxV, 0, self.height, rowV)
            pos = [-h * 3, posY]
            if grid: self.canv.line(-(h / 3), pos[1], self.width, pos[1])
            # yVal = round(canv_utils.Point2Pixel(0, self.height, min(self.dataY), max(self.dataY), pos[1]))
            # vPos.append(pos)
            self.canv.drawString(pos[0], pos[1] - (h / 3), str(rowV))

    def Figure(self, grid=False):
        canv_utils.DrawRectangle(self.canv, (0, 0), (self.width, self.height))
        self.canv.saveState()
        self.canv.setStrokeColor(Color(0.1, 0.1, 0.1, 0.3))
        self.canv.setFontSize(9)
        self.DrawVGrid(grid)
        self.DrawHGrid(grid)
        self.canv.restoreState()

    def convert_QData_pixels(self, data):
        xMin = self.Stats['yAxis']['min']
        xMax = self.Stats['yAxis']['max']
        newData = []
        for i in range(len(data)):
            y1 = canv_utils.Point2Pixel(xMin, xMax, 0, self.height, data[i][0])
            y2 = canv_utils.Point2Pixel(xMin, xMax, 0, self.height, data[i][1])
            newData.append([y1, y2])

        return newData

    def convert_xAxis_pixels(self, data):
        xMin = self.Stats['xAxis']['min']
        xMax = self.Stats['xAxis']['max']
        newData = []
        for i in range(len(data)):
            newData.append(canv_utils.Point2Pixel(xMin, xMax, 0, self.width, data[i]))
        return newData

    def convert_yAxis_pixels(self, data):
        xMin = self.Stats['yAxis']['min']
        xMax = self.Stats['yAxis']['max']

        newData = []
        for i in range(len(data)):
            newData.append(canv_utils.Point2Pixel(xMin, xMax, 0, self.height, data[i]))

        return newData

    def draw(self):
        """
        Draw the shape, text, etc
        """
        self.Figure(grid=True)
        canv_utils.drawLine(self.canv, self.mDataX, self.mDataY, line_width=0.8, stroke=1)
