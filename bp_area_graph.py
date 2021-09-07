from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from custom_graph.CanvasFigure import CanvasFigure
from datetime import datetime
import json


doc = SimpleDocTemplate("ignore/custom_graph.pdf", pagesize=letter)
style = getSampleStyleSheet()
story = []

with open('sample_inputs/area_graph_data.json', 'r') as f:
    data = json.loads(f.read())

graph = CanvasFigure(data, width=500, height=250)
story.append(graph)
doc.build(story)
