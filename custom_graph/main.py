from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.platypus import (Flowable, Paragraph,
                                SimpleDocTemplate, Spacer)
from reportlab.graphics.charts.axes import Color

class GraphAxis(Flowable):
    def __init__(self, x=0, y=-0, width=500, height=350, text=""):
        Flowable.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.styles = getSampleStyleSheet()
        self.aw = 0
        self.ah = 0

    def wrap(self, availWidth, availHeight):
        print("w,h ", availWidth, availHeight)
        self.aw = availWidth
        self.ah = availHeight
        return self.width, self.height

    def grid(self, w, h):
        prev_color = self.canv._strokeColorObj
        self.canv.setStrokeColor(Color(0.1, 0.1, 0.1, 0.3))
        nC = int(self.width/w)
        nR = int(self.height/h)
        for col in range(nC):
            self.canv.line((col+1)*w, -3, (col+1)*w, self.height)
            self.canv.drawString((col+1)*w - 5,-20, str(col+1))

        for row in range(nR):
            self.canv.line(-3, (row+1)*h, self.width, (row+1)*h)
            self.canv.drawString(-20, (row+1)*h - 5, str(row+1))

        self.canv.setStrokeColor(Color(*prev_color))

    def grid2(self, w, h):
        prev_color = self.canv._strokeColorObj
        self.canv.setStrokeColor(Color(0.1, 0.1, 0.1, 0.3))
        nC = int(self.width/w)
        nR = int(self.height/h)
        args = [[0], [0]]
        for col in range(nC):
            args[0].append((col+1)*w)
            # self.canv.drawString((col+1)*w - 1.6, 0, '|')
            self.canv.line((col+1)*w, -3, (col+1)*w, 1)
            self.canv.drawString((col+1)*w - 5,-20, str(col+1))

        for row in range(nR):
            args[1].append((row+1)*h)
            self.canv.drawString(-3, (row+1)*h - 3.35, '-')
            self.canv.drawString(-20, (row+1)*h - 5, str(row+1))

        self.canv.grid(*args)
        self.canv.setStrokeColor(Color(*prev_color))

    def draw(self):
        """
        Draw the shape, text, etc
        """
        self.grid(30, 30)
        self.canv.line(0, -5, 0, self.height)
        self.canv.line(-5, 0, self.width, 0)
        # p = Paragraph(self.text, style=self.styles["Normal"])



doc = SimpleDocTemplate("custom_graph.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()
circle = GraphAxis(text="Custom Graph")
story.append(circle)

doc.build(story)
