<h6><a href="..\preppin-data-2021-39\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2021-41\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2021 Week 40

[Challenge description](https://preppindata.blogspot.com/2021/10/2021-week-40-animal-adoptions.html)

What I learned/practiced this week:
* Practiced: read_csv with a subset of columns
* Practiced: reshaping and aggregation (crosstab)
* Learned: crosstab normalize parameter

## Python
<a href="preppin-data-2021-40.py">
<img src="img-python-code-2021-40.png?raw=true" alt="Python code">
</a>

## Alteryx
<a href="preppin-data-2021-40.yxzp">
<img src="img-alteryx-2021-40.png?raw=true" alt="Alteryx workflow">
</a>

## Experimenting with column sizes

Because this dataset was a bit larger than we normally use for these challenges, I experimented with different column types for the Outcome Group:
<a href="preppin-data-2021-40.py">
<img src="img-column-size-comparison-code-2021-40.png?raw=true" alt="Python code">
</a>

Using an integer or category type (instead of a string) saves 0.35-0.82 MB, but adds a little complexity in getting the names back into the output. In this particular case, the memory savings isn't material, so I used the string type.

<a href="preppin-data-2021-40.py">
<img src="img-column-size-comparison-2021-40.png?raw=true" alt="Python code">
</a>
