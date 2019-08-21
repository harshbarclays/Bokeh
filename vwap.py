from bokeh.io import vform
from bokeh.models import CustomJS, ColumnDataSource, MultiSelect
from bokeh.plotting import figure, output_file, show
import pandas as pd

IBM = pd.read_csv(
        "http://ichart.yahoo.com/table.csv?s=IBM&a=0&b=1&c=2011&d=0&e=1&f=2016",
        parse_dates=['Date'])

output_file("datetime.html")
source = ColumnDataSource({'x': IBM['Date'], 'y1': IBM['Close'], \
'y2': IBM['Adj Close'], 'y1p': IBM['Close'], 'y2p': IBM['Adj Close']})

p = figure(width=500, height=250, x_axis_type="datetime")

p.line('x', 'y1', source=source, color='navy', alpha=0.5)
p.line('x', 'y2', source=source, color='red', alpha=0.5)

callback = CustomJS(args=dict(source=source), code="""
        var data = source.get('data');
        var f = cb_obj.get('value')
        y1 = data['y1']
        y2 = data['y2']
        y1p = data['y1p']
        y2p = data['y2p']
        if (f == "line2") {
            for (i = 0; i < y1.length; i++) {
              y1[i] = 'nan'
                y2[i] = y2p[i]
            }
        } else if (f == "line1") {
            for (i = 0; i < y2.length; i++) {
                y1[i] = y1p[i]
                y2[i] = 'nan'
            }
        } else if (f == "none") {
            for (i = 0; i < y2.length; i++) {
                y1[i] = 'nan'
                y2[i] = 'nan'
            }
        } else {
            for (i = 0; i < y2.length; i++) {
                y1[i] = y1p[i]
                y2[i] = y2p[i]
            }
        }
        source.trigger('change');
    """)

multi_select = MultiSelect(title="Lines to plot:", \
value=["line1", "line2", "none"], \
options=["line1", "line2", "none"], callback=callback)
layout = vform(multi_select, p)
show(layout)