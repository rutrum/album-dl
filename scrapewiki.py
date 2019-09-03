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

    tables = page.find_all("table", class_="tracklist")
    possible_titles = []
    for table in tables:
        titles = get_titles_from_table(table)
        possible_titles.append(titles)

    if len(possible_titles) > 1:
        # Ask user which titles to use
        print("We found multiple tables of track information.")
        print("Please enter which tables you would like to use.")
        print("Please use space as delimeter, for example: 1 2")
        print("By default, all tables will be used, in order.")

        for i in range(len(possible_titles)):
            print("**" + str(i) + "**")
            for track in possible_titles[i]:
                print(" ", track[0], track[1])

        res = input("Track tables: ")
        selected_tracks = res.split()
        
        if len(selected_tracks) == 0:
            selected_tracks = range(len(possible_titles))

        tracks = []
        for selection in selected_tracks:
            for new_track in possible_titles[int(selection)]:
                same_num = False
                for old_track in tracks:
                    if new_track[0] == old_track[0]:
                        # if the new track has a number already assigned
                        same_num = True
                if not same_num:
                    tracks.append(new_track)
        return tracks


    else:
        # Only found 1 table, return this
        return possible_titles[0]

def get_titles_from_table(table):

    rows = table.find_all("tr")

    titles = []

    for row in rows:
        # Find strings in quotes that follow numbers with periods afterwards
        # This will ignore any extra content next to title name
        # or 'parts' of songs (i.e. 2112 by Rush)

        # not as much a BUG: Pulls text from second quotes, not first, see Fear Innoculum (Litany against Fear)
        # print(row.get_text())
        # title = re.findall("^([0-9]+)[.]\"([.]+*)\"", row.get_text())
        # (["'])(\\?.)*?\1
        # title = re.findall("([0-9]+)[.].*([\"'])(\\?.)*?\1", row.get_text())
        # print(title)

        # # title = title.reverse()
        # # title = re.findall("([\"'])(\\?.)*?\1", row.get_text())
        # if title:
        #     title = list(title[0]) # only one occurance in each table row
        #     title[0] = str(title[0]).zfill(2) # turns 1 into 01
        #     titles.append(title)

        num = re.findall("([0-9]+)[.]", row.get_text())
        title = re.findall(r'["](.*?)["]', row.get_text())

        if num and title:
            num = num[0]
            title = title[0]
            titles.append([num, title])
        
        print(num, title)

    return titles