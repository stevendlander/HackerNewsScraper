#!/usr/local/bin/python3

# Author: Steven Lander
# Created: Aug 2019

import csv
from argparse import ArgumentParser

def get_html(url):
    from urllib.request import urlopen
    page = urlopen(url)
    return page.read()

def soupify(html):
    from bs4 import BeautifulSoup
    return BeautifulSoup(html, features="lxml")

def write_csv(soup_results):
    csv_title = soup_results.title.get_text().replace(" ", "") + ".csv"
    with open(csv_title, "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        spans = soup_results.find_all("span", {"class": "commtext c00"})
        writer.writerows(spans)
    return csv_title

def get_clean_name(name):
    front, back = name.split(".")
    return front + "_clean." + back

def generate_header():
    header = [
        "Location",
        "Remote",
        "Willing to relocate",
        "Technologies",
        "Resume/CV",
        "Email",
    ]
    return header


def remove_html(row):
    replaced = string_replace_tags(row)
    regexed = regex_sub_tags(replaced)
    return regexed

def string_replace_tags(row):
    tags_to_remove = [
        "<p>",
        "</p>",
        "</a>",
        "<i>",
        "</i>",
        "<pre>",
        "</pre>",
        "<code>",
        "</code>",
    ]
    for tag in tags_to_remove:
        row = [ cell.replace(tag, "") for cell in row ]
    return row

def regex_sub_tags(row):
    from re import sub
    tags_to_sub = ["\<a.*\>"] 
    for tag in tags_to_sub:
        row = [ sub(tag, "", cell) for cell in row ]
    return row

def cleanup_location(csv_dirty):
    csv_clean = get_clean_name(csv_dirty)
    with open(csv_clean, "w", encoding="utf-8") as clean_file:
        writer = csv.writer(clean_file)
        with open(csv_dirty, "r", encoding="utf-8") as dirty_file:
            reader = csv.reader(dirty_file)
            writer.writerow(generate_header())
            for row in reader:
                if "location" in row[0].lower():
                    cleaned_row = remove_html(row)
                    writer.writerow(cleaned_row)

def main(arg_list):
    html = get_html(arg_list.url)
    results = soupify(html)
    csv_dirty = write_csv(results)
    cleanup_location(csv_dirty)

if __name__ == "__main__":
    PARSER = ArgumentParser(description="Pull entries from Hacker News Jobs URL")
    PARSER.add_argument("url", metavar="url", help="Hacker News 'Who wants to be hired' URL")
    ARG_LIST = PARSER.parse_args()
    
    if ARG_LIST.url is None:
        PARSER.print_usage()
        print("Ensure you specify a valid URL to Hacker News URL")
        exit(1)
    main(ARG_LIST)
