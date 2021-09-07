from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from custom_graph.CanvasFigure import CanvasFigure
from data import generator
from datetime import datetime


doc = SimpleDocTemplate("../ignore/custom_graph.pdf", pagesize=letter)
style = getSampleStyleSheet()
story = []
p = Paragraph("This is a table. " * 10, style['Normal'])
story.append(p)

start = datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
end = datetime(year=2000, month=1, day=1, hour=23, minute=59, second=59, microsecond=999999).timestamp()
data = generator.GenerateData(start, end)

graph = CanvasFigure(data, width=500, height=250)
story.append(graph)
story.append(p)
s = Spacer(width=0, height=60)
doc.build(story)
