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
    output_string_format = '"%s" -- %s views\n'
    path_data_values = "".join(
        output_string_format % (title, count) for title, count in query_table)
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
    output_string_format = '%s -- %s views\n'
    author_data_values = "".join(output_string_format % (author, article_count)
                                 for author, article_count in query_table)
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
    # Set the text string formatting
    output_string_format = '%s -- %s%s'
    date_error_values = "".join(
        output_string_format % (date, str(error_percent), '% errors')
        for date, error_percent in query_table)
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
