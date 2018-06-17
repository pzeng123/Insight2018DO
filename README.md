# Appartment/Housing/Rooms rent for commuters
## Find the living place has the shortest commute time

workfriendly don't waste time commuting

minute commute



## Summary:
Help people find appartment/room rent information which has less commute time


## Purpose and most common use cases
when people search appartment rent informaton (on craigslist for example), they are usually only can limit the "miles from zip".
While distance is important, it is more critical that we need to consider the commute time (car, bus, bike, walk). Moreover, we can add more similar features in different versions, such as showing the time not only to the working location, but also other places (hospital, schools, grocery stores)


Combine these two:
![image](/img/1.png "image 1")



## Data Engineering technologies


* Data: S3
* ~~（Preprocessing/data streaming: Kafka-Spark）~~(not enough large data set)
* Database: MySQL
* Web application UI: Flask


#### Scrapy apartment rental data from craigslist ->
from 5 areas in SF-Bay area(AREAS = ["eby", "sfc", "sby", "nby", "pen"]), each 20 newest results.

```
(venv) peng@ubuntu:~/myproject/apartment-finder$ python scraper.py
Fri Apr 27 13:04:27 2018: Got 96 results
```

#### -> Data saved in database (MYSQL/SQLITE)
```
from sqlalchemy import create_engine
...
engine = create_engine('sqlite:///listings.db', echo=False)
```

#### -> Google map API get the commute time (2500/day limit)

```
(venv) peng@ubuntu:~/myproject/apartment-finder$ python googlemap1.py
****************************
37.4673,-122.1388
driving: 10 mins
walking: 1 hour 13 mins
bicycling: 22 mins
transit: 46 mins
****************************
37.7024,-122.124
driving: 37 mins
walking: 8 hours 0 mins
bicycling: 2 hours 19 mins
transit: 1 hour 42 mins
****************************
```
#### -> Display on Web UI (Flask)


#### -> Container technology for Devops
 Docker -> Kubernetes




## Devops flow

* Source control: Github
* Continuous integration and deployment: Jenkins
* Container: Docker, Kubernetes


##
```
sudo docker-compose build
sudo docker-compose up -d
sudo docker-compose run --rm web python ./instance/db_create.py
```








