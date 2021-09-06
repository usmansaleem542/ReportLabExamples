from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (Flowable)
from reportlab.graphics.charts.axes import Color

from common import canv_utils


class BarGraphC(Flowable):
    def __init__(self, data, width=500, height=200):
        Flowable.__init__(self)
        self.Stats = {}
        self.data = data
        self.width = width
        self.height = height
        self.styles = getSampleStyleSheet()
        self.aw = 0
        self.ah = 0
        self.InitStats()
        self.Colors = [(0.7, 0.0, 0.0, 0.9), (0.9, 0.20, 0.25, 0.9), (0.45, 0.7, 0.35, 0.9),
                       (0.9, 0.8, 0.15, 0.9), (0.9, 0.55, 0.15, 0.9)]

    def InitStats(self):
        self.Stats['xAxis'] = {}
        self.Stats['yAxis'] = {}
        self.Stats['xAxis']['min'] = 0
        self.Stats['xAxis']['max'] = len(self.data)
        self.Stats['yAxis']['min'] = 0
        self.Stats['yAxis']['max'] = 100
        self.Stats['xAxis']['major_size'] = self.width / len(self.data)
        for i in range(len(self.data)):
            row = self.data.iloc[i]
            self.Stats['yAxis']['max'] = max(self.Stats['yAxis']['max'], row.actual, row.target)

    def wrap(self, available_width, available_height):
        self.aw = available_width
        self.ah = available_height
        return self.width, self.height + 50

    def DrawVGrid(self, grid=False):
        cols_vals = list(range(0, len(self.data.category), 1))
        min_v = self.Stats['xAxis']['min']
        max_v = self.Stats['xAxis']['max']
        w, h = canv_utils.GetFontWidhHeight('12', self.canv._fontname, self.canv._fontsize)
        pixel_pos = []
        for colV in cols_vals:
            pos_x = canv_utils.Point2Pixel(min_v, max_v, 0, self.width, colV)
            pos = [pos_x, -(h * 2)]
            if grid: self.canv.line(pos[0], -(h / 3), pos[0], self.height)
            label_str = self.data.iloc[colV].category
            pixel_pos.append(pos + [label_str])
        pixel_pos.append([self.width, 0, ''])

        for i in range(len(pixel_pos)-1):
            pos = pixel_pos[i]
            str_w, str_h = canv_utils.GetFontWidhHeight(pos[2], self.canv._fontname, self.canv._fontsize)
            diff = pixel_pos[i+1][0] - pos[0]
            self.canv.drawString(pos[0] + (diff-str_w)/2, pos[1], pos[2])

    def DrawHGrid(self, grid):
        min_v = self.Stats['yAxis']['min']
        max_v = self.Stats['yAxis']['max']
        rows = list(range(0, max_v+1, 20))

        w, h = canv_utils.GetFontWidhHeight('120', self.canv._fontname, self.canv._fontsize)

        for rowV in rows:
            pos_y = canv_utils.Point2Pixel(min_v, max_v, 0, self.height, rowV)
            pos = [-h * 3, pos_y]
            if grid: self.canv.line(-(h / 3), pos[1], self.width, pos[1])
            self.canv.drawString(pos[0], pos[1] - (h / 3), str(rowV))

    def Figure(self, grid=False):
        canv_utils.DrawRectangle(self.canv, (0, 0), (self.width, self.height), stroke_color=(0.1, 0.1, 0.1, 0.3))
        self.canv.saveState()
        self.canv.setStrokeColor(Color(0.1, 0.1, 0.1, 0.3))
        self.canv.setFontSize(10)
        self.DrawVGrid(grid)
        self.DrawHGrid(grid)
        self.canv.restoreState()

    def draw(self):
        """
        Draw the shape, text, etc
        """
        self.Figure(grid=True)
        area = self.Stats['xAxis']['major_size']
        padding = 0.07
        center_space = 0.07
        padding_size = padding*area
        center_size = center_space*area
        bar_size = (area - (padding_size*2 + center_size))/2

        self.canv.saveState()
        self.canv.setFontSize(10)
        for i in range(len(self.data)):
            data_row = self.data.iloc[i]
            actual = canv_utils.Point2Pixel(0, self.Stats['yAxis']['max'], 0, self.height, max(data_row.actual, 0.2))
            target = canv_utils.Point2Pixel(0, self.Stats['yAxis']['max'], 0, self.height, max(data_row.target, 0.2))
            xy = (padding_size + area * i, 0)
            wh = (bar_size, actual)

            xy2 = (padding_size + center_size + bar_size + area * i, 0)
            wh2 = (bar_size, target)

            # print("XY: ", xy)
            # print("WH: ", wh)
            # print("bar_size: ", bar_size, "padding_size: ", padding_size, "center_size",  center_size)
            # Actual Bar
            w_txt, h_txt = canv_utils.GetFontWidhHeight(f"{data_row.actual}%", self.canv._fontname, self.canv._fontsize)
            canv_utils.DrawRectangle(self.canv, xy, wh, fill=1, color=self.Colors[i], stroke=0)
            canv_utils.WriteText(self.canv, f"{data_row.actual}%", xy[0]+wh[0]/2 + w_txt/2, wh[1]/2, rot=0)

            # Target Bar
            w_txt, h_txt = canv_utils.GetFontWidhHeight(f"{data_row.target}%", self.canv._fontname, self.canv._fontsize)
            canv_utils.DrawRectangle(self.canv, xy2, wh2, fill=1, color=self.Colors[i], stroke=0)
            canv_utils.WriteText(self.canv, f"{data_row.target}%", xy2[0]+wh2[0]/2 + w_txt/2, wh2[1]/2, rot=0)

        self.canv.restoreState()


class BarGraph(Flowable):
    def __init__(self, data, width=600, height=500):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.data = data
        self.Padding = {"left": 0, "right": 0, "top":20, "bottom": 0}
        self.pX = self.Padding['left']
        self.pY = self.Padding['bottom']
        self.pHeight = self.height - (self.Padding['top'] + self.Padding['bottom'])
        self.pWidth = self.width - (self.Padding['left'] + self.Padding['right'])

    def wrap(self, availWidth, availHeight):
        # print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height

    def setXlabel(self, txt):
        self.canv.saveState()
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.translate((self.pWidth/2) + (w/2)+self.Padding['left'], max(0, abs(h-self.Padding['bottom'])*0.3))
        self.canv.rotate(0)
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()

    def setYLabel(self, txt):
        self.canv.saveState()
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.translate(max(0, abs(h-self.Padding['left'])*0.5), (self.pHeight/2) + (w/2)+self.Padding['bottom'])
        self.canv.rotate(90)
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()

    def setTitle(self, txt):
        self.canv.saveState()
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        x = (self.pWidth/2) + (w/2)+self.Padding['left']

        self.canv.translate(x, min(self.height-h, self.height - (self.Padding['top'])/2))
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()

    def draw(self):
        """
        Draw the shape, text, etc
        """
        self.setTitle("T: Target | A: Actual")
        # self.setXlabel("Time")
        # self.setYLabel("Blood Pressure")
        flowable = BarGraphC(self.data, width=self.pWidth, height=self.pHeight)
        canv_utils.DrawCustomFlowable(self.canv, flowable, (self.pX, self.pY), (self.aw, self.ah))