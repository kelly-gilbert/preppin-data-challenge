<h6><a href="..\preppin-data-2021-41\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2021-43\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2021 Week 42

[Challenge description](https://preppindata.blogspot.com/2021/10/2021-week-42-charity-fundraising.html)

What I learned/practiced this week:
* Practiced: generating a range of dates with date_range
* Pracitced: joining (merge)
* Practiced: filling nans with fillna
* Practiced: aggregation (transform)

## Python

The basic code to complete the challenge:
<br>
<br>
<a href="preppin-data-2021-42.py">
<img src="img-basic-code-without-apply-format-2021-42.png?raw=true" alt="Python code (basic, without apply_format function)">
</a>
<br>
<br>
I added a function to match the number formatting in the provided output file. This wasn't really necessary, and doesn't make a practical difference assuming the file would be used for visualization or further quantititative analysis. I did this more for my own practice.
<br>
<br>
The solution file had integers with no decimals and fractions with up to nine decimal places (no trailing zeroes, except one). Adding a float_format parameter to to_csv would have formatted all numbers to nine decimal places (with trailing zeroes).
<br>
<br>
<a href="preppin-data-2021-42.py">
<img src="img-apply-format-2021-42.png?raw=true" alt="Python code (apply_format function)">
</a>
<br>
<br>
There was one odd exception on day 23, where the Value Raised per Day in the provided output was included with the trailing zero (whereas other days, such as day 16, where the value/day was 31.25 did <i>not</i> include the trailing zeroes). My solution outputs this result as 56.52173913, without the trailing zero. I could have added another condition to the apply_format function to pad out the number in this case, but it didn't seem practically useful.
<br>
<br>
<img src="img-day-23-output-2021-42.png?raw=true" alt="Python code (apply_format function)">
<br>
<br>

## Alteryx
<a href="preppin-data-2021-42.yxzp">
<img src="img-alteryx-2021-42.png?raw=true" alt="Alteryx workflow">
</a>