import numpy as np
import matplotlib.pyplot as plt
np.random.seed(22)
def get_Point2Pixel(x1, x2, y1, y2, point):
    slope = (y2 - y1) / (x2 - x1)
    pixVal = y1 + slope * (point - x1)
    return pixVal


from datetime import datetime
dt = datetime.now()
start = datetime(year=2000, month= 1, day= 1, hour=0, minute=0, second=0, microsecond=0).timestamp()
end = datetime(year=2000, month= 1, day= 1, hour=23, minute=59, second=59, microsecond=999999).timestamp()
x = []
y = []
mmRange = {}

data = {}

for i in range(10):
    t = np.random.randint(start, end)
    val = np.random.randint(10, 350)
    data[t] = [[val]]
    data[t].append([np.random.randint(val-10, val), np.random.randint(val, val+10)])
    print(data[t])

x = list(np.sort(x))

now = datetime(year=2000, month= 1, day= 1, hour=dt.hour, minute=dt.minute, second=dt.second, microsecond=dt.microsecond).timestamp()
plt.plot(x, y)
plt.show()
print(x)
print(y)
print(mmRange)

val = get_Point2Pixel(start, end, 0, 1, end)


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