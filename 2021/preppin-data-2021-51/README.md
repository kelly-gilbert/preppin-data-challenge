<h6><a href="..\preppin-data-2021-50\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2021-52\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2021 Week 51

[Challenge description](https://preppindata.blogspot.com/2021/12/2021-week-51-departmental-december-it.html)

What I learned/practiced this week:
* Practiced: string parsing
* Practiced: replacing strings with factors (factorize)
* Practiced: aggregation
* Practiced: profiling

## Python
<a href="preppin-data-2021-51.py">
<img src="img-python-code-2021-51.png?raw=true" alt="Python code">
</a>

## Alteryx
<a href="preppin-data-2021-51.yxzp">
<img src="img-alteryx-2021-51.png?raw=true" alt="Alteryx workflow">
</a>

## Profiling

Using factorize to assign the IDs requires sorting the entire dataframe multiple times. I wondered if it might be more efficient to aggregate each dimension table first, then sort the smaller dataframes to assign the IDs (then merge to add the IDs back to the main fact table).

#### Setting up a simple example:
<img src="./profiling/line-profile-example-code.png?raw=true" alt="Python code with a simple example for profiling">

I was surprised to see that the merge was pretty expensive - the merge took around the same time as the sort and factorize combined.

#### Line profile for factorize:
<img src="./profiling/line-profile-factorize.png?raw=true" alt="Line profiling results for the factorize method">

#### Line profile for grouping and merging:
<img src="./profiling/line-profile-groupby-and-merge.png?raw=true" alt="Line profiling results for the group and merge method">
