<h6><a href="..\preppin-data-2022-26\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2022-28\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2022 Week 27 - C&BSCo Clean and Aggregate

[Challenge description](https://preppindata.blogspot.com/2022/07/2022-week-27-c-clean-and-aggregate.html)

What I learned/practiced this week:
* Practiced: parsing a string into columns with regex (extract)
* Practiced: aggregation (agg)
* Practiced: f strings

## Note:
This week's requirements asked us to split the workflow into two branches (one for liquids and one for bars). However, the only difference was converting the units from L to mL on the liquid branch. In reality, I would probably keep this as a single path (especially in pandas), but, in the spirit of the challenge, I tried it both ways.
<br>
<br>
In Alteryx, splitting the workflow with a Filter tool does slightly improve run time, because the mL to L conversion is only applied to part of the records. However, even after increasing the input dataset to ~1M records, the improvement was only about 0.4 sec (10%).
<br>
<br>
In Python, the single workflow was ~0.6 sec faster (20% improvement) vs. splitting the dataframe on a larger input dataframe of ~1M records. In pandas, applying the mL to L conversion to the entire dataframe is reasonably efficient using numpy where.
<br>
<br>
## Python
<i>click the image to view the code</i><br>
#### No split (how I'd normally accomplish this set of tasks)
<a href="preppin-data-2022-27.py">
<img src="img-python-code-2022-27-nosplit.png?raw=true" alt="Python code">
</a>
<br>
<br>

#### Split on Product Type (as specified in the requirements)
<a href="preppin-data-2022-27.py">
<img src="img-python-code-2022-27-split.png?raw=true" alt="Python code">
</a>

## Alteryx
<i>click the image to download the workflow</i><br>
#### No split
<a href="preppin-data-2022-27.yxzp">
<img src="img-alteryx-2022-27-nosplit.png?raw=true" alt="Alteryx workflow">
</a>
<br>
<br>

#### Split (as specified in the requirements)
<a href="preppin-data-2022-27.yxzp">
<img src="img-alteryx-2022-27-split.png?raw=true" alt="Alteryx workflow">
</a>
