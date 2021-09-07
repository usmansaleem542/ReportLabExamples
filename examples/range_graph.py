from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from custom_graph.RangeGraph import RangeGraph
from datetime import datetime
import pandas as pd
import json


def get_values():
    with open('../sample_inputs/range_graph.json', 'r') as f:
        range_graph = json.loads(f.read())

    dt = pd.DataFrame(range_graph)
    return dt


doc = SimpleDocTemplate("../ignore/custom_graph.pdf", pagesize=letter)
style = getSampleStyleSheet()
story = []

start = datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
end = datetime(year=2000, month=1, day=2, hour=0, minute=0, second=0, microsecond=0).timestamp()

df = get_values()
refGraph = RangeGraph(df, x=100, y=100, width=30, height=250)
story.append(refGraph)
s = Spacer(width=0, height=60)

doc.build(story)
