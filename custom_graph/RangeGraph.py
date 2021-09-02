from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (Flowable)
from reportlab.graphics.charts.axes import Color

from common import canv_utils
import math


class RangeGraph(Flowable):
    def __init__(self, df, x=0, y=0, width=50, height=200):
        Flowable.__init__(self)
        self.Stats = {}
        self.data = df

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.styles = getSampleStyleSheet()
        self.aw = 0
        self.ah = 0
        self.Colors = [(0.7, 0.0, 0.0, 0.9), (0.9, 0.20, 0.25, 0.9), (0.45, 0.7, 0.35, 0.9),
                       (0.9, 0.8, 0.15, 0.9), (0.9, 0.55, 0.15, 0.9)]

        # self.Colors = [(0.65, 0.82, 0.55), (0.97, 0.52, 0.32, 0.9), (0.97, 0.82, 0.20, 0.9),
        #                (0.62, 0.56, 0.67, 0.9), (0.25, 0.33, 0.86, 0.9)]

        # self.Colors = [(0.53, 0.53, 0.53), (0.47, 0.8, 0.7, 0.9), (0.57, 0.79, 0.82, 0.9),
        #                (0.84, 0.84, 0.15, 0.9), (0.91, 0.45, 0.30, 0.9)]

        self.TextPos = [0.1, 0.3, 0.5, 0.7, 0.9]

        self.InitStats()

    def InitStats(self):
        self.Stats['xAxis'] = {}
        self.Stats['yAxis'] = {}

    def wrap(self, available_width, available_height):
        self.aw = available_width
        self.ah = available_height
        return self.width, self.height + 50

    def Figure(self):
        pass
        # canv_utils.DrawRectangle(self.canv, (self.x, -self.y), (self.width, self.height))

    def DrawActual(self, x, y, border=False):
        current = 0
        font_size = 10

        canv_utils.WriteText(self.canv, "Actual", x=x+35, y=y+70, rot=-0, font_size=15)
        for i in range(len(self.data)):
            height = self.height * (self.data.iloc[i].actual / 100)
            text_vloc = -(y - (self.height * self.TextPos[i]))
            center_of_graph = -(y - current) + (height / 2)

            canv_utils.DrawLine(self.canv, (x - font_size - 18, text_vloc), (x, center_of_graph), color=self.Colors[i])
            canv_utils.WriteText(self.canv, self.data.iloc[i].range, x=x - font_size - 20, y=text_vloc,
                                 rot=-0, font_size=font_size)

            # canv_utils.DrawLine(self.canv, (x + self.width, center_of_graph),
            #                     (x + font_size + self.width + 18, text_vloc), color=self.Colors[i])
            # canv_utils.WriteLeftAlignedText(self.canv, self.data.iloc[i].category, x=x + font_size + self.width + 20,
            #                                 y=text_vloc, rot=-0, font_size=font_size)

            canv_utils.DrawRectangle(self.canv, (x, -(y - current)), (self.width, height),
                                     fill=1, stroke=0, color=self.Colors[i])
            current += height

    def DrawTarget(self, x, y):
        current = 0
        font_size = 10

        canv_utils.WriteText(self.canv, "Target", x=x+35, y=y+70, rot=-0, font_size=15)
        for i in range(len(self.data)):
            height = self.height * (self.data.iloc[i].target / 100)
            text_vloc = -(y - (self.height * self.TextPos[i]))
            center_of_graph = -(y - current) + (height / 2)

            # canv_utils.DrawLine(self.canv, (x - font_size - 18, text_vloc), (x, center_of_graph), color=self.Colors[i])
            # canv_utils.WriteText(self.canv, self.data.iloc[i].range, x=x - font_size - 20, y=text_vloc,
            #                      rot=-0, font_size=font_size)

            canv_utils.DrawLine(self.canv, (x + self.width, center_of_graph),
                                (x + font_size + self.width + 18, text_vloc), color=self.Colors[i])
            canv_utils.WriteLeftAlignedText(self.canv, self.data.iloc[i].category, x=x + font_size + self.width + 20,
                                            y=text_vloc, rot=-0, font_size=font_size)

            canv_utils.DrawRectangle(self.canv, (x, -(y - current)), (self.width, height),
                                     fill=1, stroke=0, color=self.Colors[i])
            current += height

    def draw(self):
        """
        Draw the shape, text, etc
        """
        self.Figure()

        self.DrawActual(self.x, self.y)
        self.DrawTarget(self.x+70, self.y)
        canv_utils.DrawRectangle(self.canv, (self.x, -self.y), (self.width, self.height))
        canv_utils.DrawRectangle(self.canv, (self.x + 70, -self.y), (self.width, self.height))
