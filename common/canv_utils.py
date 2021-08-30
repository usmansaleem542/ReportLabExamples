from reportlab.graphics.charts.axes import Color
from reportlab.pdfbase import pdfmetrics
import math

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

def GetRotFontWidhHeight(canv, rot, txt, font_name, font_size):
    canv.saveState()
    face = pdfmetrics.getFont(font_name).face
    ascent = (face.ascent * font_size) / 1000.0
    descent = (face.descent * font_size) / 1000.0
    descent = -descent
    height = ascent + descent
    width = pdfmetrics.stringWidth(txt, font_name, font_size)
    h = height * abs(math.cos(rot)) + width * abs(math.sin(rot))
    w = width * abs(math.cos(rot)) + height * abs(math.sin(rot))
    canv.restoreState()
    return w, h

def WriteText(canv, txt, x, y, rot=0):
    canv.saveState()
    canv.translate(x, y)
    canv.rotate(rot)
    canv.drawRightString(0, 0, str(txt))
    canv.restoreState()

def WriteCenteredText(canv, txt, x, y, rot=-45):
    w, h = GetRotFontWidhHeight(canv, rot, txt, canv._fontname, canv._fontsize)
    canv.saveState()
    if rot < 0:
        canv.translate(x + (w/2), y-(h/2))
    else:
        canv.translate(x + (w/2), y+(h/2))
    canv.rotate(rot)
    canv.drawRightString(0, 0, str(txt))
    canv.restoreState()


def DrawCustomFlowable(canv, flowable, xy, availableWH):
    flowable.wrapOn(canv, *availableWH)
    flowable.drawOn(canv, *xy)


def drawLine(canv, x, y, color=(0, 0, 1, 0.4), fill=0, stroke=1, line_width=2, style=None):
    if len(x) != len(y):
        return

    canv.saveState()
    if style == 'dash':
        canv.setStrokeColor(Color(*color))
        canv.setDash(6, 4)
    canv.setFillColor(Color(*color))
    canv.setLineWidth(line_width)  # small lines
    canv.setLineCap(1)
    canv.setLineJoin(1)
    p = canv.beginPath()
    p.moveTo(x[0] , y[0])
    for i in range(len(x)):
        p.lineTo(x[i], y[i])

    canv.drawPath(p, stroke=stroke, fill=fill)
    p.close()
    canv.restoreState()
