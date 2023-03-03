<h6><a href="..\preppin-data-2022-47\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2022-49\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2022 Week 48 - Tiddlywinks Tidy

[Challenge description](https://preppindata.blogspot.com/2022/11/2022-week-48-tiddlywinks-tidy.html)

What I learned/practiced this week:
* Practiced: replacing partial strings with regex
* Practiced: reshaping (melt)
* Practiced: writing multiple sheets to an Excel file

## Python
<i>click the image to view the code</i><br>
<br>
<a href="preppin-data-2022-48.py">
<img src="img-python-code-2022-48.png?raw=true" alt="Python code">
</a>

## Alteryx
<i>click the image to download the workflow</i><br>
<br>
In the screen shot below, I used a Block Until Done tool to write the separate sheets to Excel. An alternative method (also included in the workflow linked below) is using Alteryx reporting tools + rendering to Excel.<br>
<br>
The drawback of the Block Until Done tool is that it will force the two branches to run in series (rather than parallel), which may take longer. On the other hand, using reporting tools adds unnecessary formatting, and can be difficult/impossible to pass through special characters (such as the line breaks in one of the event descriptions).<br>
<br>
This dataset is very small/runs quickly, so I chose Block Until Done for simplicity.<br>
<br>
<a href="preppin-data-2022-48.yxzp">
<img src="img-alteryx-2022-48.png?raw=true" alt="Alteryx workflow">
</a>