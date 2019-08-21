from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import HoverTool, ColumnDataSource, Select,TextInput,Slider
from bokeh.plotting import figure
import pandas as pd
from functools import partial 
import datashader as ds
import datashader.transfer_functions as tf
from datashader.bokeh_ext import InteractiveImage
from datashader.utils import export_image
from datashader.colors import colormap_select, Hot,virdis,inferno,Greys9
background = "white"
export = partial(export_image, background = background, export_path="export")




TOOLS='pan,wheel_zoom,box_zoom,reset,tap,save,box_select,lasso_select'

# Select widget
ccy_options = ['AUDUSD', 'USDJPY']
menu = Select(options=['AUDUSD','USDJPY'], value='USDJPY')
slider = Slider(start=0, end=300, step=100, value=100, title='Volume Cutoff')

# Function to get Order/Trade/Price Datasets
def get_order_dataset(src,name,value):
    df = src[(src.CCY == name) & (src.Type == 'Order') & (src.Volume > value) & (src.Side == 'Buy')].copy()
    return ColumnDataSource(data=df)

def get_trade_dataset(src,name,value):
    df = src[(src.CCY == name) & (src.Type == 'Trade') & (src.Volume > value) & (src.Side == 'Buy')].copy()
    return ColumnDataSource(data=df)

def get_price_dataset(src,name):
    df = src[(src.CCY == name) & (src.Type == 'Prices')].copy()
    return ColumnDataSource(data=df)

# Function to Make Plots
def make_plot(source_order,source_trade,source_price):
    x  = 'Date'
    y  = 'Price'
    size = 20
    alpha = 0.5
    hover = HoverTool(
        tooltips = [
            ('OrderId', '@OrderId'),
            ('Volume', '@Volume')
            ]
        )
    plot = figure(plot_width=800, plot_height=450, tools=[hover, TOOLS], 
           title='Order/Execution Snapshot with Price Levels',
           x_axis_label='Date', y_axis_label='Price',x_axis_type="datetime")
    plot.circle(x=x, y=y, size=size, alpha=alpha, color='blue',
    legend='Orders', source=source_order)
    plot.triangle(x=x, y=y, size=size, alpha=alpha, color='red',
    legend='Trades', source=source_trade)
    plot.line(x=x, y=y, color='grey',legend='Price Levels', source=source_price)
    plot.legend.location = 'top_left'
    return plot
# Function to Update Plots
def update_plot(attrname, old, new):
    newccy = menu.value
    newvalue = slider.value
    print(newvalue)
    src_order = get_order_dataset(Combined,newccy,newvalue)
    src_trade = get_trade_dataset(Combined,newccy,newvalue)
    source_order.data.update(src_order.data)
    source_trade.data.update(src_trade.data)
    src_price = get_price_dataset(Combined,newccy)
    source_price.data.update(src_price.data)

# Input Files    
Ops = "C:/Users/Harsh/Documents/Python Scripts/Surveillance/Ops.xlsx"
Price = "C:/Users/Harsh/Documents/Python Scripts/Surveillance/Price.xlsx"
Ops_CCY = pd.read_excel(Ops,parse_dates=['Date'],parse_integer=['Volume'])
Price_CCY = pd.read_excel(Price,parse_dates=['Date'],parse_decimal=['Level'],parse_string=['CCY'])
Ops_CCY_formatted = Ops_CCY[['Date','CCY','Side','Price','Type','Volume','OrderId']]
Price_CCY_formatted = Price_CCY[['Date','CCY','Price']]
Price_CCY_formatted['Type'] = "Prices"
Price_CCY_formatted['Volume'] = 0
Price_CCY_formatted['OrderId'] = 0
Price_CCY_formatted['Side'] = 0
Combined = pd.concat([Ops_CCY_formatted,Price_CCY_formatted])

# Files Sourcing via Get Function
source_order = get_order_dataset(Combined,menu.value,slider.value)
source_trade = get_trade_dataset(Combined,menu.value,slider.value)
source_price = get_price_dataset(Combined,menu.value)
plot = make_plot(source_order,source_trade,source_price)
menu.on_change('value', update_plot)
slider.on_change('value', update_plot)

# Arrange plots and widgets in layouts
layout = layout([menu,slider],
                [plot])
curdoc().add_root(layout)