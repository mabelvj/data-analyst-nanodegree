# OpenStreetMap Data Case Study
Author: Isabel María Villalba Jiménez

### Map Area
La Cala del Moral, Rincón de la Victoria and Málaga, Province of Málaga, Spain

- [https://www.openstreetmap.org/#map=10/36.6299/-4.4907](https://www.openstreetmap.org/#map=10/36.6299/-4.4907)

This map is of my home village, a peaceful and little village in the outskirts of Málaga and also the map of Málaga área, the capital of the province. I have chosen this area since I am curious to see what database querying reveals and I would like to help improve its mapping on OpenStreetMap.org.


# 1. Data Audit
###Unique Tags
Looking at the XML file (OSM extension, but still XML), I found different types of tags.  Using `1_mapparser.py` I managed to count the unique tags for the Málaga Area.

The results are the following:

```python
{'bounds': 1,
 'member': 22291,
 'meta': 1,
 'nd': 411535,
 'node': 305971,
 'note': 1,
 'osm': 1,
 'relation': 1199,
 'tag': 162389,
 'way': 47490}
 ```

### Patterns in the Tags
The `"k"` value of each tag contain different patterns. Using `2_tags.py`, I created  3 regular expressions to check for certain patterns in the tags.

I have counted each of four tag categories.

*  `"lower" : 129799`, for tags that contain only lowercase letters and are valid,
*  `"lower_colon" : 29506`, for otherwise valid tags with a colon in their names,
*  `"problemchars" : 0`, for tags with problematic characters, and
*  `"other" : 2084`, for other tags that do not fall into the other three categories.


# 2. Problems Encountered in the Map
###Street address inconsistencies

After initially downloading a small sample size of the La Cala del Moral - Málaga area and I could check that the main problem encountered in the dataset is the street name inconsistencies. Below is the old name corrected with the better name. Using `3_audit.py` to update the names.

* **Abbreviations**
    * `CL -> Calle` <sup>*calle : street*</sup>
    * `CR -> Carretera` <sup>*carretera : road*</sup>
    * `Urb -> Urbanización`<sup>*urbanización :  urbanization*</sup>
* **Incorrect street names**
    * `Calle San José -> Calle San Juan`
    * `Paseo Marítimo de La Cala -> Paseo Marítimo Blas Infante`
* **Redundant information**
    * `AVENIDA AVDA -> Avenida`
* **LowerCase**
    * `calle puerta buenaventura -> Calle Puerta Buenaventura`
* **Misspelling**
    * `socity -> Society`
* **Other languages names**
    * `CARRER -> Calle`<sup>*carrer (catalan) : street*</sup>
* **UpperCase Words**
    * `CALLE -> Calle`

# 3. Data Overview
### File sizes:

* `Malaga.osm: 71.9 MB`
* `nodes.csv: 25.1 MB`
* `nodes_tags.csv: 1.3 KB`
* `ways.csv: 2.8 MB`
* `ways_nodes.csv: 9.9 MB`
* `ways_tags.csv: 4.5 MB`
* `Malaga.db: 37.9 MB`

### Open database
In terminal:
``` sql
sqlite3 Malaga.db
```
### Number of nodes:
``` sql
sqlite> SELECT COUNT(*) FROM nodes;
```
**Output:**
```
305971
```

### Number of ways:
```sql
sqlite> SELECT COUNT(*) FROM ways;
```
**Output:**
```
47490
```

### Number of unique users:
```sh
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
**Output:**
```
600
```

### Top contributing users:
```sql
sqlite> SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
```
**Output:**

```sql
dcapillae|65909
CPrados|53834
Parie|43424
Lübeck|37287
Héctor García Pérez|19408
Todie|18402
docmart|5612
Joe E|5490
andi9876|4738
emilkhatib|4636
```

### Number of users contributing only once:
```sql
sqlite> SELECT COUNT(*)
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1) u;
```
**Output:**
```
139
```

# 4. Additional Data Exploration

### Common ammenities:
```sql
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;

