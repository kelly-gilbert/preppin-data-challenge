# Preppin' Data 2021 Week 12

## Python - data prep
<a href="preppin-data-2021-12.py">
<img src="img-python-code-2021-12.png?raw=true" alt="Python code">
</a>

## Alteryx - data prep
<a href="/preppin-data-2021-12.yxmd">
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
The Interactive Chart tool has many useful features like batching (outputing multiple charts, grouped by a field) and transforming (splitting one input stream into multiple series on the chart). However, I've found this tool to be a bit buggy since I upgraded to 2020.3. I intended to batch (create separate charts) by Breakdown and transform (break into series/layers) by year, so I could format the years independently. That should work in theory, but in practice, my changes wouldn't stay when I entered them in the By Type tab (or the Individually tab) of the Layer configuration. 😞

Without the transform option, I could have crosstabbed the years into columns, and then manually added a layer for each year, so I could change the settings individually. In the end, I accomplished what I wanted by manually editing the colors and line widths in the tool XML.

<a href="preppin-data-2021-12.yxmd">
<img src="img-alteryx-chart-2021-12.png?raw=true" alt="Alteryx workflow to generate charts">
</a>

### Alteryx - chart output

I did use an overlay tool to add the legend in the lower right corner, but for some reason it did not render in the png output.

<a href="preppin-data-2021-12.yxmd">
<img src="img-alteryx-chart-output-2021-12.png?raw=true" alt="Chart output from Alteryx">
</a>
