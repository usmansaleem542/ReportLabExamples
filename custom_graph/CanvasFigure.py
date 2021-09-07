from reportlab.platypus import Flowable

from common import canv_utils as canv_utils
from custom_graph.BPAreaGraph import BPAreaGraph


class CanvasFigure(Flowable):
    def __init__(self, data, width=600, height=500):
        Flowable.__init__(self)
        self.data = data
        self.width = width
        self.height = height
        self.Padding = {"left": 50, "right": 50, "top":50, "bottom": 50}
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
        self.setTitle("Blood Pressure Graph")
        self.setXlabel("Time")
        self.setYLabel("Blood Pressure")
        canv_utils.DrawRectangle(self.canv, (0, 0), (self.width, self.height))
        # canv_utils.DrawRectangle(self.canv, (self.pX, self.pY), (self.pWidth, self.pHeight), color=(0.0, 0.0, 0.0, 0.1), fill=1)
        flowable = BPAreaGraph(self.data, width=self.pWidth, height=self.pHeight)
        canv_utils.DrawCustomFlowable(self.canv, flowable, (self.pX, self.pY), (self.aw, self.ah))
