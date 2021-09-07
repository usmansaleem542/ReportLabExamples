from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, time
from reportlab.platypus import (Flowable)
from reportlab.graphics.charts.axes import Color

from common import canv_utils
import numpy as np
import math


class BPAreaGraph(Flowable):
    def __init__(self, data, width=500, height=200):
        Flowable.__init__(self)
        self.Stats = {}
        self.dataX = data['data']['time']
        self.dataY = data['data']['value']
        self.Q1 = data['data']['Q1']
        self.Q2 = data['data']['Q2']
        self.NormalRange = data['normal_range']

        self.width = width
        self.height = height
        self.text = data['title']
        self.styles = getSampleStyleSheet()
        self.aw = 0
        self.ah = 0
        self.InitStats()
        self.mDataX = self.convert_xAxis_pixels(self.dataX)
        self.mDataY = self.convert_yAxis_pixels(self.dataY)
        self.mDataQ1 = self.convert_QData_pixels(self.Q1)
        self.mDataQ2 = self.convert_QData_pixels(self.Q2)
        # self.Padding = {"left": 0, "right": 0, "top": 0, "bottom": 0}

    def InitStats(self):
        self.Stats['xAxis'] = {}
        self.Stats['yAxis'] = {}
        self.GetVerticalPosition()
        self.GetHorizontalPosition()

    def wrap(self, availWidth, availHeight):
        # print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height + 50

    def GetHorizontalPosition(self, minLimit=0, maxLimit=24, step=3):
        min_time = min(self.dataX)
        start = int(datetime.fromtimestamp(min_time).hour / step) * step
        end_dt = datetime.fromtimestamp(max(self.dataX))
        end = math.ceil((end_dt.hour + (end_dt.minute / 60)) / step) * step

        if end <= start:
            print("There Issue in Given Data For X Axis")
            exit()
        if start == minLimit:
            time_d = time.min
        else:
            time_d = time(hour=start)
        min_time = datetime.combine(datetime.fromtimestamp(min_time).date(), time_d)

        if end == maxLimit:
            time_d = time.max
        else:
            time_d = time(hour=end, second=0, microsecond=0)
        max_time = datetime.combine(min_time.date(), time_d)

        # print("X Min: ", minTime)
        # print("X Max: ", maxTime)

        self.Stats['xAxis']['min'] = min_time.timestamp()
        self.Stats['xAxis']['max'] = max_time.timestamp()
        self.Stats['xAxis']['pos'] = list(range(start, end + 1, step))

    def GetVerticalPosition(self, minLimit=None, maxLimit=None, step=50):
        max_v = max(max(self.dataY), np.max(self.Q1), np.max(self.Q2), max(self.NormalRange))
        min_v = min(min(self.dataY), np.min(self.Q1), np.min(self.Q2), min(self.NormalRange))
        min_v = math.floor(min_v / step) * step
        if minLimit is not None:
            min_v = min(minLimit, min_v)

        max_v = math.ceil(max_v / step) * step
        if maxLimit is not None:
            min_v = min(maxLimit, max_v)

        if min_v == max_v:
            print("There Issue in Given Data For Y Axis")
            exit()

        self.Stats['yAxis']['min'] = min_v
        self.Stats['yAxis']['max'] = max_v
        step = math.ceil(((max_v - min_v) * .10) / 50) * 50
        self.Stats['yAxis']['pos'] = list(range(min_v, max_v + 1, step))

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

    def DrawNormalRange(self, txt="Normal Range"):
        range_low = canv_utils.Point2Pixel(self.Stats['yAxis']['min'],
                                           self.Stats['yAxis']['max'], 0, self.height, self.NormalRange[0])

        range_high = canv_utils.Point2Pixel(self.Stats['yAxis']['min'], self.Stats['yAxis']['max'],
                                            0, self.height, self.NormalRange[1])

        self.canv.saveState()
        clr = np.array([3, 125, 80, 125]) / 255
        self.canv.setStrokeColor(Color(*clr))
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.setLineWidth(2)  # small lines
        self.canv.line(0, range_low, self.width + h, range_low)
        self.canv.line(0, range_high, self.width + h, range_high)

        diff = abs(range_low - range_high)

        font_size = min(10, max(5, int(
            diff * 0.12)))  # Calculating Suitable Font Size between 7-12 according to Range Difference

        self.canv.setFontSize(font_size)
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        y = range_low + (diff - w) / 2
        canv_utils.WriteText(self.canv, txt, x=self.width + h, y=y, rot=-90)
        self.canv.setFontSize(8)
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        canv_utils.WriteText(self.canv, self.NormalRange[0], self.width + (h * 4), range_low - (h / 2))
        canv_utils.WriteText(self.canv, self.NormalRange[1], self.width + (h * 4), range_high - (h / 2))
        self.canv.restoreState()

    def draw(self):
        """
        Draw the shape, text, etc
        """
        import numpy as np
        self.Figure(grid=True)

        if self.Q2 is not None:
            er_d = np.array(self.mDataQ2)
            x = np.append(self.mDataX, np.flip(self.mDataX))
            y = np.append(er_d[:, 0], np.flip(er_d[:, 1]))
            canv_utils.drawLine(self.canv, x, y, color=(0.16, 0.5, 0.72, 0.3), stroke=1, fill=1, style='dash')

        if self.Q1 is not None:
            er_d = np.array(self.mDataQ1)
            x = np.append(self.mDataX, np.flip(self.mDataX))
            y = np.append(er_d[:, 0], np.flip(er_d[:, 1]))
            canv_utils.drawLine(self.canv, x, y, color=(0.16, 0.5, 0.72, 0.4), stroke=0, fill=1)

        canv_utils.drawLine(self.canv, self.mDataX, self.mDataY)
        self.DrawNormalRange()
