import numpy as np
import pandas as pd
import json
import os
from datetime import datetime


# np.random.seed(5)

def get_Point2Pixel(x1, x2, y1, y2, point):
    slope = (y2 - y1) / (x2 - x1)
    pixVal = y1 + slope * (point - x1)
    return pixVal


def gen(x, scale, offset, mult=100):
    dt = np.sin(x) + np.random.normal(scale=scale, size=len(x))
    dt = (dt * mult) + abs(min(dt) * mult)
    return np.round(dt) + offset


def GenerateData(start, end, filename='ignore/sample_data2.json', offset=50, randomN=False):
    # dt = datetime.now()
    dataBP = {"title": "Blood Pressure Graph", "xLabel": "Time", "yLabel": "Blood Pressure",
              "normal_range": [50, 200],
              "data": {"time": [], "value": [], "Q1": [], "Q2": []}}

    data = dataBP['data']
    x = np.linspace(start, end - 3600)
    y = gen(x, 0.05, offset)
    for i in range(len(x)):
        t = x[i]
        val = y[i]

        data["time"].append(t)
        data["value"].append(val)
        if randomN:
            q1 = [np.random.randint(val - offset, val), np.random.randint(val, val + offset)]
        else:
            q1 = [val - offset, val + offset]
        data["Q1"].append(q1)
        if randomN:
            q2 = [np.random.randint(q1[0] - offset, q1[0]), np.random.randint(q1[1], q1[1] + offset)]
        else:
            q2 = [q1[0] - offset, q1[1] + offset]
        data["Q2"].append(q2)
    # now = datetime(year=2000, month= 1, day= 1, hour=dt.hour, minute=dt.minute, second=dt.second, microsecond=dt.microsecond).timestamp()
    df = pd.DataFrame(data).sort_values(by='time')

    data['time'] = list(df.time)
    data["value"] = list(df.value)
    data["Q1"] = list(df.Q1)
    data["Q2"] = list(df.Q2)

    # print(df.head())
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(json.dumps(dataBP, indent=4))
        f.close()
    return dataBP
