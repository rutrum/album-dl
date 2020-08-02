from unidecode import unidecode
from bs4 import BeautifulSoup
import re

class YTVideo:
    
    def __init__(self, metadata):
        self.id = metadata["id"]
        self.title = metadata["title"]
        # considering using .lower() but may be unnecessary
        self.clean = unidecode(self.title)

    def filename(self):
        return "{}.mp3".format(self.id)


class WikiTrack:
    
    def __init__(self, num, title):
        self.num = num
        self.title = title
        # considering using .lower() but may be unnecessary
        self.clean = unidecode(self.title)


class Metadata:

    def __init__(self, table):
        self.artist = table.find("div", class_="contributor").string
        self.album = table.find("th", class_="album").string

        yearElement = table.find("td", class_="published")
        self.year = re.findall("[0-9]{4}", str(yearElement))[0]

        self.genre = self.get_genre(table)

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


# Just for reference
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
