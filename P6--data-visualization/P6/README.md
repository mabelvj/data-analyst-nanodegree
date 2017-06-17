# Summary 
In this project it will be visualized the health investment versus the life expectancy at birth in the year 2014 for all countries in the world. The question is simple: **does health spending influences directly the life expectancy?** 

The data will be plotted in five different graphs, one per continent, keeping in mind that nearest countries may have similar conditions and it is easier to compare between them.The data is extracted from the **World Data Bank** [[source]](http://databank.worldbank.org/data/reports.aspx?source=2&series=SH.XPD.PUBL&country=#advancedDownloadOptions).

<!-- In no more than 4 sentences, briefly introduce your data visualization and add any context that can help readers understand it -->
# Design 
The first aim of the project was to be able to represent the data in a clear way. After plotting the data altogether, I decided to implement an algorithm to filter the data and asign them their correspondent continent, so as to be able to plot them separately.

> Last graph is saved in index.html and also in that with the highest index (i.e. index9.html). The first graph has the lowest index (in this case index0.html.

The process of design of the graph has had the following steps:

1. Created a slopegraph showing lines between two variables: one related to **money spent in health care** and the other as **life expectancy at date of birth**.
	-	Showed all connections, names of countries and data on each side.
	-	Highlighted a line when putting the mouse over it and printed country and data related.
2. Removed all data printed and **highlighted only the line on mouse over**.
3. Left only maximum and minimum values for left and right variables.
	-  Printed **lines connecting means** between each side of the graph. 
	-  Set values to diplay only 1 decimal point.
4. Made data to appear when setting the mouse over the lines. 
	-	Show country and data for left and right variable
5. **Separated data by continents**.Added variable names.
	- Dimmed axis labels
	- Increased continent labels to 24px.
6. Added **global mean** and **continental mean**. Also dimmed out the lines. Means now dissapear when pointer is selecting a line.
7. Added **menu** to select variable in the left.
	- "Health expenditure per capita(current US$)" is the variable more correlated with "Life expectancy at birth, total(years)"
8. Added **main title** and **subtitle** describing variables plotted. Removed names of variables from each side of the graphs. Placed the menu in the top right of the page.
	- Adjusted width to  10246x500px to be displayed on most computers. 
	- Sent everything to background

9. Only current graph data goes out when selecting a line.
	- Decreased description font-size
	- Removed "per continent", since it is obvious and it adds clutter.
	- Mean tags are only shown for the first graphic
	- Dashed line for global mean.
10. Added conclusions	

11. Incremented font sizes. Removed values for the global mean and only left it in the first graph. Legend appears only for the first graph.

# Feedback
Asked 3 people to give feedback on the project:
	1. Suggested to remove all data and only show the one under the mouse.
	2. Suggested to display different variables and to give explanatory sentences.
	3. Suggested to increase the width of the lines when setting the mouse over the lines

## Suggestions
Other suggestions but not implemented at the moment were:
	- Compare EU members vs non-members
	- Highlight main countries (highest population or highest income)
	- Be able to search and select for specific countries.
	- Plot sub-regions (i.e. Central Europe, South Europe...)

# Conclusions
	- In general: the higher the amount spent the greater the life expectancy.
	- Europe is the continent spending more money on health whereas Africa shows the lowes rate in health expenditure. This is reflected on the average life expectancy of both countries: Europe has an average life expentancy of 78.8 years where in Africa it is  61.3 years.
	- Some countries show that other factors may be taken into account: i.e. U.S. being one of the countries with highest spending but not reflected in a longer life. Other countries, like Spain or Italy, do not have that health investment per capita, but life expectancy is higher. One factor that may be influecing this results is diet: junk food (U.S.) vs mediterranean (Spain, Italy).
	

# Resources
- Data [http://databank.worldbank.org/data/reports.aspx?source=2&series=SH.XPD.PUBL&country=#advancedDownloadOptions](http://databank.worldbank.org/data/reports.aspx?source=2&series=SH.XPD.PUBL&country=#advancedDownloadOptions) 
- Slopegraph [http://bl.ocks.org/zbjornson/2547496](http://bl.ocks.org/zbjornson/2547496)
 - Wrap function [http://bl.ocks.org/mbostock/7555321](http://bl.ocks.org/mbostock/7555321)
-Nest [http://bl.ocks.org/phoebebright/raw/3176159/](http://bl.ocks.org/phoebebright/raw/3176159/)