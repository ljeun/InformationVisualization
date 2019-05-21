import pandas
from bokeh.models import ColumnDataSource, LabelSet, HoverTool, CustomJS, Select
from bokeh.plotting import curdoc, figure, show, output_file
from bokeh.sampledata.iris import flowers
from bokeh.transform import jitter
from bokeh.sampledata.sprint import sprint
from bokeh.layouts import row, column

from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider


df = pandas.read_csv('flower_data.csv')
source = ColumnDataSource(df)

TITLE = "Growing Height and Scent of Flowers"
TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save"
label = ['Not Scented', 'Deliciously Scented']

TOOLTIPS = """
    <div>
        <div>
            <span style="font-size: 15px; font-weight: bold;">@CommonName</span><br/>
            
        </div>
       
    </div>
     <p>
        <span style="font-size: 12px;">Botanical Name: <span style="color: #696;"><b>@BotanicalName</b></span><br/>
        <span style="font-size: 12px; ">Growing Height: <span style="color: #696;"><b>@GrowingHeightFrom cm</b></span><br/>
        <span style="font-size: 12px; ">Scent: <span style="color: #696;"><b>@ScentName</b></span><br/>
    </p>
"""


colormap = {'Blue': 'blue', 'White': 'white', 'Grey': 'grey',
            'Red': 'red', 'Pink': 'pink', 'Orange': 'orange', 'Yellow': 'yellow', 'Purple': 'purple', 'Green': 'green'}
colors = [colormap[x] for x in df.Color]

i=0
x = ["ScentNum", "Sun"]
x_title = ["ScentName", "Sun"]

p = figure(tools=TOOLS, toolbar_location=None,
           plot_width=400, title=TITLE, x_range=label, tooltips=TOOLTIPS)
#p.background_fill_color = "#dddddd"
p.xaxis.axis_label = 'Scented'
p.yaxis.axis_label = 'Growing Height'
p.grid.grid_line_color = "white"


cr = p.circle(x=jitter('ScentNum', 0.4), y="GrowingHeightFrom", size=20, source=source,
             color="Color", line_color=None, fill_alpha=0.6)

labels = LabelSet(x="ScentName", y="GrowingHeightFrom", text="CommonName", y_offset=8, source=source,
                    text_font_size="8pt", text_color="#555555", text_align='center')

output_file("output.html", title="flower properties")


month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


p2 = figure(y_range=df.CommonName, x_range=month, plot_width=400, plot_height=600, toolbar_location=None,
            title="Flower Blooming Period", tools=TOOLS)


renders = p2.hbar(hover_color="Color", y="CommonName", left='FlowerStartMonth',
                  right='FlowerEndMonth', height=0.4, source=source, color="#dcdcdc")


hover = HoverTool(tooltips=[
    ("Common Name:", "@CommonName"),
    ("Period:", "@FlowerStartMonth")], mode="mouse")
p2.add_tools(hover)


p2.ygrid.grid_line_color = None
p2.xaxis.axis_label = "Month"
p2.outline_line_color = None

# Style
p.title.text_font_size = '18px'
p2.title.text_font_size = '18px'




layout = row(
    p,
    p2
)


show(layout)