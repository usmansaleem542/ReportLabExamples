from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (Flowable, Paragraph, SimpleDocTemplate, Spacer)
from reportlab.graphics.charts.axes import Color

import numpy as np
from custom_graph import canv_utils

class DrawAxis(Flowable):
    def __init__(self, canvFig, Grid=False, width=500, height=250):
        Flowable.__init__(self)
        self.Stats = {}
        self.CanvFig = canvFig
        self.Grid = Grid
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
        gridH = 0
        if grid: gridH = self.height
        for col in cols:
            posX = canv_utils.Point2Pixel(minTime, maxTime, 0, self.width, col)
            pos = [posX, -(h*2)]
            self.canv.line(pos[0], -(h/3), pos[0], gridH)
            strLabel = datetime.fromtimestamp(col).strftime('%I %P')
            self.canv.drawString(pos[0] - (h*1.2), pos[1], strLabel)

    def DrawHGrid(self, grid=True):
        rows = self.Stats['yAxis']['major']
        minV = self.Stats['yAxis']['min']
        maxV = self.Stats['yAxis']['max']

        w, h = canv_utils.GetFontWidhHeight('12', self.canv._fontname, self.canv._fontsize)
        gridW = 0
        if grid: gridW = self.width

        for rowV in rows:
            posY = canv_utils.Point2Pixel(minV, maxV, 0, self.height, rowV)
            pos = [-h*3, posY]
            self.canv.line(-(h/3), pos[1], gridW, pos[1])
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
        self.DrawVGrid(self.Grid)
        self.DrawHGrid(self.Grid)
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
            from datetime import datetime
            print("==========", datetime.fromtimestamp(x.max()))
            y = np.append(erD[:, 0], np.flip(erD[:, 1]))
            self.mDataX = self.convert_to_pixels_1d(x, (self.Stats['xAxis']['min'], self.Stats['xAxis']['max']), (0, self.width))
            self.mDataY = self.convert_to_pixels_1d(y, (self.Stats['yAxis']['min'], self.Stats['yAxis']['max']), (0, self.height))

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


class RangePlot(Flowable):
    def __init__(self, canvFig, data, width=500, height=200):
        Flowable.__init__(self)
        self.Stats = {}
        self.data = data
        self.NormalRange = data['y']
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

    def wrap(self, availWidth, availHeight):
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height + 50


    def DrawNormalRange(self, txt):
        rangeLow = canv_utils.Point2Pixel(self.Stats['yAxis']['min'], self.Stats['yAxis']['max'], 0, self.height, self.NormalRange[0])
        rangeHigh = canv_utils.Point2Pixel(self.Stats['yAxis']['min'], self.Stats['yAxis']['max'], 0, self.height, self.NormalRange[1])

        self.canv.saveState()
        clr = np.array([3, 125, 80, 125])/255
        self.canv.setStrokeColor(Color(*clr))
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.setLineWidth(2)  # small lines
        self.canv.line(0, rangeLow, self.width+h, rangeLow)
        self.canv.line(0, rangeHigh, self.width+h, rangeHigh)

        diff = abs(rangeLow - rangeHigh)

        fontSize = min(10, max(5, int(diff*0.12)))  # Calculating Suitable Font Size between 7-12 according to Range Difference

        self.canv.setFontSize(fontSize)
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        y = rangeLow + (diff - w)/2
        canv_utils.WriteText(self.canv, txt, x=self.width+h, y=y, rot=-90)
        self.canv.setFontSize(8)
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        canv_utils.WriteText(self.canv, self.NormalRange[0], self.width + (h*4), rangeLow - (h/2))
        canv_utils.WriteText(self.canv, self.NormalRange[1], self.width + (h*4), rangeHigh - (h/2))
        self.canv.restoreState()

    def draw(self):
        self.DrawNormalRange(self.data.get("txt", "Range"))

