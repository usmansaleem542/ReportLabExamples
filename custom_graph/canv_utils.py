from reportlab.graphics.charts.axes import Color
from reportlab.pdfbase import pdfmetrics

def Point2Pixel(x1, x2, y1, y2, point):
    slope = (y2 - y1) / (x2 - x1)
    pixVal = y1 + slope * (point - x1)
    return pixVal

def DrawLine(canv, xy, wh, color=(0 ,0 ,0 ,1)):
    canv.saveState()
    canv.setStrokeColor(Color(*color))
    canv.line(*xy, *wh)
    canv.restoreState()

def DrawRectangle(canv, xy, wh, stroke_color = (0.1, 0.1, 0.1, 0.9), color=(0.8, 0.1, 0.1, 0.9), fill=0, stroke=1):
    canv.saveState()
    canv.setStrokeColor(Color(*stroke_color))
    canv.setFillColor(Color(*color))
    p = canv.beginPath()
    p.rect(*xy, *wh)
    canv.drawPath(p, fill=fill, stroke=stroke)
    p.close()
    canv.restoreState()

def GetFontWidhHeight(txt, font_name, font_size):
    face = pdfmetrics.getFont(font_name).face
    ascent = (face.ascent * font_size) / 1000.0
    descent = (face.descent * font_size) / 1000.0
    descent = -descent
    height = ascent + descent
    width = pdfmetrics.stringWidth(txt, font_name, font_size)
    return width, height

def WriteText(canv, txt, x, y, rot=0):
    canv.saveState()
    canv.translate(x, y)
    canv.rotate(rot)
    canv.drawRightString(0, 0, str(txt))
    canv.restoreState()

def DrawCustomFlowable(canv, flowable, xy, availableWH):
    flowable.wrapOn(canv, *availableWH)
    flowable.drawOn(canv, *xy)
