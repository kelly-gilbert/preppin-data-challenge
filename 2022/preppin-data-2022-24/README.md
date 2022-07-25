<h6><a href="..\preppin-data-2022-23\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2022-25\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2022 Week 24 - Longest Flights

[Challenge description](https://preppindata.blogspot.com/2022/06/2022-week-24-longest-flights.html
)

What I learned/practiced this week:
* Practiced: string methods (replace, extract, concatenating columns)
* Practiced: ranking
* Practiced: joining (merge)

## Python
<i>click the image to view the code</i><br>
<br>
<a href="preppin-data-2022-24.py">
<img src="img-python-code-2022-24.png?raw=true" alt="Python code">
</a>

## Alteryx
<i>click the image to download the workflow</i><br>
<br>
<a href="preppin-data-2022-24.yxzp">
<img src="img-alteryx-2022-24.png?raw=true" alt="Alteryx workflow">
</a><br>
<br>
#### Performance comparison
Knowing that regex functions can be slower than regular string functions, I tried replacing the Regex Parse + Multi-Field tools (to parse the distances and convert to numeric) with string formulas + ToNumber in the existing Formula tool. I duplicated the dataset 35,000 times for a test dataset of ~1.1M records.<br>
<br>
At 1.1M records, the non-regex alternative was a bit faster (~20% or 2.5 seconds). For this specific use case, I would favor the regex solution, because a few seconds is not likely to make a material difference, and (in my opinion) the regex version would be easier to maintain if the pattern changed in the future. However, with a very large dataset, it might make more sense to consider the non-regex solution.<br>
<br>
<img src="img-alteryx-2022-24-performance-compare.png?raw=true" alt="Alteryx workflow">
