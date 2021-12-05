# bleepingComputerScraper
Scrapes the forum from bleeping computer


1. Download this repo

2. pip install scrapy scrapy_useragents pymongo

3. download docker image for mongo 
docker pull mongo

4. run mongo 

docker run --name some-mongo -v /data/data1/bleeping/mongodb:/data/db  -p 27017 -d mongo

5. run scraper 

scrapy crawl forum_post_scraper

