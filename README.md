# This readme discribes the code for the log analysis program. 

* Find below the views used to solve each question.
* A text file called test.txt has been attached with output from running the code.
### The database for this analysis is a fictional news database with the following table:
* Author table
* Article table
* Log table
### The questions answered by the log analysis are the following:
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?
### Usage
This projects depends on the following:
* A linux virtual machine:
* https://www.virtualbox.org/wiki/Documentation
* Vagrant:
* https://www.vagrantup.com
* Download the news data (FSND version)
* https://udacity.com/course/full-stack-web-developer-nanodegree
* once downloaded, cd into the directory and run the following command to load the database

```sh
psql -d news -f newsdata.sql
```


# Solution1
### Create view: (article_slug_tite)
```sh
create view article_slug_title as select concat ('/article/', slug) as article_slug, title from articles;
```

# Solution 2:
### Create view: (top_article_paths) 
```sh
create view top_article_paths as select count(*) as views, path from log group by path order by views desc limit 20 offset 1;
```

### Create view: (author_paths_view)
```sh
create view author_paths_view as select concat ('/article/', slug) as article_slug, name from articles, authors where authors.id = articles.author;
```

# Solution 3
### Create view: (date_stat_view)
```sh
create view date_stat_view as select concat(date_part ('year', time), '-', date_part ('month', time), '-', date_part ('day', time)) as new_time, status from log;
```

# Total Count Views as (total_stat_view)
```sh
create view total_stat_view as select new_time, count(*) as total_stats from date_stat_view group by new_time;
```
# Bad Status View as (bad_stat_view)
```sh
create view bad_stat_view as select new_time, count(*) as total_bad_stats from date_stat_view where not status = '200 OK' group by new_time;
```
