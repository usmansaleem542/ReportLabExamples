from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from datetime import datetime, time
from reportlab.platypus import (Flowable, Paragraph,
                                SimpleDocTemplate, Spacer)
from reportlab.graphics.charts.axes import Color
from reportlab.pdfbase import pdfmetrics
import math
import numpy as np
from generator import *

class GraphAxis(Flowable):
    def __init__(self, data, x=0, y=-0, width=500, height=200):
        Flowable.__init__(self)
        self.Stats = {}
        self.Title = data['title']
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
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height + 50


    def GetHorizontalPosition(self, minLimit=0, maxLimit=24, step=3):
        minTime = min(self.dataX)
        start = int(datetime.fromtimestamp(minTime).hour / step) * step
        endDT = datetime.fromtimestamp(max(self.dataX))
        end = math.ceil((endDT.hour + (endDT.minute/60)) / step) * step

        if end <= start:
            print("There Issue in Given Data For X Axis")
            exit()
        if start == minLimit:
            timeD = time.min
        else:
            timeD = time(hour=start)
        minTime = datetime.combine(datetime.fromtimestamp(minTime).date(), timeD)

        if end == maxLimit:
            timeD = time.max
        else:
            timeD = time(hour=end, second=0, microsecond=0)
        maxTime = datetime.combine(minTime.date(), timeD)

        print("X Min: ", minTime)
        print("X Max: ", maxTime)

        self.Stats['xAxis']['min'] = minTime.timestamp()
        self.Stats['xAxis']['max'] = maxTime.timestamp()
        self.Stats['xAxis']['pos'] = list(range(start, end+1, step))

    def GetVerticalPosition(self, minLimit=None, maxLimit=None, step=50):
        maxV = max(max(self.dataY), np.array(self.Q1).max(), np.array(self.Q2).max())
        minV= min(min(self.dataY), np.array(self.Q1).min(), np.array(self.Q2).min())
        minV = math.floor(minV/step)*step
        if minLimit is not None:
            minV = min(minLimit, minV)

        maxV = math.ceil(maxV/step)*step
        if maxLimit is not None:
            minV = min(maxLimit, maxV)

        if minV == maxV:
            print("There Issue in Given Data For Y Axis")
            exit()

        self.Stats['yAxis']['min'] = minV
        self.Stats['yAxis']['max'] = maxV
        self.Stats['yAxis']['pos'] = list(range(minV, maxV+1, step))



    def DrawVGrid(self, grid=False):
        cols = self.Stats['xAxis']['pos']
        minTime = datetime.fromtimestamp(self.Stats['xAxis']['min'])
        maxTime = datetime.fromtimestamp(self.Stats['xAxis']['max'])
        w, h = self.GetFontWidhHeight('12', self.canv._fontname, self.canv._fontsize)
        for col in cols:
            if col == 24:
                timeD = time.max
            else:
                timeD = time(hour=col, second=0, microsecond=0)
            newT = datetime.combine(minTime.date(), timeD)
            posX = self.Point2Pixel(minTime.timestamp(), maxTime.timestamp(), 0, self.width, newT.timestamp())
            print(newT, posX, self.width)
            pos = [posX, -(h*2)]
            if grid: self.canv.line(pos[0], -(h/3), pos[0], self.height)
            labelStr = f'{newT.hour} {newT.strftime("%p").lower()}'
            self.canv.drawString(pos[0] - (h*1.2), pos[1], labelStr)

    def DrawHGrid(self, grid):
        rows = self.Stats['yAxis']['pos']
        minV = self.Stats['yAxis']['min']
        maxV = self.Stats['yAxis']['max']

        w, h = self.GetFontWidhHeight('12', self.canv._fontname, self.canv._fontsize)

        for rowV in rows:
            posY = self.Point2Pixel(minV, maxV, 0, self.height, rowV)
            pos = [-h*3, posY]
            if grid: self.canv.line(-(h/3), pos[1], self.width, pos[1])
            # yVal = round(self.Point2Pixel(0, self.height, min(self.dataY), max(self.dataY), pos[1]))
            # vPos.append(pos)
            self.canv.drawString(pos[0], pos[1] - (h/3), str(rowV))


    def setXlabel(self, txt):
        w, h = self.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.saveState()
        self.canv.translate((self.width/2) + (w/2), -(h*4))
        self.canv.rotate(0)
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()

    def setYLabel(self, txt):
        w, h = self.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.saveState()
        self.canv.translate(-(h*3), (self.height/2) + (w/2))
        self.canv.rotate(90)
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()


    def DrawRectangle(self, xy, wh, color=(0.1, 0.1, 0.1, 0.3), fill=0, stroke=1):
        self.canv.saveState()
        p = self.canv.beginPath()
        p.rect(*xy, *wh)
        self.canv.drawPath(p, fill=fill, stroke=stroke)
        p.close()
        self.canv.restoreState()

    def Figure(self, grid=False):
        self.DrawRectangle((0,0), (self.width, self.height))
        self.canv.saveState()
        self.canv.setStrokeColor(Color(0.1, 0.1, 0.1, 0.3))

        self.canv.setFontSize(9)
        self.DrawVGrid(grid)
        self.DrawHGrid(grid)

        self.canv.restoreState()

    def Point2Pixel(self, x1, x2, y1, y2, point):
        slope = (y2 - y1) / (x2 - x1)
        pixVal = y1 + slope * (point - x1)
        return pixVal

    def GetFontWidhHeight(self, txt, font_name, font_size):
        face = pdfmetrics.getFont(font_name).face
        ascent = (face.ascent * font_size) / 1000.0
        descent = (face.descent * font_size) / 1000.0
        descent = -descent
        height = ascent + descent
        width = pdfmetrics.stringWidth(txt, font_name, font_size)
        return width, height

    def convert_QData_pixels(self, data):
        xMin = self.Stats['yAxis']['min']
        xMax = self.Stats['yAxis']['max']
        newData = []
        for i in range(len(data)):
            y1 = self.Point2Pixel(xMin, xMax, 0, self.height, data[i][0])
            y2 = self.Point2Pixel(xMin, xMax, 0, self.height, data[i][1])
            newData.append([y1, y2])

        return newData

    def convert_xAxis_pixels(self, data):
        xMin = self.Stats['xAxis']['min']
        xMax = self.Stats['xAxis']['max']
        newData = []
        for i in range(len(data)):
            newData.append(self.Point2Pixel(xMin, xMax, 0, self.width, data[i]))
        return newData

    def convert_yAxis_pixels(self, data):
        xMin = self.Stats['yAxis']['min']
        xMax = self.Stats['yAxis']['max']

        newData = []
        for i in range(len(data)):
            newData.append(self.Point2Pixel(xMin, xMax, 0, self.height, data[i]))

        return newData

    def WriteText(self, txt, x, y, rot=0):
        self.canv.saveState()
        self.canv.translate(x, y)
        self.canv.rotate(rot)
        self.canv.drawRightString(0, 0, str(txt))
        self.canv.restoreState()

    def DrawNormalRange(self, txt = "Normal Range"):
        rangeLow = self.Point2Pixel(self.Stats['yAxis']['min'], self.Stats['yAxis']['max'], 0, self.height, self.NormalRange[0])
        rangeHigh = self.Point2Pixel(self.Stats['yAxis']['min'], self.Stats['yAxis']['max'], 0, self.height, self.NormalRange[1])

        self.canv.saveState()
        clr = np.array([3, 125, 80, 125])/255
        self.canv.setStrokeColor(Color(*clr))
        w, h = self.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.setLineWidth(2)  # small lines
        self.canv.line(0, rangeLow, self.width+h, rangeLow)
        self.canv.line(0, rangeHigh, self.width+h, rangeHigh)

        diff = abs(rangeLow - rangeHigh)
        y = rangeLow + abs(w - diff)/2
        self.WriteText(txt, x=self.width+h, y=y, rot=-90)
        self.canv.setFontSize(8)
        w, h = self.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.WriteText(self.NormalRange[0], self.width + (h*4), rangeLow - (h/2))
        self.WriteText(self.NormalRange[1], self.width + (h*4), rangeHigh - (h/2))
        self.canv.restoreState()

    def plot(self, x, y, color= (0, 0, 1, 0.4), fill=0, stroke=1, style=None):

        if len(x) != len(y):
            return
        print("Drawing")

        self.canv.saveState()
        if style == 'dash':
            self.canv.setStrokeColor(Color(*color))
            self.canv.setDash(6, 4)
        self.canv.setFillColor(Color(*color))
        self.canv.setLineWidth(2)  # small lines
        self.canv.setLineCap(1)
        self.canv.setLineJoin(1)
        p = self.canv.beginPath()
        p.moveTo(x[0] , y[0])
        for i in range(len(x)):
            p.lineTo(x[i], y[i])

        self.canv.drawPath(p, stroke=stroke, fill=fill)
        p.close()
        self.canv.restoreState()

    def draw(self):
        """
        Draw the shape, text, etc
        """
        import numpy as np
        self.Figure(grid=True)
        self.setXlabel("Time")
        self.setYLabel("Blood Pressure")

        if self.Q2 is not None:
            erD = np.array(self.mDataQ2)
            x = np.append(self.mDataX, np.flip(self.mDataX))
            y = np.append(erD[:, 0], np.flip(erD[:, 1]))
            self.plot(x, y, color= (0.16, 0.5, 0.72, 0.3), stroke=1, fill=1, style='dash')

        if self.Q1 is not None:
            erD = np.array(self.mDataQ1)
            x = np.append(self.mDataX, np.flip(self.mDataX))
            y = np.append(erD[:, 0], np.flip(erD[:, 1]))
            self.plot(x, y, color= (0.16, 0.5, 0.72, 0.4), stroke=0, fill=1)

        self.plot(self.mDataX, self.mDataY)
        self.DrawNormalRange()


import json
data = GenerateData('sample_data2.json', offset=30)
# with open('sample_data2.json', 'rb') as f:
#     data = json.load(f)

doc = SimpleDocTemplate("custom_graph.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

p = Paragraph("This is a table. " * 10, styles["Normal"])
story.append(p)
circle = GraphAxis(data, x=200, y=250)
s = Spacer(width=0, height=60)
story.append(circle)
story.append(s)
story.append(p)
doc.build(story)
