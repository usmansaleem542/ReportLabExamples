from reportlab.platypus import (SimpleDocTemplate, Spacer)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

from custom_graph.LineGraph import LineGraph
import pandas as pd
import json
import os


def get_values(index):
    with open('sample_inputs/line_data.json', 'r') as f:
        line_graph = json.loads(f.read())

    dt = pd.DataFrame(line_graph[index]['data'])
    input_data = {'title': 'Monday', 'xLabel': 'Time', 'yLabel': 'Blood Pressure', 'data': {}}
    input_data['data']['time'] = dt.value_x_axis.values - 18000
    input_data['data']['value'] = dt.value_y_axis.values

    return input_data


path = './ignore'
os.makedirs(path, exist_ok=True)
doc = SimpleDocTemplate(f"{path}/custom_graph.pdf", pagesize=letter)
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