```
**Output:**
``` sql
restaurant|315
parking|87
bench|83
cafe|81
bank|80
bar|80
pharmacy|60
fuel|51
drinking_water|35
recycling|34
```

### Biggest religion:
```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 1;
```
**Output:**
```
christian|17
```
### Popular cuisines
```sql
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC;
```
**Output:**
```sql
regional|75
spanish|13
tapas|8
chinese|6
pizza|5
italian|4
asian|3
international|3
seafood|3
burger|2
fish|2
greek|2
Meeresfrüchte-Restaurant|1
american|1
barbecue|1
burguer|1
coffee_shop;moroccan;turkish;vegetarian;arab;crepe;breakfast;pizza;cake;tea|1
japanese|1
mediterranean|1
nepalese-indian|1
noodle|1
spanish;fish;tapas|1
steak|1
steak_house|1
sushi|1
vegetarian|1
```

# 5. Conclusion
The OpenStreetMap data of Ahmedabad is of fairly reasonable quality but the typo errors caused by the human inputs are significant. We have cleaned a significant amount of the data which is required for this project. But, there are lots of improvement needed in the dataset. The dataset contains very less amount of additional information such as amenities, tourist attractions, popular places and other useful interest. The dataset contains very old information which is now incomparable to that of Google Maps or Bing Maps.

So, I think there are several opportunities for cleaning and validation of the data in the future.

### Additional Suggestion and Ideas

#### Control typo errors
* We can build parser which parse every word input by the users.
* We can make some rules or patterns to input data which users follow everytime to input their data. This will also restrict users input in their native language.
* We can develope script or bot to clean the data regularly or certain period.

#### More information
* The tourists or even the city people search map to see the basic amenities provided in the city or what are the popular places and attractions in the city or near outside the city. So, the users must be motivated to also provide these informations in the map.
* If we can provide these informations then there are more chances to increase views on the map because many people directly enter the famous name on the map.

# Files
* `Quiz/` : scripts completed in lesson Case Study OpenStreetMap
* `README.md` : this file
* `ahmedabad_sample.osm`: sample data of the OSM file
* `audit.py` : audit street, city and update their names
* `data.py` : build CSV files from OSM and also parse, clean and shape data
* `database.py` : create database of the CSV files
* `mapparser.py` : find unique tags in the data
* `query.py` : different queries about the database using SQL
* `report.pdf` : pdf of this document
* `sample.py` : extract sample data from the OSM file
* `tags.py` : count multiple patterns in the tags

-------------------------------------------------------------
## Problems Encountered in the Map

After initially downloading a small sample size of the La Cala del Moral - Málaga area and running it against a provisional data.py file, I noticed five main problems with the data, which I will discuss in the following order:


- Over­abbreviated street names  *("CL PZ. CRUZ HUMILLADERO")* and sometimes redundant information*(“AVENIDA AVDA. WASHINGTON-POLIG. EL VISO”)*  
- Inconsistent postal codes *(“NC28226”, “28226­0783”, “28226”)*
- “Incorrect” postal codes (Charlotte area zip codes all begin with “282” however a large portion of all documented zip codes were outside this region.)
- Second­ level `“k”` tags with the value `"type"`(which overwrites the element’s previously processed `node[“type”]field`).
- Street names in second ­level `“k”` tags pulled from Tiger GPS data and divided into segments, in the following format:

	```XML
	<tag k="tiger:name_base" v="Stonewall"/>
	<tag k="tiger:name_direction_prefix" v="W"/>
	<tag k="tiger:name_type" v="St"/>
	```

### Over­abbreviated Street Names
Once the data was imported to SQL, some basic querying revealed street name abbreviations and postal code inconsistencies. To deal with correcting street names, I opted not use regular expressions, and instead iterated over each word in an address, correcting them to their respective mappings in audit.py using the following function:

```python
def update(name, mapping):
	words = name.split()
	for w in range(len(words)):
		if words[w] in mapping:
			if words[w­1].lower() not in ['suite', 'ste.', 'ste']:
				# For example, don't update 'Suite E' to 'Suite East'
				words[w] = mapping[words[w]] name = " ".join(words)
	return name
```

This updated all substrings in problematic address strings, such that:
*“S Tryon St Ste 105”*
becomes:
*“South Tryon Street Suite 105”*

### Postal Codes
Postal code strings posed a different sort of problem, forcing a decision to strip all leading and trailing characters before and after the main 5­digit zip code. This effectively dropped all leading state characters (as in “NC28226”) and 4­digit zip code extensions following a hyphen (“28226­0783”). This 5­digit restriction allows for more consistent queries.


Regardless, after standardizing inconsistent postal codes, some altogether “incorrect” (or perhaps misplaced?) postal codes surfaced when grouped together with this aggregator:

```sql
SELECT tags.value, COUNT(*) as count
FROM (SELECT * FROM nodes_tags
	  UNION
      SELECT * FROM ways_tags) tags
WHERE tags.key='postcode'
GROUP BY tags.value
ORDER BY count DESC;
```

Here are the top ten results, beginning with the highest count:

```sql
value|count
29620|150
29018|46
29004|39
29002|32
29130|22
29016|21
29730|19
29720|18
29017|15
29014|14
29007|13
29010|12
29001|11
29006|11
29012|11
29005|10
29015|10
29008|7
29013|7
29790|7
29140|5
29071|4
29003|3
29011|3
29791|3
29590|2
29738|2
24190|1
29.730|1
29009|1
2910|1
29196|1
```

 These results were taken before accounting for Tiger GPS zip codes residing in second­ level “k” tags. Considering the relatively few documents that included postal codes, of those, it appears that out of the top ten, seven aren’t even in Charlotte, as marked by a “#”. That struck me as surprisingly high to be a blatant error, and found that the number one postal code and all others starting with“297”lie in Rock Hill, SC. So, I performed another aggregation to verify a certain suspicion...
# Sort cities by count, descending

```sql
sqlite> SELECT tags.value, COUNT(*) as count
FROM (SELECT * FROM nodes_tags UNION ALL
      SELECT * FROM ways_tags) tags
