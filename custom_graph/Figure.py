from reportlab.platypus import (Flowable, Paragraph, SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.charts.axes import Color
from reportlab.lib.pagesizes import letter

from custom_graph import generator
from custom_graph import canv_utils as canv_utils
from custom_graph.BPGraph import BPGraph


class TestFlowable(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height

    def draw(self):
        canv_utils.DrawRectangle(self.canv, (0, 0), (self.width, self.height), color=(0.1, 0.2, 0.9, 0.9), fill=1)

class Figure(Flowable):
    def __init__(self, dataX, dataY, width=500, height=600):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.dataX = dataX
        self.dataY = dataY
        self.Padding = {"left": 50, "right": 40, "top": 10, "bottom": 50}
        self.Init()

    def Init(self):
        self.pX = self.Padding['left']
        self.pY = self.Padding['bottom']
        self.pHeight = self.height - (self.Padding['top'] + self.Padding['bottom'])
        self.pWidth = self.width - (self.Padding['left'] + self.Padding['right'])


    def wrap(self, availWidth, availHeight):
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height


    def DrawMinor(self, data):
        for dp in data:
            canv_utils.DrawLine(self.canv, (self.pX, self.pY), (self.pWidth, self.pHeight/dp))

    def DrawMajor(self):
        pass

    def draw(self):
        """
        Draw the shape, text, etc
        """
        canv_utils.DrawRectangle(self.canv, (0, 0), (self.width, self.height))
        canv_utils.DrawRectangle(self.canv, (self.pX, self.pY), (self.pWidth, self.pHeight), color=(0.0, 0.0, 0.0, 0.1), fill=1)
        data = generator.GenerateData()
        flowable = BPGraph(data, width=self.pWidth, height=self.pHeight)
        canv_utils.DrawCustomFlowable(self.canv, flowable, (self.pX, self.pY), (self.aw, self.ah))
        #
        # self.DrawMinor([1.5, 2, 3, 5])
