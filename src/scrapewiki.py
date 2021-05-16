import requests
from lxml import html
from bs4 import BeautifulSoup
import os

from models import WikiTrack

import re           # For regular expressions
import urllib       # Downloading images from urls

def capture_page(url):
    try:
        raw = requests.get(url)
        page = BeautifulSoup(raw.text, "lxml")
        return page
    except:
        raise Exception("Wikipedia url is not valid.")

def get_metadata(page):

    # Find the metadata table at top of page
    table = page.find("table", class_="infobox")
    if table == None:
        raise Exception("Metadata not found on wiki.")

    data = {}
    
    data["artist"] = table.find("div", class_="contributor").string
    data["album"] = table.find("th", class_="album").string

    yearElement = table.find("td", class_="published")
    data["year"] = re.findall("[0-9]{4}", str(yearElement))[0]

    data["genre"] = get_genre(table)

    # data["tracks"] = get_titles(page)

    # data["trackTotal"] = str(len(data["tracks"]))

    # data["image"] = download_art(table, data["artist"])

    return data

def download_art(page):
    try:
        table = page.find("table", class_="infobox")
        a = table.find("a", class_="image")
        firsturl = "https://wikipedia.org" + a.get('href')

        raw = requests.get(firsturl)
        page = BeautifulSoup(raw.text, "lxml")

        newa = page.find("div", class_="fullImageLink").find("a")
        imageurl = "https:" + newa.get('href')

        urllib.request.urlretrieve(imageurl, "/tmp/album-dl/art.jpg")

    except:
        raise Exception("Failure to find image.")


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


def get_track_tables(page):

    track_tables = []

    tables = page.find_all("table", class_="tracklist")
    for table in tables:
        titles = get_titles_from_table(table)
        track_tables.append(titles)

    return track_tables

def get_tracks(tables, renumber, table_indicies):
    tracks = []
    for renum, i in zip(renumber, table_indicies):
        for new_track in tables[i]:
            if renum:
                new_track.num = len(tracks) + 1
                tracks.append(new_track)
            else:
                same_num = False
                for old_track in tracks:
                    if new_track.num == old_track.num:
                        # if the new track has a number already assigned
                        same_num = True
                if not same_num:
                    tracks.append(new_track)
    return tracks

def get_titles_from_table(table):

    rows = table.find_all("tr")

    titles = []

    for row in rows:
        num = re.findall("([0-9]+)[.]", row.get_text())
        title = re.findall(r'["](.*?)["]', row.get_text())

        if num and title:
            num = num[0]
            title = title[0]
            titles.append(
                WikiTrack(num, title)
            )

    return titles
