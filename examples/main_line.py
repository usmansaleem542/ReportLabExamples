from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from custom_graph.LineGraph import LineGraph
from datetime import datetime
import pandas as pd
import json


def get_values(index):
    with open('../sample_inputs/line_data.json', 'r') as f:
        line_graph = json.loads(f.read())

    dt = pd.DataFrame(line_graph[index]['data'])
    data = {'title': 'Monday', 'xLabel': 'Time', 'yLabel': 'Blood Pressure', 'data': {}}
    data['data']['time'] = dt.value_x_axis.values - 18000
    data['data']['value'] = dt.value_y_axis.values

    return data


doc = SimpleDocTemplate("../ignore/custom_graph.pdf", pagesize=letter)
style = getSampleStyleSheet()
story = []
p = Paragraph("This is a table. " * 10, style['Normal'])
story.append(p)

start = datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0, microsecond=0).timestamp()
end = datetime(year=2000, month=1, day=2, hour=0, minute=0, second=0, microsecond=0).timestamp()

for i in range(13):
    data = get_values(i)
    try:
        refGraph = LineGraph(data, width=500, height=100)
        story.append(refGraph)
        s = Spacer(width=0, height=60)
    except:
        pass

doc.build(story)
