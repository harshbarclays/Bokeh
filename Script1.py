from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import HoverTool, ColumnDataSource, Select, Slider
from bokeh.plotting import figure
import pandas as pd

TOOLS='pan,wheel_zoom,box_zoom,reset,tap,save,box_select,lasso_select'
file_obj = "C:/Users/Harsh/Documents/Python Scripts/county.xlsx"
df = pd.read_excel(file_obj)
source1 = ColumnDataSource(df[df.winner == 'Democratic'])
source2 = ColumnDataSource(df[df.winner == 'Republican'])

hover = HoverTool(
        tooltips = [
            ('County Name', '@county'),
            ('Population', '@population'),
            ('Land Area', '@land_area'),
            ('Pop. Density', '@density'),
            ('Winning Party', '@winner'),
            ('Winning Vote %', '@winning_vote_pct'),
            ]
        )
# Plot
plot = figure(plot_width=800, plot_height=450, tools=[hover, TOOLS], 
           title='2016 US Presidential Vote % vs. Population Density (by County)',
           x_axis_label='Vote %', y_axis_label='Population Density (K / sq. mi.)')

y = 'density'
size = 20
alpha = 0.5

c1 = plot.circle(x='winning_vote_pct', y=y, size=size, alpha=alpha, color='blue',
            legend='Democratic-Won County', source=source1)
c2 = plot.circle(x='winning_vote_pct', y=y, size=size, alpha=alpha, color='red',
            legend='Republican-Won County', source=source2)

plot.legend.location = 'top_left'

# Select widget
party_options = ['Show both parties', 'Democratic-won only', 'Republican-won only']
menu = Select(options=party_options, value='Show both parties')

N = 2000000
slider = Slider(start=0, end=10000000, step=1000000, value=N, title='Population Cutoff')

# Select callback
def select_callback(attr, old, new):
    if menu.value == 'Democratic-won only': c1.visible=True; c2.visible=False
    elif menu.value == 'Republican-won only': c1.visible=False; c2.visible=True
    elif menu.value == 'Show both parties': c1.visible=True; c2.visible=True
menu.on_change('value', select_callback)

# Slider callback
def slider_callback(attr, old, new):
    N = new  # this works also with slider.value but new is more explicit
    new1 = ColumnDataSource(df.loc[(df.winner == 'Democratic') & (df.population >= N)])
    new2 = ColumnDataSource(df.loc[(df.winner == 'Republican') & (df.population >= N)])
    source1.data = new1.data
    source2.data = new2.data
    slider.on_change('value', slider_callback)

# Arrange plots and widgets in layouts
layout = layout([menu, slider],
                [plot])

curdoc().add_root(layout)