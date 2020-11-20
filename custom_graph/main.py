from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from datetime import datetime
from reportlab.platypus import (Flowable, Paragraph,
                                SimpleDocTemplate, Spacer)
from reportlab.graphics.charts.axes import Color

class GraphAxis(Flowable):
    def __init__(self, dataX, dataY, errorRate=[], x=0, y=-0, width=500, height=350, text=""):
        Flowable.__init__(self)
        self.dataX = dataX
        self.dataY = dataY
        self.errorRate = errorRate

        self.width = width
        self.height = height
        self.text = text
        self.styles = getSampleStyleSheet()
        self.aw = 0
        self.ah = 0

        self.mDataX = self.convert_xAxis_pixels(dataX)
        self.mDataY = self.convert_yAxis_pixels(dataY)
        self.mDataErrorRate = self.convert_errorRate_pixels(errorRate)

    def wrap(self, availWidth, availHeight):
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height

    def Figure(self, w, h, grid=False):
        prev_color = self.canv._strokeColorObj
        self.canv.setStrokeColor(Color(0.1, 0.1, 0.1, 0.3))

        self.canv.line(0, -5, 0, self.height)
        self.canv.line(-5, 0, self.width, 0)

        nC = int(self.width/w)
        nR = int(self.height/h)
        for col in range(nC):
            if grid: self.canv.line((col+1)*w, -3, (col+1)*w, self.height)
            dtm = self.get_Point2Pixel(0, self.width, min(self.dataX), max(self.dataX), (col+1)*w)
            dtm = datetime.fromtimestamp(dtm)
            print(dtm)
            self.canv.drawString((col+1)*w - 5, -20, f'{dtm.hour}h')

        for row in range(nR):
            if grid: self.canv.line(-3, (row+1)*h, self.width, (row+1)*h)
            yVal = round(self.get_Point2Pixel(0, self.height, min(self.dataY), max(self.dataY), (row+1)*h))
            self.canv.drawString(-30, (row+1)*h - 5, str(yVal))

        self.canv.setStrokeColor(Color(*prev_color))

    def Point2Pixel(self, x1, x2, y1, y2, point):
        slope = (y2 - y1) / (x2 - x1)
        pixVal = y1 + slope * (point - x1)
        return pixVal

    def convert_errorRate_pixels(self, data):
        xMin = min(self.dataY)
        xMax = max(self.dataY)
        newData = []
        for i in range(len(data)):
            y1 = self.get_Point2Pixel(xMin, xMax, 0, self.height, data[i][0])
            y2 = self.get_Point2Pixel(xMin, xMax, 0, self.height, data[i][1])
            newData.append([y1, y2])

        return newData

    def convert_xAxis_pixels(self, data):
        # xMin = datetime(year=2000, month= 1, day= 1, hour=0, minute=0, second=0, microsecond=0).timestamp()
        # xMax = datetime(year=2000, month= 1, day= 1, hour=23, minute=59, second=59, microsecond=999999).timestamp()

        xMin = min(data)
        xMax = max(data)
        newData = []
        for i in range(len(data)):
            newData.append(self.Point2Pixel(xMin, xMax, 0, self.width, data[i]))
        return newData

    def convert_yAxis_pixels(self, data):
        xMin = min(data)
        xMax = max(data)

        newData = []
        for i in range(len(data)):
            newData.append(self.get_Point2Pixel(xMin, xMax, 0, self.height, data[i]))

        return newData

    def plot(self, x, y, color= (0, 0, 1, 0.4), fill=0, stroke=1):

        if len(x) != len(y):
            return
        print("Drawing")
        prev_color = self.canv._fillColorObj
        self.canv.setFillColor(Color(*color))
        self.canv.setLineWidth(1)  # small lines
        p = self.canv.beginPath()
        p.moveTo(x[0] , y[0])
        for i in range(len(x)):
            p.lineTo(x[i], y[i])

        self.canv.drawPath(p, stroke=stroke, fill=fill)
        self.canv.setFillColor(Color(*prev_color))
        self.canv._fillColorObj = prev_color
        p.close()

    def plotError(self, x, y, color= (0, 0, 1, 0.4), fill=0, stroke=1):

        if len(x) != len(y):
            return
        print("Drawing")
        prev_color = self.canv._fillColorObj
        self.canv.setFillColor(Color(*color))
        self.canv.setLineWidth(1)  # small lines
        p = self.canv.beginPath()
        p.moveTo(x[0] , y[0])
        for i in range(len(x)):
            p.lineTo(x[i], y[i])

        self.canv.drawPath(p, stroke=stroke, fill=fill)
        self.canv.setFillColor(Color(*prev_color))
        self.canv._fillColorObj = prev_color
        p.close()

    def draw2(self):
        """
        Draw the shape, text, etc
        """
        self.Figure(30, 30, True)

        import numpy as np
        time = np.arange(0, 10, 0.1)
        amplitude = np.sin(time)+2

        amplitudeU = np.sin(time)+2.5
        amplitudeD = np.sin(time)+1.5

        self.plot(np.append(x, np.flip(time)), np.append(amplitudeU, np.flip(amplitudeD)), color=(1,1,1,0.8), stroke=0, fill=1)
        self.plot(np.append(time, np.flip(time)), np.append(amplitudeU, np.flip(amplitudeD)), stroke=0, fill=1)
        self.plot(time, amplitude)
        # self.draw_line(time, amplitudeD, fill=1)

    def draw(self):
        """
        Draw the shape, text, etc
        """
        import numpy as np
        self.Figure(30, 30, True)
        self.plot(self.mDataX, self.mDataY)
        erD = np.array(self.mDataErrorRate)
        x = np.append(self.mDataX, np.flip(self.mDataX))
        y = np.append(erD[:, 0], np.flip(erD[:, 1]))
        self.plotError(x, y, stroke=0, fill=1)


doc = SimpleDocTemplate("custom_graph.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

dx = [946698831, 946710395, 946711366, 946720722, 946737503, 946738884, 946738973, 946747032, 946751234, 946752420]
dy = [72, 100, 75, 263, 95, 213, 319, 218, 124, 293]
errorRate = [[68, 74], [80, 120], [60, 95], [255, 270], [85, 105], [200, 230], [300, 325], [200, 230], [110, 145], [280, 300]]
circle = GraphAxis(dx, dy, errorRate=errorRate, text="Custom Graph")
story.append(circle)

doc.build(story)
