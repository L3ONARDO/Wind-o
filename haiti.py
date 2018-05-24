import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row, widgetbox
from bokeh.models import Slider, CustomJS, ColumnDataSource
from bokeh.colors import Color, RGB

output_file('haiti_analysis.html')


x_scale = 14.1
y_scale = 10

# Suppose we have the points distributed in a square grid of size 'x', so
# there are 'x*x' elements in total
x = []
y = []
color = []

side = 7
for i in range(side**2):
    x.append((i//side) + 4)
    y.append((i%side) + 2)
    color.append(RGB(0,0,0))

# Create some random wind data for the points
wind = np.random.rand(side**2)*100

source = ColumnDataSource(data=dict(x=x, y=y, color=color, wind=wind))

# To keep the image centered with its aspect ratio
y_offset = (x_scale - y_scale)/2


# Create the figure
p = figure(x_range=(0, x_scale), y_range=(0 - y_offset, y_scale + y_offset))

p.circle('x', 'y', radius=0.5, fill_color='color', source=source, level='overlay', alpha=0.7)

color_change = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var color = data['color'];
        var wind = data['wind'];
        var s = spec.value;

        var fc = "red"; // Final color
        var diff = 0;

        for (var i = 0; i < color.length; i++) {
            fc = "red";
            diff = wind[i] - s;

            if (diff < -20) {
                fc = "green";
            }
            else if (diff < 0) {
                fc = "yellow";
            }
            else if (diff < 10) {
                fc = "salmon";
            }
            else if (diff < 20) {
                fc = "indianred";
            }
            color[i] = fc;

        }

        source.change.emit();
        // console.log(s);
        """)

# Create a slider
spec_slider = Slider(start=20, end=200, value=50, step=1,
        title="Shelter max. withstand (km/h)", callback=color_change)
color_change.args["spec"] = spec_slider

# Add the Haiti image background
p.image_url(url=['haiti_hq.png'], x=0, y=10, w=14.1, h=10)

# Set up the GUI
layout = row(p, spec_slider)

show(layout)
