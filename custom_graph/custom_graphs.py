from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (Flowable, Paragraph, SimpleDocTemplate, Spacer)
from reportlab.graphics.charts.axes import Color

import numpy as np
from custom_graph import canv_utils

class Grid(Flowable):
    def __init__(self, canvFig, width=500, height=250):
        Flowable.__init__(self)
        self.Stats = {}
        self.CanvFig = canvFig

        self.width = width
        self.height = height
        self.aw = 0
        self.ah = 0
        self.InitStats()

    def InitStats(self):
        self.Stats['xAxis'] = {}
        self.Stats['yAxis'] = {}
        self.Stats = self.CanvFig.dp.Stats

    def wrap(self, availWidth, availHeight):
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height + 50

    def DrawVGrid(self, grid=True):
        from datetime import datetime
        cols = self.Stats['xAxis']['major']
        minTime = self.Stats['xAxis']['min']
        maxTime = self.Stats['xAxis']['max']
        w, h = canv_utils.GetFontWidhHeight('12', self.canv._fontname, self.canv._fontsize)
        for col in cols:
            posX = canv_utils.Point2Pixel(minTime, maxTime, 0, self.width, col)
            pos = [posX, -(h*2)]
            if grid: self.canv.line(pos[0], -(h/3), pos[0], self.height)
            strLabel = datetime.fromtimestamp(col).strftime('%I %P')
            self.canv.drawString(pos[0] - (h*1.2), pos[1], strLabel)

    def DrawHGrid(self, grid=True):
        rows = self.Stats['yAxis']['major']
        minV = self.Stats['yAxis']['min']
        maxV = self.Stats['yAxis']['max']

        w, h = canv_utils.GetFontWidhHeight('12', self.canv._fontname, self.canv._fontsize)

        for rowV in rows:
            posY = canv_utils.Point2Pixel(minV, maxV, 0, self.height, rowV)
            pos = [-h*3, posY]
            if grid: self.canv.line(-(h/3), pos[1], self.width, pos[1])
            self.canv.drawString(pos[0], pos[1] - (h/3), str(rowV))

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

        canv_utils.DrawRectangle(self.canv, (0,0), (self.width, self.height))
        self.canv.saveState()
        self.canv.setStrokeColor(Color(0.1, 0.1, 0.1, 0.3))
        self.canv.setFontSize(9)
        self.DrawVGrid()
        self.DrawHGrid()
        self.canv.restoreState()

class LineGraph(Flowable):
    def __init__(self, canvFig, data, width=500, height=200):
        Flowable.__init__(self)
        self.Stats = {}
        self.data = data
        self.CanvFig = canvFig
        self.width = width
        self.height = height
        self.styles = getSampleStyleSheet()
        self.aw = 0
        self.ah = 0
        self.Fill = 0
        self.FillColor = (0.16, 0.5, 0.72, 0.4)
        self.Stroke = 1
        self.InitStats()
        # self.Padding = {"left": 0, "right": 0, "top": 0, "bottom": 0}

    def InitStats(self):
        self.Stats['xAxis'] = {}
        self.Stats['yAxis'] = {}

        self.Stats = self.CanvFig.dp.Stats

        if self.data['type'] ==  'fillbetween':
            self.Fill = 1
            self.FillColor = (0.16, 0.5, 0.72, 0.4)
            self.Stroke = 0
            erD = np.array(self.data['y'])
            x = np.append(self.data['x'], np.flip(self.data['x']))
            y = np.append(erD[:, 0], np.flip(erD[:, 1]))
            self.mDataX = self.convert_to_pixels_1d(x, (self.Stats['xAxis']['min'], self.Stats['xAxis']['max']), (0, self.width))
            self.mDataY = self.convert_to_pixels_2d(y, (self.Stats['yAxis']['min'], self.Stats['yAxis']['max']), (0, self.height))

        elif self.data['type'] ==  'lineplot':
            self.mDataX = self.convert_to_pixels_1d(self.data['x'], (self.Stats['xAxis']['min'], self.Stats['xAxis']['max']), (0, self.width))
            self.mDataY = self.convert_to_pixels_1d(self.data['y'], (self.Stats['yAxis']['min'], self.Stats['yAxis']['max']), (0, self.height))

        else:
            print("Currently We Don't Support ", self.data['type'], "Graph")
            exit()

    def wrap(self, availWidth, availHeight):
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height + 50


    def convert_to_pixels_2d(self, data, sourceRange, targetRange):
        newData = []
        for i in range(len(data)):
            y1 = canv_utils.Point2Pixel(sourceRange[0], sourceRange[1], targetRange[0], targetRange[1], data[i][0])
            y2 = canv_utils.Point2Pixel(sourceRange[0], sourceRange[1], targetRange[0], targetRange[1], data[i][1])
            newData.append([y1, y2])

        return newData


    def convert_to_pixels_1d(self, data, sourceRange, targetRange):
        newData = []
        for i in range(len(data)):
            newData.append(canv_utils.Point2Pixel(sourceRange[0], sourceRange[1], targetRange[0], targetRange[1], data[i]))
        return newData

    def draw(self):
        canv_utils.drawLine(self.canv, self.mDataX, self.mDataY, color= self.FillColor, stroke=self.Stroke, fill=self.Fill)

