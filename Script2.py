from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import HoverTool, ColumnDataSource, Select, Slider
from bokeh.plotting import figure
import pandas as pd

TOOLS='pan,wheel_zoom,box_zoom,reset,tap,save,box_select,lasso_select'
Ops = "C:/Users/Harsh/Documents/Python Scripts/Surveillance/Ops.xlsx"
Ops_CCY = pd.read_excel(Ops,parse_dates=['Date'],parse_integer=['Volume'])


Ops_CCY_AUDUSD = ColumnDataSource(Ops_CCY[Ops_CCY.CCY == 'AUDUSD'])
Ops_CCY_USDJPY = ColumnDataSource(Ops_CCY[Ops_CCY.CCY == 'USDJPY'])

hover = HoverTool(
        tooltips = [
            ('OrderId', '@OrderId'),
            ('Date', '@Date'),
            ('CCY', '@CCY'),
            ('Volume', '@Volume'),
            ('Type', '@Type'),
            ('Price', '@Price'),
            ]
        )
# Plot
plot = figure(plot_width=800, plot_height=450, tools=[hover, TOOLS], 
           title='Order/Execution Snapshot',
           x_axis_label='Date', y_axis_label='Price',x_axis_type="datetime")

y = 'Price'
x = 'Date'
size = 20
alpha = 0.5

c1 = plot.circle(x=x, y=y, size=size, alpha=alpha, color='blue',
            legend='AUDUSD', source=Ops_CCY_AUDUSD)
c2 = plot.circle(x=x, y=y, size=size, alpha=alpha, color='red',
            legend='USDJPY',source=Ops_CCY_USDJPY)

plot.legend.location = 'top_left'

# Select widget
party_options = ['Show All', 'AUDUSD', 'USDJPY']
menu = Select(options=party_options, value='Show All')

N = 100
slider = Slider(start=0, end=1000, step=100, value=N, title='Volume Cutoff')

# Select callback
def select_callback(attr, old, new):
    if menu.value == 'AUDUSD': c1.visible=True; c2.visible=False
    elif menu.value == 'USDJPY': c1.visible=False; c2.visible=True
    elif menu.value == 'Show All': c1.visible=True; c2.visible=True
menu.on_change('value', select_callback)

# Slider callback
def slider_callback(attr, old, new):
    N = slider.value  # this works also with slider.value but new is more explicit
    new1 = ColumnDataSource(Ops_CCY.loc[(Ops_CCY.CCY == 'AUDUSD') & (Ops_CCY.Volume > N)])
    new2 = ColumnDataSource(Ops_CCY.loc[(Ops_CCY.CCY == 'USDJPY') & (Ops_CCY.Volume > N)])
    Ops_CCY_AUDUSD.data = new1.data
    Ops_CCY_USDJPY.data = new2.data
    Slider.on_change('value', slider_callback)

# Arrange plots and widgets in layouts
layout = layout([menu],
                [plot])

curdoc().add_root(layout)