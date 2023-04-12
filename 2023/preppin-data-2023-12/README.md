<h6><a href="..\preppin-data-2023-11\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2023-13\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2023 Week 12 - Regulatory Reporting Alignment

[Challenge description](https://preppindata.blogspot.com/2023/03/2023-week-12-regulatory-reporting.html)

What I learned/practiced this week:
* Learned: numpy busday functions (busday_offset and busday_count)
* Practiced: grouping and aggregation
* Practiced: date formatting

## Python
<i>click the image to view the code</i><br>
<br>
<a href="preppin-data-2023-12.py">
<img src="img-python-code-2023-12.png?raw=true" alt="Python code">
</a>

## Alteryx
<i>click the image to download the workflow</i><br>
<br>
In practice, we'd normally have a database dimension table that had the holiday flags and reporting dates pre-calculated. To imitate that here, I created a macro to generate the reporting calendar. In reality, that would be an Input tool that brought in the date dimension table.
<br>
<br>
<a href="preppin-data-2023-12.yxzp">
<img src="img-alteryx-2023-12.png?raw=true" alt="Alteryx workflow">
</a>
<br>
<br>
<a href="preppin-data-2023-12.yxzp">
<img src="img-alteryx-2023-12-macro.png?raw=true" alt="Alteryx workflow">
</a>