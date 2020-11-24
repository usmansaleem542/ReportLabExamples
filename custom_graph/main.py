from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from datetime import datetime, time
from reportlab.platypus import (Flowable, Paragraph,
                                SimpleDocTemplate, Spacer)
from reportlab.graphics.charts.axes import Color
from reportlab.pdfbase import pdfmetrics
import math

class GraphAxis(Flowable):
    def __init__(self, data, x=0, y=-0, width=500, height=350):
        Flowable.__init__(self)
        self.Stats = {}
        self.Title = data['title']
        self.dataX = data['time']
        self.dataY = data['value']
        self.errorRate = data['Q1']

        self.width = width
        self.height = height
        self.text = data['title']
        self.styles = getSampleStyleSheet()
        self.aw = 0
        self.ah = 0
        self.InitStats()
        self.mDataX = self.convert_xAxis_pixels(self.dataX)
        self.mDataY = self.convert_yAxis_pixels(self.dataY)
        self.mDataErrorRate = self.convert_errorRate_pixels(self.errorRate)

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
        end = math.ceil(datetime.fromtimestamp(max(self.dataX)).hour / step) * step

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

        self.Stats['xAxis']['min'] = minTime.timestamp()
        self.Stats['xAxis']['max'] = maxTime.timestamp()
        self.Stats['xAxis']['pos'] = list(range(start, end+1, 3))

    def GetVerticalPosition(self, minLimit=None, maxLimit=None, step=50):
        minV = int(min(self.dataY)/step)*step
        if minLimit is not None:
            minV = min(minLimit, minV)

        maxV = math.ceil(max(self.dataY)/step)*step
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

        # self.canv.line(0, -5, 0, self.height)
        # self.canv.line(-5, 0, self.width, 0)
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

    def convert_errorRate_pixels(self, data):
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

    def plot(self, x, y, color= (0, 0, 1, 0.4), fill=0, stroke=1):

        if len(x) != len(y):
            return
        print("Drawing")

        self.canv.saveState()
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
        if self.errorRate is not None:
            erD = np.array(self.mDataErrorRate)
            x = np.append(self.mDataX, np.flip(self.mDataX))
            y = np.append(erD[:, 0], np.flip(erD[:, 1]))
            self.plot(x, y, color= (0.5,0.8,0.9, 0.5), stroke=0, fill=1)

        self.plot(self.mDataX, self.mDataY)


import json

with open('sample_data2.json', 'rb') as f:
    data = json.load(f)

doc = SimpleDocTemplate("custom_graph.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()


dx = [946678831, 946710395, 946711366, 946720722, 946737503, 946738884, 946738973, 946747032, 946751234, 946752420]
dy = [355, 100, 75, 263, 95, 213, 319, 218, 124, 293]
errorRate = [[340, 370], [80, 120], [65, 105], [240, 280], [85, 105], [200, 230], [300, 325], [200, 230], [110, 145], [280, 300]]
p = Paragraph("This is a table. " * 10, styles["Normal"])
story.append(p)
circle = GraphAxis(data)
s = Spacer(width=0, height=60)
story.append(circle)
story.append(s)
story.append(p)
doc.build(story)
