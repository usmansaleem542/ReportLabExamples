from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from custom_graph.CanvasFigure import CanvasFigure
from custom_graph.Figure import CGFigure
from custom_graph import generator

doc = SimpleDocTemplate("custom_graph.pdf", pagesize=letter)
style = getSampleStyleSheet()
story = []
p = Paragraph("This is a table. " * 10, style['Normal'])
story.append(p)


refGraph = CanvasFigure([], [], width=500, height=250)

data = generator.GenerateData()
ax = CGFigure((500, 250), title="Graph Title", xlabel='Time', ylabel="Blood Sugar", boundary=True)
ax.fillbetween(data['data']['time'], data['data']['Q1'])
ax.fillbetween(data['data']['time'], data['data']['Q2'])
ax.plot(data['data']['time'], data['data']['value'])
ax.plotrange(data['normal_range'])
graph = ax.render()

story.append(refGraph)
story.append(graph)
story.append(p)
s = Spacer(width=0, height=60)
doc.build(story)