<h6><a href="..\preppin-data-2022-22\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2022-24\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2022 Week 23 - PD x WOW Salesforce Opportunities

[Challenge description](https://preppindata.blogspot.com/2022/06/2022-week-23-pd-x-wow-salesforce.html)

What I learned/practiced this week:
* Practiced: Unioning (concat)
* Practiced: Performance comparison

## Python
<i>click the image to view the code</i><br>
<br>
<a href="preppin-data-2022-23.py">
<img src="img-python-code-2022-23.png?raw=true" alt="Python code">
</a>

## Alteryx
<i>click the image to download the workflow</i><br>
<br>
<a href="preppin-data-2022-23.yxzp">
<img src="img-alteryx-2022-23.png?raw=true" alt="Alteryx workflow">
</a>

## Performance analysis

For performance analysis, I made the opportunity dataset larger by appending the dataset to itself 5000 times (a dataframe of 1.1M rows).

This exercise is purely for my own exploration/curiosity. For a one-time analytics exercise like this, performance within a few seconds is certainly acceptable and doesn't require additional optimization. Even if this was part of a recurring data pipeline, it is likely that < 5 second performance on 1M records would be acceptable, too. If the dataset was very large, then I'd likely use a different solution vs. performing this in-memory with pandas. 

#### Creating the Opened and ExpectedCloseDate records

My first idea was to melt the CreatedDate and CloseDate into separate rows, then filter out the IDs that were already closed. However, I wondered if it would be faster to slice out just the records that were NOT closed (rather than return them and filter them out).

Using timeit, slicing out the NOT closed records was more than 5 times faster! The drawback is that the code is less readable/tidy, and for this exercise, <5 seconds is certainly acceptable.

<a href="preppin-data-2022-23.py">
<img src="img-performance-testing-2022-23-appending.png?raw=true" alt="timeit results for different options for appending the data">
</a><br>
<br>

The more I thought about it, though, the more I liked the way that option 2 keeps the renames/assignments together with each dataframe (I can see all of the transformations needed to get the source data ready for concatenation).<br>
<br>

#### Handling renames and calculations

Next, I looked at some options for handling the renames across dataframes + the assignments (such as the SortOrder).

For the first option, I performed all of the renames/assignments with method chaining. It's efficient, but looks ugly and is somewhat difficult to read.

For the second option, I concatenated the three parts first (leaving the original column names), then combined the columns and updated the Stage and SortOrder in series. This took about twice as long (and there would be some memory implications due to the additional fields). This option was much tidier/easier to read, in my opinion, though, and even though option 2 is slower, it's still an acceptable amount of time for this particular use case.

<a href="preppin-data-2022-23.py">
<img src="img-performance-testing-2022-23-renames-and-calcs.png?raw=true" alt="timeit results for different options for appending the data">
</a><br>
<br>

Finally, I chose a slightly modified version of option 1. I fixed some inconsistent line breaks and used a common dictionary to tidy up the renames. 

<a href="preppin-data-2022-23.py">
<img src="img-performance-testing-2022-23-renames-and-calcs-opt3.png?raw=true" alt="timeit results for different options for appending the data">
</a>
