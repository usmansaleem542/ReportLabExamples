from custom_graph import generator
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

data = generator.GenerateData()
data['data']['value'][0] = 1950
plt.plot(data['data']['time'], data['data']['value'])
plt.show()
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