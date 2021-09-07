from reportlab.platypus import (SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from custom_graph.LineGraph import LineGraph
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

for i in range(13):
    data = get_values(i)
    try:
        refGraph = LineGraph(data, width=500, height=100)
        story.append(refGraph)
        s = Spacer(width=0, height=60)
    except:
        pass

doc.build(story)
