from common import CGFigure

def GetBloodGlucoseGraph(data, size, title="Graph Title", xlabel='Time', ylabel="Blood Sugar", boundary=False):
    ax = CGFigure(size, title=title, xlabel=xlabel, ylabel=ylabel, boundary=boundary)
    ax.fillbetween(data['data']['time'], data['data']['Q1'])
    ax.fillbetween(data['data']['time'], data['data']['Q2'])
    ax.plot(data['data']['time'], data['data']['value'])
    ax.plotrange(data['normal_range'])
    graph = ax.render()
    return graph