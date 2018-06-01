import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import row, widgetbox
from bokeh.models import Slider, CustomJS, ColumnDataSource, Select
from bokeh.colors import Color, RGB

import random

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
p.title.text = 'Haiti case study'
p.toolbar.active_drag = None  # Disable dragging
p.toolbar.logo = None
p.toolbar_location = None

# Add the Haiti image background
p.image_url(url=['haiti_hq.png'], x=0, y=10, w=14.1, h=10)

# Add elevation (terrain roughness) overlay
elevation_colors = ['blue', 'red', 'green', 'yellow', 'orange']
x_elevation_cells = 14
y_elevation_cells = 10

for i in range(x_elevation_cells):
    for j in range(y_elevation_cells):
        # We do some math to distribute the patches all along the map
        x_unit = x_scale/x_elevation_cells
        x_start = x_unit*i
        x_end = x_unit*(i+1)
        y_unit = y_scale/y_elevation_cells
        y_start = y_unit*j
        y_end = y_unit*(j+1)

        p.patch([x_start, x_end, x_end, x_start],
                [y_start, y_start, y_end, y_end],
                fill_alpha=0.2,
                line_alpha=0,
                fill_color=random.choice(elevation_colors),
                legend='Terrain Roughness',
                level='overlay')

# Add the shelter withstanding circle markers
p.circle('x',
         'y',
         radius=0.5,
         fill_color='color',
         source=source,
         level='overlay',
         legend='Shelter withstandings',
         alpha=0.7)

color_change = CustomJS(args=dict(source=source), code="""
        var data = source.data;
        var color = data['color'];
        var wind = data['wind'];
        var s = spec.value;
        var h = height.value;

        offset = 0;
        if (h == "Roof level") {
            offset = 5;
        }
        else if (h == "10m") {
            offset = 20;
        }

        var fc = "red"; // Final color
        var diff = 0;

        for (var i = 0; i < color.length; i++) {
            fc = "red";
            diff = wind[i] - s + offset;

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

# Create the dropdown for the elevation
height_select = Select(title="Height of measurements", value="Ground level",
                options = ["Ground level","Roof level", "10m"],
                callback=color_change)
color_change.args["height"] = height_select

# Make legend hide on click
p.legend.click_policy="hide"

# Set up the GUI
layout = row(p,
             widgetbox(spec_slider, height_select))

show(layout)
