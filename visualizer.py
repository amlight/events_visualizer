from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, CheckboxGroup, Button, DatePicker, HoverTool
from bokeh.plotting import figure, curdoc
from bokeh.palettes import d3
from datetime import datetime
from parse_data import process_data

data = process_data()
nodes = list(data.columns.values)
current_day = datetime.now().date()

# this is so the checkboxgroup has all boxes active by default when the application starts running
active_boxes = []
for i in range(len(nodes)):
    active_boxes.append(i)

# widgets for input controls
node_checkbox = CheckboxGroup(labels=nodes, active=active_boxes)
reset_button = Button(label="Select All", width=50)
daterange_start = DatePicker(title='Select start date', value="2020-10-15", min_date="2020-10-15", max_date=current_day)
daterange_end = DatePicker(title='Select end date', value=current_day, min_date="2020-10-15", max_date=current_day)

# creating column data source (CDS) to be used by the plot
source = ColumnDataSource(data=data)
source.add(data.index, 'index')

# creating figure
p = figure(plot_height=650, title="AmLight Link Flap Events", sizing_mode="stretch_both",
           x_axis_type='datetime', toolbar_location='above')

# creating renderers for each stacker on the plot - necessary to assign HoverTools
renderers = p.vbar_stack(nodes, x='index', width=1e7, source=source, legend_label=nodes,
                         color=d3['Category20'][len(nodes)], line_color="black", name=nodes)

for r in renderers:
    node = r.name
    hover = HoverTool(tooltips=[
        ("%s events" % node, "@$name"),
        ("date", "@index{%F}")
    ], formatters={
        '@index': 'datetime',
    }, renderers=[r], toggleable=False)
    p.add_tools(hover)

p.y_range.start = 0
p.y_range.end = data.max().max() + 15


# updates data with filtering from widgets
def update():
    start = daterange_start.value
    end = daterange_end.value
    active_labels = [node_checkbox.labels[i] for i in node_checkbox.active]

    # make a copy of the parsed dataframe from list of active nodes (selected by checkbox)
    temp_df = data[active_labels]

    if start == end:
        selected = temp_df.loc[start]
    else:
        selected = temp_df.loc[start:end]

    # "refreshes" the CDS so it can be given a different set of columns
    source.data = {name: [] for name in active_labels}

    # update CDS that's currently in use by the plot
    new_source = ColumnDataSource(selected)
    source.data.update(new_source.data)


# function for reset button
def select_all():
    node_checkbox.active = list(range(len(nodes)))


# groups all widgets together and calls update function if any are interacted with
controls = [daterange_start, daterange_end, node_checkbox, reset_button]
for control in controls:
    if control == node_checkbox:
        control.on_change('active', lambda attr, old, new: update())
    elif control == reset_button:
        control.on_click(select_all)
    else:
        control.on_change('value', lambda attr, old, new: update())

widgets = column(*controls, width=250, height=1000)
widgets.sizing_mode = "stretch_height"

curdoc().add_root(row(widgets, p))
curdoc().title = "AmLight Event Report"
