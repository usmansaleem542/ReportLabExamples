
import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
def get_Point2Pixel(x1, x2, y1, y2, point):
    slope = (y2 - y1) / (x2 - x1)
    pixVal = y1 + slope * (point - x1)
    return pixVal

with open('sample_data.json', 'r') as f:
    sampleData = json.load(f)

from datetime import datetime
dt = datetime.now()
start = datetime(year=2000, month= 1, day= 1, hour=0, minute=0, second=0, microsecond=0).timestamp()
end = datetime(year=2000, month= 1, day= 1, hour=23, minute=59, second=59, microsecond=999999).timestamp()
x = []
y = []
mmRange = {}

data = {"time": [], "value": [], "Q1": []}

for i in range(10):
    t = np.random.randint(start, end)
    val = np.random.randint(47, 279)
    data["time"].append(t)
    data["value"].append(val)
    data["Q1"].append([np.random.randint(val-50, val), np.random.randint(val, val+50)])
# now = datetime(year=2000, month= 1, day= 1, hour=dt.hour, minute=dt.minute, second=dt.second, microsecond=dt.microsecond).timestamp()
data = pd.DataFrame(data).sort_values(by='time')

sampleData['time'] = list(data.time)
sampleData["value"]= list(data.value)
sampleData["Q1"] = list(data.Q1)

print(sampleData['time'])
print(sampleData["value"])
print(sampleData["Q1"])

with open('sample_data2.json', 'w') as f:
    f.write(json.dumps(sampleData, indent=4))
    f.close()
plt.plot(data['time'], data['value'])
plt.show()
# val = get_Point2Pixel(start, end, 0, 1, end)


exit()
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
c = canvas.Canvas("rotate.pdf")

c.line( 2*cm, 21*cm, 2*cm, 16*cm)
c.line( 2*cm, 16*cm, 11*cm, 16*cm )

c.setFillColorRGB( 0, 0, 1 )
c.rect( 2.5*cm, 16*cm, 1.5*cm, 3*cm, fill = 1 )
c.setFillColorRGB( 0, 1, 0 )
c.rect( 4.5*cm, 16*cm, 1.5*cm, 4*cm, fill = 1 )
c.setFillColorRGB( 1, 0, 0 )
c.rect( 6.5*cm, 16*cm, 1.5*cm, 2*cm, fill = 1 )

c.setFillColorRGB( 0, 0, 0 )

i=0
for str in ["blue", "green", "red"]:
    c.saveState()
    c.translate( (i + 3.5) * cm, 15.5 * cm )
    c.rotate( 45 )
    c.drawRightString( 0, 0, str )
    c.restoreState()
    i += 2

c.showPage()
c.save()

exit()

from reportlab.pdfgen import canvas
from reportlab.lib.colors import blue, green, white

def welcome(c):
    c.acroForm.checkbox(
        checked=True,
        buttonStyle='check',
        shape='square',
        fillColor=white,
        borderColor=green,
        textColor=blue,
        borderWidth=1,
        borderStyle='solid',
        size=20,
        x=100,
        y=100,
        tooltip="example tooltip",
        name="example_checkbox",
        annotationFlags='print',
        fieldFlags='required',
        forceBorder=True,
        relative=False,
        dashLen=3)


c3 = canvas.Canvas("story.pdf")
welcome(c3)
c3.showPage()
c3.save()