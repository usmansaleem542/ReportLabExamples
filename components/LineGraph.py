from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Flowable

import numpy as np
from common import canv_utils


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
        self.Stroke = 1
        self.InitStats()

    def GetAboveBelow(self, ref, y, type):
        if isinstance(y, int): y = np.repeat(y, len(ref))
        if type == 'fillabove':
            index = np.where(y > ref)
        else:
            index = np.where(y < ref)
        y[index] = ref[index]
        return y

    def InitStats(self):
        self.Stats['xAxis'] = {}
        self.Stats['yAxis'] = {}

        self.Stats = self.CanvFig.dp.Stats

        if self.data['type'] ==  'fillbetween':
            self.Fill = 1
            self.Stroke = 0
            erD = np.array(self.data['y'])
            x = np.append(self.data['x'], np.flip(self.data['x']))
            y = np.append(erD[:, 0], np.flip(erD[:, 1]))
            self.mDataX = self.convert_to_pixels_1d(x, (self.Stats['xAxis']['min'], self.Stats['xAxis']['max']), (0, self.width))
            self.mDataY = self.convert_to_pixels_1d(y, (self.Stats['yAxis']['min'], self.Stats['yAxis']['max']), (0, self.height))

        elif self.data['type'] in ['fillabove', 'fillbelow']:
            self.Fill = 1
            self.Stroke = 0
            x = np.array(self.data['ref_x'])
            ref = np.array(self.data['ref_y'])
            erD = self.GetAboveBelow(ref, self.data['y'], self.data['type'])
            x = np.append(x, np.flip(x))
            y = np.append(ref, np.flip(erD))

            self.mDataX = self.convert_to_pixels_1d(x, (self.Stats['xAxis']['min'], self.Stats['xAxis']['max']), (0, self.width))
            self.mDataY = self.convert_to_pixels_1d(y, (self.Stats['yAxis']['min'], self.Stats['yAxis']['max']), (0, self.height))

        elif self.data['type'] ==  'lineplot':
            self.mDataX = self.convert_to_pixels_1d(self.data['x'], (self.Stats['xAxis']['min'], self.Stats['xAxis']['max']), (0, self.width))
            self.mDataY = self.convert_to_pixels_1d(self.data['y'], (self.Stats['yAxis']['min'], self.Stats['yAxis']['max']), (0, self.height))

        else:
            print("Currently We Don't Support ", self.data['type'], "Graph")
            exit()

    def wrap(self, availWidth, availHeight):
        # print("w,h ", availWidth, availHeight)
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
            newData.append(
                canv_utils.Point2Pixel(sourceRange[0], sourceRange[1], targetRange[0], targetRange[1], data[i]))
        return newData

    def GetRandomColor(self):
        return (round(np.random.rand(), 1), round(np.random.rand(), 1),
                              round(np.random.rand(), 1), 1.0)
    def draw(self):
        color = self.data['args'].get('color', None)
        if color is None:
            color = self.GetRandomColor()
        canv_utils.drawLine(self.canv, self.mDataX, self.mDataY, color= color, stroke=self.Stroke, fill=self.Fill)

