<h6><a href="..\preppin-data-2021-29\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2021-31\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2021 Week 30

[Challenge description](https://preppindata.blogspot.com/2021/07/2021-week-30-lift-your-spirits.html)

What I learned/practiced this week:
* Practiced: multi-row formula/shift
* Practiced: grouping and aggregation
* Practiced: string to date conversion (date parsing)

## Python
<a href="preppin-data-2021-30.py">
<img src="img-python-code-2021-30.png?raw=true" alt="Python code">
</a>

## Alteryx
<a href="preppin-data-2021-30.yxzp">
<img src="img-alteryx-2021-30.png?raw=true" alt="Alteryx workflow">
</a>

### Note:
My solution did not match the provided solution exactly, I believe due to sort order. We are asked to to sort based on timestamp, but there weren't explicit requirements on how to handle timestamps with multiple trips. Within each timestamp, my solution preserves the original record order. The [solution](https://preppindata.blogspot.com/2021/08/2021-week-30-solution.html) in Tableau Prep shows trips sorted differently within each timestamp.

For example, the trips during 0:04 in the original file were 1-->G, then 10-->11. However, the solution output shows them sorted in the opposite order.

<img src="img-output-comparison-2021-30.png?raw=true" alt="Output comparison">
