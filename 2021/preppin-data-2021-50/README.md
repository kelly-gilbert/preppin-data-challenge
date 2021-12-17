<h6><a href="..\preppin-data-2021-49\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2021-51\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2021 Week 50

[Challenge description](https://preppindata.blogspot.com/2021/12/2021-week-50-departmental-december-sales.html)

What I learned/practiced this week:
* Practiced: reading multiple sheets from an Excel file
* Practiced: aggregation (sum and cumsum)
* Practiced: reshaping (melt)


In this week's challenge, we had to parse out the YTD total from the first month, and then use it to calculate the running YTD total for the next month. I tried to make my solution as dynamic as possible, so it could handle any future months that were added (and re-start the YTD calculation for future years).


## Python
<a href="preppin-data-2021-50.py">
<img src="img-python-code-2021-50.png?raw=true" alt="Python code">
</a>

## Alteryx

This week's Alteryx solution required a batch macro to import the sheets (Dynamic Input couldn't be used because the sheets have different columns).

<a href="preppin-data-2021-50.yxzp">
<img src="img-alteryx-2021-50.png?raw=true" alt="Alteryx workflow">
</a>

#### Batch macro:
<br>
<a href="preppin-data-2021-50.yxzp">
<img src="img-alteryx-2021-50-batch-macro.png?raw=true" alt="Alteryx batch macro">
</a>
