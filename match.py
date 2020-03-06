import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process 
from unidecode import unidecode

def mapTitlesToFiles(tracks, yt_titles):

    mapToFile = {}
    for track in tracks:
        track.update({ "clean": clean_string(track["title"]) })
    for title in yt_titles:
        title.update({ "clean": clean_string(title["title"]) })

    shortToFilename = {}
    for title in yt_titles:
        shortToFilename[title["clean"]] = title["title"]
    yt_shorts = list(map(lambda x: x["clean"], yt_titles))

    for track in tracks:
        # regex = re.compile(r'' + track["clean"])
        # selected_short = list(filter(regex.search, yt_shorts))

        # ERROR HERE
        # Only looks at first match (bad when one song is subtring of another)
        # See saints an sinners by whitesnake
        # selected_file = ""
        # if len(selected_short) > 0:
        #     selected_file = shortToFilename[selected_short[0]]

        selected_short = process.extractOne(track["clean"], yt_shorts)
        selected_file = shortToFilename[selected_short[0]]

        mapToFile[track["title"]] = selected_file

    return mapToFile
        

    for title in data["tracks"]:

        # remove characters inside parenthesis
        short_title = re.sub("(\(.*\))", "", title[1]).strip()
        # remove all other characters
        short_title = re.sub("[^A-Za-z0-9]+", "", short_title)

        regex = re.compile(r'' + short_title, re.IGNORECASE)
        selected_file = list(filter(regex.search, audiofiles))

        if len(selected_file) > 0:
            selected_file = selected_file[0]
        else:
            selected_file = ""

        mapToFile[title[1]] = selected_file
    
    return mapToFile

def clean_string(title):

    # Remove items inside parenthesis and spaces
    title = re.sub("(\(.*\))", "", title).strip()
    title = title.replace(" ", "")

    # Replace special unicode characters with ascii
    title = unidecode(title)

    # Remove all other non numeric or alphabetic symbols
    title = re.sub("[^A-Za-z0-9]+", "", title)

    # change to lowercase
    title = title.lower()

    return title
