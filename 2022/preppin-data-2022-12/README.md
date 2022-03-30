<h6><a href="..\preppin-data-2022-11\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2022-13\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2022 Week 12 - Gender Pay Gap

[Challenge description](https://preppindata.blogspot.com/2022/03/2022-week-12-gender-pay-gap.html)

What I learned/practiced this week:
* Practiced: importing multiple csv files
* Practiced: finding a value based on highest value in another column
* Practiced: string concatenation and formatting
* Practiced: performance profiling

## Python
<a href="preppin-data-2022-12.py">
<img src="img-python-code-2022-12.png?raw=true" alt="Python code">
</a>

## Alteryx
<a href="preppin-data-2022-12.yxzp">
<img src="img-alteryx-2022-12.png?raw=true" alt="Alteryx workflow">
</a>

## Performance profiling

I tried several methods for identifying the most recent EmployerName for each EmployerID:
<br>
<img src="img-performance-profiling.png?raw=true" alt="Python code for performance profiling">
<br>
<br>
#### Results:
<img src="img-runtime-1.png?raw=true" alt="Chart of run times for all methods">
<br>
<br>
Removing method 2, which is clearly the slowest option:<br>
<br>
<img src="img-runtime-1.png?raw=true" alt="Chart of run times without method 2">