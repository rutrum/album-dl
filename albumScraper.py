import requests
from lxml import html
from bs4 import BeautifulSoup

import re           # For regular expressions
import sys          # For system arguments
import glob         # For finding audio files
import os           # For change current directory
import subprocess   # For running shell commands

def main():

    # if len(sys.argv) < 2:
    #     print("Need wikipedia url as argument.")
    #     sys.exit(1)
    
    # page = requests.get(sys.argv[1])
    page = requests.get("https://en.wikipedia.org/wiki/Twilight_in_Olympus")
    soup = BeautifulSoup(page.text, "lxml")
    data = get_album_data(soup)

    # print(data)

    os.chdir("/tmp")
    audiofiles = glob.glob("*.mp3")
    # print(audiofiles)

    map = mapTitlesToFiles(data, audiofiles)

    # WARNING
    # Confirm with user that mapping is correct

    # print(map)

    applyTags(data, map)
    

def applyTags(data, map):

    # Create new folder to move files into
    newDir = "/home/rutrum/music/" + data["artist"] + "/" + data["album"]
    subprocess.call(["mkdir", "-p", newDir])

    for track in data["tracks"]:
        audiofile = map[track[1]]
        
        # First apply tags
        tagCommand = ["mid3v2", audiofile,
            "-a", data["artist"],
            "-A", data["album"],
            "-g", data["genre"],
            "-y", data["year"],
            "-T", track[0] + "/" + data["trackTotal"],
            "-t", track[1]]
        subprocess.call(tagCommand)

        # Now rename the file
        newName = track[0] + " " + track[1] + ".mp3"
        renameCommand = ["mv", audiofile, newName]
        subprocess.call(renameCommand)

        # Move the file to ~/music/artist/album/
        subprocess.call(["cp", newName, newDir])
        



# Currently pattern matches on song titles,
# in future should probably be song index, since song titles
# can vary greatly across documentation
def mapTitlesToFiles(data, audiofiles):
    mapToFile = dict()

    for title in data["tracks"]:
        title = title[1]

        regex = re.compile(r'' + title, re.IGNORECASE)
        selected_file = list(filter(regex.search, audiofiles))

        if len(selected_file) > 0:
            selected_file = selected_file[0]
        else:
            selected_file = ""

        mapToFile[title] = selected_file
    
    return mapToFile


def get_album_data(page):

    data = dict()

    table = page.find("table", class_="infobox")
    
    data["artist"] = table.find("div", class_="contributor").string
    data["album"] = table.find("th", class_="album").string

    yearElement = table.find("td", class_="published")
    data["year"] = re.findall("[0-9]{4}", str(yearElement))[0]

    data["genre"] = get_genre(table)

    data["tracks"] = get_titles(page)

    data["trackTotal"] = str(len(data["tracks"]))

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
            titles.append(title)

    return titles;
    

if __name__ == '__main__':
    main()