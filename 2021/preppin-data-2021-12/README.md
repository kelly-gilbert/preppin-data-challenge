<h6><a href="..\preppin-data-2021-11\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2021-13\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2021 Week 12 - Maldives Tourism

[Challenge description](https://preppindata.blogspot.com/2021/03/2021-week-12-maldives-tourism.html)

### Summary: 
This week was fairly straightforward data reshaping, but the charts were an exercise in frustration in both tools - I definitely should have chosen a simpler chart type for this practice exercise.

### What I learned/practiced this week:
* Reshaping data
* Text parsing with regex
* Small multiple charts and looping through the original axes to make adjustments to the charts

## Python - data prep
<a href="preppin-data-2021-12.py">
<img src="img-python-code-2021-12.png?raw=true" alt="Python code">
</a>

## Alteryx - data prep
<a href="preppin-data-2021-12.yxzp">
<img src="img-alteryx-2021-12.png?raw=true" alt="Alteryx workflow">
</a>

## Charts

These chart outputs aren't pixel-perfect, but I wanted to try some new things without spending too much time tweaking them!

### Python - chart code
<a href="preppin-data-2021-12.py">
<img src="img-python-chart-code-2021-12.png?raw=true" alt="Python code to generate charts">
</a>

### Python - chart output
<a href="preppin-data-2021-12.py">
<img src="img-python-chart-output-2021-12.png?raw=true" alt="Chart output from Python">
</a>

### Alteryx - chart workflow
Normally, I find charts in Alteryx to be MUCH easier to configure vs. Python, but this week was the opposite. The Alteryx Interactive Chart tool has many useful features like batching (outputing multiple charts, grouped by a field) and transforming (splitting one input stream into multiple series on the chart). However, I've found this tool to be a bit buggy since I upgraded to 2020.3. I intended to batch (create separate charts) by Breakdown and transform (break into series/layers) by year, so I could format the years independently. That should work in theory, but in practice, my changes wouldn't stay when I entered them in the By Type tab (or the Individually tab) of the Layer configuration. 😞

Without the transform option, I could have crosstabbed the years into columns, and then manually added a layer for each year, so I could change the settings individually. In the end, I accomplished what I wanted by manually editing the colors and line widths in the tool XML.

<a href="preppin-data-2021-12.yxzp">
<img src="img-alteryx-chart-2021-12.png?raw=true" alt="Alteryx workflow to generate charts">
</a>

### Alteryx - chart output

I did use an overlay tool to add the legend in the lower right corner, but for some reason it did not render in the png output.

<a href="preppin-data-2021-12.yxzp">
<img src="img-alteryx-chart-output-2021-12.png?raw=true" alt="Chart output from Alteryx">
</a>
