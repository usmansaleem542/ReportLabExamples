from reportlab.platypus import Flowable

from custom_graph import generator
from custom_graph import canv_utils as canv_utils
from custom_graph.custom_graphs import Grid, LineGraph
from custom_graph.BPGraph import BPGraph

class CanvasFigure2(Flowable):
    def __init__(self, dp):
        Flowable.__init__(self)
        self.dp = dp
        self.Init()

    def Init(self):
        self.width = self.dp.FigSize[0]
        self.height = self.dp.FigSize[1]
        self.pX = self.dp.PLeft
        self.pY = self.dp.PBottom
        self.pHeight = self.height - (self.dp.PTop + self.dp.PBottom)
        self.pWidth = self.width - (self.dp.PLeft + self.dp.PRight)

    def wrap(self, availWidth, availHeight):
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height

    def setXlabel(self, txt):
        self.canv.saveState()
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.translate((self.pWidth/2) + (w/2)+self.dp.PLeft, max(0, abs(h-self.dp.PBottom)*0.3))
        self.canv.rotate(0)
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()

    def setYLabel(self, txt):
        self.canv.saveState()
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        self.canv.translate(max(0, abs(h-self.dp.PLeft)*0.5), (self.pHeight/2) + (w/2)+self.dp.PBottom)
        self.canv.rotate(90)
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()

    def setTitle(self, txt):
        self.canv.saveState()
        w, h = canv_utils.GetFontWidhHeight(txt, self.canv._fontname, self.canv._fontsize)
        x = (self.pWidth/2) + (w/2)+self.dp.PLeft

        self.canv.translate(x, min(self.height-h, self.height - (self.dp.PTop)/2))
        self.canv.drawRightString(0, 0, txt)
        self.canv.restoreState()

    def draw(self):
        """
        Draw the shape, text, etc
        """
        if self.dp.Title is not None: self.setTitle(self.dp.Title)
        if self.dp.xLabel is not None: self.setXlabel(self.dp.xLabel)
        if self.dp.yLabel is not None: self.setYLabel(self.dp.yLabel)
        if self.dp.Boundary: canv_utils.DrawRectangle(self.canv, (0, 0), (self.width, self.height))

        data = generator.GenerateData()

        flowable = Grid(self, width=self.pWidth, height=self.pHeight)
        canv_utils.DrawCustomFlowable(self.canv, flowable, (self.pX, self.pY), (self.aw, self.ah))

        for gd in self.dp.Plots:
            if gd['type'] in ['lineplot', 'fillbetween']:
                flowable = LineGraph(self, gd, width=self.pWidth, height=self.pHeight)
                canv_utils.DrawCustomFlowable(self.canv, flowable, (self.pX, self.pY), (self.aw, self.ah))

        # for graphs in self.dp.Plots:
        #     if 'lineplot' in graphs:
        # flowable = LineGraph(self, data, width=self.pWidth, height=self.pHeight)
        # canv_utils.DrawCustomFlowable(self.canv, flowable, (self.pX, self.pY), (self.aw, self.ah))

