import requests
from lxml import html
from bs4 import BeautifulSoup

import re           # For regular expressions
import urllib       # Downloading images from urls

def scrape(url):

    raw = requests.get(url)
    page = BeautifulSoup(raw.text, "lxml")

    data = dict()

    table = page.find("table", class_="infobox")
    
    data["artist"] = table.find("div", class_="contributor").string
    data["album"] = table.find("th", class_="album").string

    yearElement = table.find("td", class_="published")
    data["year"] = re.findall("[0-9]{4}", str(yearElement))[0]

    data["genre"] = get_genre(table)

    data["tracks"] = get_titles(page)

    data["trackTotal"] = str(len(data["tracks"]))

    data["image"] = download_art(table, data["artist"])

    return data

def download_art(table, album):

    try:
    
        a = table.find("a", class_="image")
        firsturl = "https://wikipedia.org" + a.get('href')

        raw = requests.get(firsturl)
        page = BeautifulSoup(raw.text, "lxml")

        newa = page.find("div", class_="fullImageLink").find("a")
        imageurl = "https:" + newa.get('href')

        urllib.request.urlretrieve(imageurl, "/tmp/album-dl/art.jpg")

    except:
        return False

    return True


def get_genre(table):

    # First find the text with "Genre"
    genreLink = table.find("a", title="Music genre")

    # Then look at the next sibling of parent and find the first li element
    genreLi = genreLink.parent.next_sibling.find("li")
    if genreLi and genreLi.a:
        return genreLi.a.string.title()
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
            titles.append(title)

    return titles;