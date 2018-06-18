#!/usr/bin/python3
import psycopg2


# Method to find the most popular articles
def popular_articles():
    # Connect to the news database
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    # Query the database and order the results by time
    cursor.execute("""select title, views from article_slug_title,
                   top_article_paths
                   where
                   article_slug_title.article_slug=top_article_paths.path
                   order by views desc limit 4""")
    all_paths = cursor.fetchall()
    db.close()
    return all_paths


# Format the popular articles output to specification.
def format_popular_articles(query_table):
    print("Processing articles report .....")
    # Set the text string formatting
    article_heading = '1 - What are the most popular articles of all time?\n'
    data_values = "".join(
        '\t"{}" -- {}\n'.format(row[0], row[1]) for row in query_table)
    path_data_values = article_heading + data_values
    return path_data_values


# Method to querry for popular authors
def popular_authors():
    # Connect to the news database
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    # Query the database and order the results by time
    cursor.execute("""select name, count(*)
                   as total_count from author_paths_view, log
                   where
                   author_paths_view.article_slug=log.path
                   group by author_paths_view.name
                   order by total_count desc""")
    authors = cursor.fetchall()
    db.close()
    return authors


# Format the popular authors output
def format_popular_authors(query_table):
    print("Processing authors report ......")
    # Set the text string formatting
    report_heading = '\n2 - The most popular article authors?\n'
    data_values = "".join(
        '\t{} -- {} views\n'.format(row[0], row[1]) for row in query_table)
    author_data_values = report_heading + data_values
    return author_data_values


# Method to querry for errors above 1%
def date_errors():
    # Connect to the news database
    db = psycopg2.connect("dbname=news")
    cursor = db.cursor()
    # Query the database and order the results by time
    cursor.execute("""select
                   bad_stat_view.new_time,
                   ((bad_stat_view.total_bad_stats * 100) /
                    total_stat_view.total_stats)
                   from bad_stat_view
                   join
                   total_stat_view
                   on
                   bad_stat_view.new_time=total_stat_view.new_time
                   where
                   ((bad_stat_view.total_bad_stats * 100) /
                    total_stat_view.total_stats) > 1""")
    errors = cursor.fetchall()
    db.close()
    return errors


# Format the error data output
def format_error_data(query_table):
    print("Processing error report .....")
    report_heading = '\n3 - Days with more than 1 % of requests as errors?\n'
    error_values = "".join(
        '\t{} -- {}% errors\n'.format(row[0], row[1]) for row in query_table)
    date_error_values = report_heading + error_values
    return date_error_values


# Make the report text file
text_list = [format_popular_articles(popular_articles()),
             format_popular_authors(popular_authors()),
             format_error_data(date_errors())]


# Write the report to the text file
def write_functions(text_list):
    logfile = open('test.txt', 'w')
    for wm1 in text_list:
        logfile.write(wm1)
    logfile.close()
    print("Find the completed log report in the text.txt file")


# write the report to file.
write_functions(text_list)
