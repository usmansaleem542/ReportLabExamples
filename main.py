from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from custom_graph.CanvasFigure import CanvasFigure
from custom_graph import graph_wrappers as graphP
from data import generator

doc = SimpleDocTemplate("ignore/custom_graph.pdf", pagesize=letter)
style = getSampleStyleSheet()
story = []
p = Paragraph("This is a table. " * 10, style['Normal'])
story.append(p)


refGraph = CanvasFigure([], [], width=500, height=250)

data = generator.GenerateData()
graph = graphP.GetBloodGlucoseGraph(data, (500, 250), boundary=True)

story.append(refGraph)
story.append(graph)
story.append(p)
s = Spacer(width=0, height=60)
doc.build(story)