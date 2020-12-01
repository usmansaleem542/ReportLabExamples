from reportlab.platypus import Flowable
from reportlab.graphics.charts.axes import Color
from reportlab.lib.styles import getSampleStyleSheet
import numpy as np

from common import canv_utils


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
        # print("w,h ", availWidth, availHeight)
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
        canv_utils.WriteText(self.canv, txt, x=self.width + h, y=y, rot=-90)
        self.canv.setFontSize(8)
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        canv_utils.WriteText(self.canv, self.NormalRange[0], self.width + (h * 4), rangeLow - (h / 2))
        canv_utils.WriteText(self.canv, self.NormalRange[1], self.width + (h * 4), rangeHigh - (h / 2))
        self.canv.restoreState()

    def draw(self):
        self.DrawNormalRange(self.data.get("txt", "Range"))

