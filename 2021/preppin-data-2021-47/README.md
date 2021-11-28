<h6><a href="..\preppin-data-2021-46\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-2021-48\README.md">Next Week  ▶</a></h6>

# Preppin' Data 2021 Week 47

[Challenge description](https://preppindata.blogspot.com/2021/11/2021-week-47-games-night-viz-collab.html)

What I learned/practiced this week:
* Practiced: named aggregation
* Practiced: date calculation
* Practiced: reshaping (melt)
* Practiced: [bonus section] small multiple charts (matpotlib)

This week's challenge was a collaboration with #GamesNightViz, a data visualization challenge around the topic of games. Learn more [here](https://github.com/wjsutton/games_night_viz/blob/main/1_player_select.md).

My solution did not match the provided solution for the percent_won metric, because I show that Lika Gerasimova had one win (on Aug 18, 2012), while the solution has null win percentage for Lika (and ranked her last).

## Data prep: Python
<a href="preppin-data-2021-47.py">
<img src="img-python-code-prep-2021-47.png?raw=true" alt="Python code (data prep)">
</a>

## Data prep: Alteryx
I only did the data prep part in Alteryx (I did not use Alteryx to recreate the chart). I would have used the Python tool within Alteryx to generate the chart, so I would have used the same code below.
<br>
<br>
<a href="preppin-data-2021-47.yxzp">
<img src="img-alteryx-2021-47.png?raw=true" alt="Alteryx workflow">
</a>

## Bonus chart: Python
<a href="preppin-data-2021-47.py">
<img src="img-python-code-chart-2021-47.png?raw=true" alt="Python code (chart)">
</a>

#### Chart output:
<img src="img-plot-2021-47.png?raw=true" alt="Chart output">
