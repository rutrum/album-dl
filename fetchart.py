import os
import requests
from lxml import html
from bs4 import BeautifulSoup
import urllib       # Downloading images from urls

def main():

    print("Please enter wikipedia url: ")
    wikiURL = input()
    print("Please enter output file.  Default is /tmp/album-dl/art.jpg")
    location = input()
    if location == "":
        location = "/tmp/album-dl/art.jpg"

    raw = requests.get(wikiURL)
    page = BeautifulSoup(raw.text, "lxml")

    table = page.find("table", class_="infobox")
    album = table.find("th", class_="album").string

    success = fetch_art(table, album, location)

    if success:
        print("Done!")
    else:
        print("Image not found.")


def fetch_art(table, album, location):

    print("Downloading image...")
    try:
    
        a = table.find("a", class_="image")
        firsturl = "https://wikipedia.org" + a.get('href')

        raw = requests.get(firsturl)
        page = BeautifulSoup(raw.text, "lxml")

        newa = page.find("div", class_="fullImageLink").find("a")
        imageurl = "https:" + newa.get('href')

        folder = "/".join(location.split("/")[:-1])
        if not os.path.exists(folder):
            os.makedirs(folder)

        urllib.request.urlretrieve(imageurl, location)

    except Exception as e:
        print(e)
        return False

    return True


if __name__ == "__main__":
    main()
