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

The first method that came to mind was grouping by unique values, then assigning the IDs to that smaller dataframe, then joining (merging) back to the fact table to add the IDs. However, I wondered if this would be an opportunity to use the factorize method (which converts strings to factors). The drawback to factorize, though, is that the entire dataframe has to be sorted first. Using factorize made for tidier code, but sorting and re-sorting the entire dataframe had to be pretty expensive. I did a little profiling to see which method was more efficient (in terms of run time). 

#### Using timeit on the original exercise
I wrote the solution both ways (method #1 = sort + factorize, method #2 = group + merge) and ran timeit to compare them. I was surprised to see that both methods were pretty similar. However, the challenge dataset was pretty small (< 3000 records), and there are some additional processes (such as reading in the file, splitting strings, calculating sales, etc.) taking up some of the time.

<img src="./profiling/img-profiling-01-timeit.png?raw=true" alt="Python timeit results showing that factorize completed in 31.2 ms +/- 2.22 ms, and group+merge completed in 32.5 ms +/- 1.15 ms">

#### Setting up a simple example:
To investigate further, I set up the example below to generate some sample Customer strings and Order Dates, then I ran both functions with datasets of varying size and cardinality.

<a href="./profiling/preppin-data-2021-51-profiling-example.py">
<img src="./profiling/img-profiling-02-test-code.png?raw=true" alt="Screen shot of Python code with functions for profiling">
</a>

#### Line profiling for a small example
First, I used the sample code to profile a small dataset similar to the exercise (3000 records, 380 unique customer IDs). Run time was similar, and, at this size, the time it takes to perform the sort+factorize is pretty similar to the time it takes to do the merge (join).

<img src="./profiling/img-profiling-03-small-example.png?raw=true" alt="Screen shot of Python code with functions for profiling">

#### Line profiling for a large example, low cardinality:
Next, I tried making the dataset larger (1M records), and I kept the cardinality low (52 possible customer names). At this size, the factorize method took a good bit longer (0.74 s vs. 0.29 s), and we can see that the sort+factorize time is much higher than the merge time.

<img src="./profiling/img-profiling-04-low-cardinality.png?raw=true" alt="Screen shot of Python code with line profiling results">

#### Line profiling for a large example, high cardinality:
Next, I kept the dataset size the same (1M records), but changed the cardinality of the customer name. Instead of 52 possible choices, now the customer IDs are basically unique, which should make the merge more expensive. However, it also made the sort much more expensive. While the join (merge) did get more expensive, the sort blew up 20x!

<img src="./profiling/img-profiling-05-high-cardinality.png?raw=true" alt="Screen shot of Python code with line profiling results">

#### Conclusion

For a small dataset with low cardinality, either method works, but for a larger dataset, the group-first-then-merge method is more efficient (in time).
