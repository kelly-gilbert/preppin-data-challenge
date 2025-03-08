<h6><a href="..\preppin-data-2024-50\README.md">◀️  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2024-52\README.md">Next Week  ▶️</a></h6>

# Preppin' Data 2024 Week 51 - Strictly Positive Improvements?

[Challenge description](https://preppindata.blogspot.com/2024/12/2024-week-51-strictly-positive.html)

What I learned/practiced this week:
* [Practiced] String parsing
* [Practiced] Grouping and aggregation
* [Learned] differences in handling nulls and NaNs in polars vs. pandas

```pandas df[df['Result'] != 'Eliminated']``` will keep rows where Result is NaN 
```polars df.filter(pl.col('Result') != 'Eliminated')``` will exclude rows where Result is null


## Python (pandas)
<i>click the image to view the code</i><br>
<br>
<a href="preppin-data-2024-51.py">
<img src="img-python-code-2024-51.png?raw=true" alt="Python code (pandas)">
</a>

## Python (polars)
<i>click the image to view the code</i><br>
<br>
<a href="preppin-data-2024-51-polars.py">
<img src="img-python-code-2024-51-polars.png?raw=true" alt="Python code (polars)">
</a>

## Alteryx
<i>click the image to download the workflow</i><br>
<br>
<a href="preppin-data-2024-51.yxzp">
<img src="img-alteryx-2024-51.png?raw=true" alt="Alteryx workflow">
</a>