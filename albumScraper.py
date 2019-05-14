from lxml import html
import requests
from bs4 import BeautifulSoup
import re

import sys

def main():

    if len(sys.argv) < 2:
        print("Need wikipedia url as argument.")
    else:

        page = requests.get(sys.argv[1])

        soup = BeautifulSoup(page.text, "lxml")

        data = get_album_data(soup)

        print(data)

def get_album_data(page):

    data = dict()

    table = page.find("table", class_="infobox")
    
    data["artist"] = table.find("div", class_="contributor").string
    data["album"] = table.find("th", class_="album").string

    yearElement = table.find("td", class_="published")
    data["year"] = re.findall("[0-9]{4}", str(yearElement))[0]

    data["genre"] = get_genre(table)

    data["tracks"] = get_titles(page)

    data["trackTotal"] = len(data["tracks"])

    return data

def get_genre(table):

    # First find the text with "Genre"
    genreLink = table.find("a", title="Music genre")

    # Then look at the next sibling of parent and find the first li element
    genreLi = genreLink.parent.next_sibling.find("li")
    if genreLi:
        return genreLi.string.title()
    
    # If that didn't work, its a comma seperated list of links
    return genreLink.parent.next_sibling.a.string.title()


def get_titles(page):

    titles = []

    # Find the first tracklist table
    # Does not work when broken up for mulitple discs 
    # (see https://en.wikipedia.org/wiki/Diver_Down)
    table = page.find("table", class_="tracklist")
    rows = table.find_all("tr")

    for row in rows:
        # Find strings in quotes that follow numbers with periods afterwards
        # This will ignore any extra content next to title name
        # or 'parts' of songs (i.e. 2112 by Rush)
        title = re.findall("([0-9]+)[.].*[\"](.*)[\"]", row.get_text())
        if title:
            title = list(title[0]) # only one occurance in each table row
            title[0] = str(title[0]).zfill(2) # turns 1 into 01
            # print(title[0])
            titles.append(title)

    return titles;
    

if __name__ == '__main__':
    main()