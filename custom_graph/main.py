from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from custom_graph.Figure import Figure


doc = SimpleDocTemplate("custom_graph.pdf", pagesize=letter)
style = getSampleStyleSheet()
story = []
p = Paragraph("This is a table. " * 10, style['Normal'])
story.append(p)
dataX = [1, 2, 3, 4, 5]
dataY = [1, 2, 3, 4, 5]
graph = Figure(dataX, dataY, width=500, height=250)
story.append(graph)
story.append(p)
s = Spacer(width=0, height=60)
doc.build(story)