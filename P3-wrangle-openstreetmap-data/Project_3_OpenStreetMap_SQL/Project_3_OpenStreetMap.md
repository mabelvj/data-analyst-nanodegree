# OpenStreetMap Data Case Study

>**Author**: Isabel María Villalba Jiménez
>
>**Date**: March 20th, 2017

# 0. Map Area
La Cala del Moral, Rincón de la Victoria and Málaga, Province of Málaga, Spain

- [https://www.openstreetmap.org/#map=10/36.6299/-4.4907](https://www.openstreetmap.org/#map=10/36.6299/-4.4907)

This map is of my home village, a peaceful and little village in the outskirts of Málaga and also the map of Málaga area, the capital of the province. I have chosen this area since I am curious to see what database querying reveals and I would like to help improve its mapping on OpenStreetMap.org.


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
The `"k"` value of each tag contain different patterns. Using `2_tags.py`, I created 3 regular expressions to check for certain patterns in the tags: tags with only lower case letters, tags with a colon in their names and problematic chars.

The resulting count is the following:

*  `"lower" : 129799`, for tags that contain only lowercase letters and are valid,
*  `"lower_colon" : 29506`, for otherwise valid tags with a colon in their names,
*  `"problemchars" : 0`, for tags with problematic characters, and
*  `"other" : 2084`, for other tags that do not fall into the other three categories.


# 2. Problems Encountered in the Map
## Street address inconsistencies

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

### Abbreviations
I have created a dictionary in order to translate abbreviations appearing into the correct long desired expression. The update of the names is made through an update function as follows:

```python
mapping = { "C/": "Calle",
            "Clle": "Calle",
            "CL": "Calle",
            "CARRER": "Calle",
            "Ctra": "Carretera",
            "Ctra.": "Carretera",
            "CR" : "Carretera",
            "Av": "Avenida",
            "Av.": "Avenida",
            "Avd": "Avenida",
            "Avd.": "Avenida",
            "Avda": "Avenida",
            "Avda.": "Avenida",
            "Pza" : "Plaza",
            "Pza.": "Plaza",
            "Pz": "Plaza",
            "Pz.": "Plaza",
            "PZ" : "Plaza",
            "PZ.": "Plaza",
            "Plza": "Plaza",
            "Plza.": "Plaza",
            "Urb." : u"Urbanización",
            "Urb" : u"Urbanización",
            "Polig" : u"Polígono",
            "Polig." : u"Polígono",
            "Blq." : "Bloque",
            "Blq" : "Bloque"
            }


def update_name(name, mapping):
    return street_type_re.sub(lambda x: mapping[x.group()], name)

```

This way abbreviations will be corrected, i.e. "CL PZ. CRUZ HUMILLADERO -> Calle Plaza CRUZ HUMILLADERO".

### Postal Codes
Postal codes appearing in this area are mostly correct. The following query was used:

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

There is an inconsistency, for the 29.730 case. We should correct this particular case and remove dots appearing in postal codes.

I tried to get more information about this only incorrect case. After trying in nodes and ways I was able to locate the problematic case in the `ways` table.

```sql
SELECT *
FROM ways
WHERE id IN (SELECT DISTINCT(id) FROM ways_tags WHERE key='postcode' AND value='29.730');
```
`397816252|Parie|246941|2|46025352|2017-02-12T17:15:10Z`

Using the user id `397816252` I could fetch more info:

```sql
SELECT * FROM ways_tags WHERE id=397816252 and type='addr';
```

```sql
397816252|city|Rincón de la Victoria|addr
397816252|housenumber|230|addr
397816252|postcode|29.730|addr
397816252|street|Avenida de la Mediterráneo|addr
```

I was able to correct the error with the following query:

```sql
UPDATE ways_tags SET value= 29730 WHERE value="29.730" and key ="postcode" and type='addr';
```
# Sort cities by count, descending

```sql
SELECT tags.value, COUNT(*) as count
FROM (SELECT * FROM nodes_tags UNION ALL
      SELECT * FROM ways_tags) tags
WHERE tags.key LIKE '%city'
GROUP BY tags.value
ORDER BY count DESC;
```

Results, edited for readability:

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

Some misspellings appear requiring correction:

CORRECT                 | INCORRECT
----------              |---------------------------
Málaga                  | Malaga, MALAGA, MÁLAGA, Mälaga
Rincón de la Victoria   | Rincon de la Victoria


These errors can be corrected (i.e.('Malaga -> 'Málaga'')) with the following query:

```sql
UPDATE ways_tags
SET value= N'Málaga'
WHERE value='Malaga' and key LIKE '%city';

```
I implemented a script named `7_correct_cities.py` that iterates over a dictionary and corrects the misspellings.

```python
mapping = { u'Malaga': u'Málaga',
			u'MALAGA': u'Málaga',
			u'MÁLAGA': u'Málaga',
			u'Mälaga': u'Málaga',
			u'Rincon de la Victoria': u'Rincón de la Victoria'}

with sqlite3.connect(db_filename) as conn:
	cursor = conn.cursor()
	query_nodes = """UPDATE nodes_tags SET value = :value WHERE value = :value2 and key LIKE '%city'"""
	query_ways = """UPDATE ways_tags SET value = :value WHERE value = :value2 and key LIKE '%city'"""

	for key, value in mapping.items():
	    #iterate over the dict and update each value in each table
	    cursor.execute(query_nodes, {'value':value, 'value2': key})
	    cursor.execute(query_ways, {'value':value, 'value2': key})
	    conn.commit()
conn.close()
```

>These solutions should work, but **unfortunately**, it is not completely implemented the **compatibility between sqlite and latin characters**, so **accented letters are not recognized**.

>I have tried to find a workaround but it seems too excessively complicated when compared to the scope of this work.

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
SELECT COUNT(*) FROM nodes;
```
**Output:**
```
305971
```

### Number of ways:
```sql
SELECT COUNT(*) FROM ways;
```
**Output:**
```
47490
```

### Number of unique users:
```sh
SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
**Output:**
```
600
```

### Top contributing users:
```sql
SELECT e.user, COUNT(*) as num
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
I got quite surprise here since I know one of the guys contributing.

### Number of users contributing only once:
```sql
SELECT COUNT(*)
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
SELECT value, COUNT(*) as num
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
The most common ammenities are the restaurants (remember Spain is the place of the work with more restaurants per inhabitant), followed by parkings, benches and cafes.

### Biggest religion:
```sql
SELECT nodes_tags.value, COUNT(*) as num
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
No surprise here, the most common religion is christianism.
### Popular cuisines
```sql
SELECT nodes_tags.value, COUNT(*) as num
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
Most popular type of food in the area are: `regional`, followed by `spanish` and `tapas`, but quite often, the are synonyms.

# 5. Conclusion
The OpenStreetMap data of the Málaga area is of fairly reasonable quality but there are some errors due to Spanish special characters compatibility. W

I have cleaned a fair amount of data, and processed abbreviations occurring.
Still, there is a lot of work pending related to special character in order to have a consistent dataset. Fortunately, these errors do not affect the readability of the maps.

### Additional Suggestion and Ideas

#### Control typo errors
* Build a parser for the `csv` file to intensively find error patters, involving special characters, before writing into database. The `csv` had special characters and they were all written into de database, so this could work.

    - **Benefits**: having special characters corrected will result in a cleaner and more standardized outlook of the information.
    
    - **Anticipated issues**: it may be hard to deal with special characters in a SQL environment. Some users may not have compatibility with the special characters: using `UTF-8` is encouraged.
    
    
* Make format rules clear so the users know the format required for inserting the information. Rules must be clear and easy to follow.

    - **Benefits**: stating rules will result in a more professional and standardized information.
    
    - **Anticipated issues**:  some users may have problems following the standardizing rules and other may just skip them and directly insert information at their will.
    
    
* Develop a script or bot to clean the data regularly or certain period.

    - **Benefits**: the script will help to keep the quality of the map up to a good level with a continuous basis.
    
    - **Anticipated issues**: continuous work in the script must be done in order to keep it continuously improving and detecting new variations in the patterns of the information inserted by users.

# Files
* `Project_3_OpenStreetMap.md` : this file
* `Project_3_OpenStreetMap.pdf` : pdf of this document
* `README.md`: a copy of this file
* `Malaga.osm`: too big, export it from here  [https://www.openstreetmap.org/#map=10/36.6299/-4.4907](https://www.openstreetmap.org/#map=10/36.6299/-4.4907) (results may be different since I selected the area manually)
* `1_mapparser.py` : find unique tags in the data
* `2_tags.py` : find errors in the data
* `3_audit.py` : audit street, city and update their names
* `4_data.py` : build CSV files from OSM and also parse, clean and shape data
* `5_create_database.py` : create database from the `data_wrangling.sql` schema
* `6_csv_to_db.py`: insert the values from the CSV files into the database
* `7_correct_cities.py`: script to correct misspelling appearing in city names
* `data_wrangling.sql`: supplied schema for the SQL database structure

# References
1. [OpenStreetMap Data Case Study by Carlward](https://gist.github.com/carlward/54ec1c91b62a5f911c42#file-sample_project-md)
2. [OpenStreetMap Data Case Study by Pratyush Kumar](https://github.com/pratyush19/Udacity-Data-Analyst-Nanodegree/tree/master/P3-OpenStreetMap-Wrangling-with-SQL)
3. [OSM_XML reference guide by OpenStreetMap](http://wiki.openstreetmap.org/wiki/OSM_XML)
4. [Nodes reference guide by OpenStreetMap](http://wiki.openstreetmap.org/wiki/Node)
5. [Ways reference guide by OpenStreetMap](http://wiki.openstreetmap.org/wiki/Way)
6. [SQL schema](https://gist.github.com/swwelch/f1144229848b407e0a5d13fcb7fbbd6f)
7. [sqlite3 reference guide](https://pymotw.com/2/sqlite3/)