WHERE tags.key LIKE '%city'
GROUP BY tags.value
ORDER BY count DESC;
```

And, the results, edited for readability:

```sql
Málaga|320
Torremolinos|128
Alhaurín de la Torre|32
Malaga|24
La Cala del Moral|10
Churriana|8
Rincón de la Victoria|8
Chilches|7
24|4
30|4
Macharaviaya|3
15|2
20|2
5|2
8|2
Campanillas|2
0|1
1|1
13|1
14|1
1533|1
17|1
18|1
21|1
22|1
250|1
36|1
37|1
48|1
50|1
500|1
732|1
968|1
La Araña|1
MALAGA|1
MÁLAGA|1
Mälaga|1
Rincon de la Victoria|1
Torre de Benagalbón|1
no|1       
```

These results confirmed my suspicion that this metro extract would perhaps be more aptly named “Metrolina” or the “Charlotte Metropolitan Area” for its inclusion of surrounding cities in the sprawl. More importantly, three documents need to have their trailing state abbreviations stripped. So, these postal codes aren’t “incorrect,” but simply unexpected. However, one final case proved otherwise.
A single zip code stood out as clearly erroneous. Somehow, a “48009” got into the dataset. Let’s display part of its document for closer inspection (for our purposes, only the “address” and “pos” fields are relevant):

```sql
SELECT *
FROM (SELECT * FROM nodes_tags
	  UNION ALL
      SELECT * FROM ways_tags) tags
WHERE tags.key='postcode' and tags.value="29.730";
```


```sql
sqlite> SELECT *
FROM ways
WHERE id IN (SELECT DISTINCT(id) FROM ways_tags WHERE key='postcode' AND value='29.730');
```
`397816252|Parie|246941|2|46025352|2017-02-12T17:15:10Z`

```sql
sqlite> SELECT * FROM ways_tags WHERE id=397816252 and type='addr';
```
```sql
397816252|city|Rincón de la Victoria|addr
397816252|housenumber|230|addr
397816252|postcode|29.730|addr
397816252|street|Avenida de la Mediterráneo|addr
```

 It turns out, *“280 North Old Woodward Avenue, 48009”* is in Birmingham, Michigan. All data in this document, including those not shown here, are internally consistent and verifiable, except for the latitude and longitude. These coordinates are indeed in Charlotte, NC. I’m not sure about the source of the error, but we can guess it was most likely sitting in front of a computer before this data entered the map. The document can be removed from the database easily enough.

# Data Overview and Additional Ideas
This section contains basic statistics about the dataset, the MongoDB queries used to gather them, and some additional ideas about the data in context.

### File sizes
```
charlotte.osm ......... 294 MB
charlotte.db .......... 129 MB
nodes.csv ............. 144 MB
nodes_tags.csv ........ 0.64 MB
ways.csv .............. 4.7 MB
ways_tags.csv ......... 20 MB
ways_nodes.cv ......... 35 MB  
```  





# Additional Ideas

## Contributor statistics and gamification suggestion
The contributions of users seems incredibly skewed, possibly due to automated versus manual map editing (the word “bot” appears in some usernames). Here are some user percentage statistics:

- Top user contribution percentage (“jumbanho”) 52.92%
- Combined top 2 users' contribution (“jumbanho” and “woodpeck_fixbot”) 83.87%
- Combined Top 10 users contribution
94.3%
- Combined number of users making up only 1% of posts 287 (about 85% of all users)

Thinking about these user percentages, I’m reminded of “gamification” as a motivating force for contribution. In the context of the OpenStreetMap, if user data were more prominently displayed, perhaps others would take an initiative in submitting more edits to the map. And, if everyone sees that only a handful of power users are creating more than 90% a of given map, that might spur the creation of more efficient bots, especially if certain gamification elements were present, such as rewards, badges, or a leaderboard.

## Additional Data Exploration

### Top 10 appearing amenities


### Biggest religion (no surprise here)

### Most popular cuisines


# Conclusion
 After this review of the data it’s obvious that the Charlotte area is incomplete, though I believe it has been well cleaned for the purposes of this exercise. It interests me to notice a fair amount of GPS data makes it into OpenStreetMap.org on account of users’ efforts, whether by scripting a map editing bot or otherwise. With a rough GPS data processor in place and working together with a more robust data processor similar to data.pyI think it would be possible to input a great amount of cleaned data to OpenStreetMap.org.

 ---------------------------


-- Street named "CARRER" in catalan: while map is in spanish.
- CL: Calle
--------------------------------------------------
