from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import HoverTool, ColumnDataSource, Select,TextInput,Slider
from bokeh.plotting import figure
import pandas as pd
from functools import partial 
import numpy as np
#import datashader as ds
#import datashader.transfer_functions as tf
#from datashader.bokeh_ext import InteractiveImage
#from datashader.utils import export_image
#from datashader.colors import colormap_select, Hot,virdis,inferno,Greys9
import holoviews as hv
hv.extension('bokeh')

'''
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
ds = hv.Dataset(Combined)
ds.to(hv.Curve,'Date','Price')
'''
df = pd.DataFrame({'dt': range(10), 'col1': np.random.rand(10),
                   'col2': np.random.rand(10), 'col3': np.random.rand(10)})
tidy_df = pd.melt(df, id_vars='dt', var_name='column', value_name='value')
ds = hv.Dataset(tidy_df)
output_file("interactive_legend.html", title="interactive_legend.py example")
ds.to(hv.Curve, 'dt', 'value', 'column')

