# events_visualizer

This application displays a graph for network link event data that occur in a specific timeframe.

It requires two files to run - the first file being a data.csv file that is used for device event data. 
Each line in this file should have data consisting of the format:
'[Device],[Port],[YYYY/MM/DD],[hh:mm:ss],[Value of Event (shown as 0 or 1)]'

The second set of data is a dictionary.txt file that consists of: 
[Device],[port],[Name of Link]

It is used to relabel links on the plot when the application runs.

## Getting Started:

This application runs as a Bokeh server using its library in python which can be installed using **pip install bokeh**. 
You can use the command **bokeh info** to verify that it was installed and check the version information as well.

For any issues that may come up during installation refer to
https://docs.bokeh.org/en/latest/docs/first_steps/installation.html#installation

To run this application, navigate to the directory that contains the visualizer.py file and run the command: 
**bokeh serve --show visualizer.py**


### Additional Comments

This application can be extended in the future to show the outage times (in seconds) for each link and be able to identify 
when multiple outages happen (correlating two or more outages in parallel). 
Bokeh has the capability to display multiple plots and change the axis values depending on which information the user 
would like to view.

To find support or discussions related potential issues/information for the Bokeh library, visit https://discourse.bokeh.org/
For more information about this project and explanations behind its code, refer to the docs folder.






