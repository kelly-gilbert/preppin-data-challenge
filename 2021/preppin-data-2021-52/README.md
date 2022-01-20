<h6><a href="..\preppin-data-2021-51\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\..\2022\preppin-data-2022-01\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2021 Week 52

[Challenge description](https://preppindata.blogspot.com/2021/12/2021-week-52-departmental-december.html)

What I learned/practiced this week:
* Practiced: grouping and aggregation
* Practiced: string methods (changing case, strip, findall, join)
* Practiced: replacing a column with assign

## Python
<a href="preppin-data-2021-52.py">
<img src="img-python-code-2021-52.png?raw=true" alt="Python code">
</a>

## Alteryx

This week, I tried a few different methods in Alteryx to see how they performed. For performance testing, I created a larger complaint dataset (~1M records), but I did not adjust the number of keywords.

Also, I don't have access to the Alteryx Intelligence Suite, which has more advanced tools for text analytics. I'm using only the standard Alteryx tool set here.

### Method 1: using regex parse to split keywords into rows (~25 s for 1M records)
In this method, the keywords are concatenated into a pipe-delimited list, and a Regex Parse tool (inside the macro) extracts the keywords into rows using the Tokenize method. The macro is only necessary so we can feed a dynamic list of keywords to the Regex Parse tool. This method is especially efficient, because it returns null records for complaints that did not match any keywords.

<a href="preppin-data-2021-52.yxzp">
<img src="img-alteryx-2021-52-method-1.png?raw=true" alt="Alteryx workflow">
</a>

#### Batch macro:
<a href="preppin-data-2021-52.yxzp">
<img src="img-alteryx-2021-52-method-1-macro.png?raw=true" alt="Alteryx workflow">
</a>

#### Method 1 performance profile:
<img src="img-alteryx-2021-52-method-1-performance-profile.PNG?raw=true" alt="Alteryx performance profile results for method 1">

### Method 2: cross join all complaints with all keywords (~35 s for 1M records)
In this method, all complaints were cross joined with all keywords, and then only the matching records were filtered out. With the example set of keywords, this method performed similarly to method 1, but method 2's performance would degrade with a larger number of keywords.

<a href="preppin-data-2021-52-method-2.yxzp">
<img src="img-alteryx-2021-52-method-2.png?raw=true" alt="Alteryx workflow (method 2)">
</a>

#### Method 2 performance profile:
<img src="img-alteryx-2021-52-method-2-performance-profile.PNG?raw=true" alt="Alteryx performance profile results for method 2">

### Method 3: parse complaints into words (~60 s for 1M records)
This method doesn't meet the requirements, because it can't handle multi-word keywords. I wanted to try it just to see the run time. This method uses the Regex Parse tool to split the complaints into individual words, then joins the word list to the keywords.

<a href="preppin-data-2021-52-method-3.yxzp">
<img src="img-alteryx-2021-52-method-3.png?raw=true" alt="Alteryx workflow (method 3)">
</a>

#### Method 3 performance profile:
<img src="img-alteryx-2021-52-method-3-performance-profile.PNG?raw=true" alt="Alteryx performance profile results for method 3">
