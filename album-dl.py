import sys          # sys.exit
import subprocess   # subprocess.call runs shell commands
import os           # os.chdir
import glob         # finding files in pwd

import scrapewiki
import tags

def main():
    
    config = askConfig()

    res = input("Are you sure about this operation? [Y/n] ")
    if res == "n" or res == "N":
        print("Aborting download.")
        sys.exit(1)

    metadata = scrapewiki.scrape(config["wiki-url"])

    print("")
    for key in metadata:
        if key != "tracks" and key != "trackTotal":
            print(key, ":", metadata[key])
    for track in metadata["tracks"]:
        print(" ", track[0], track[1])

    res = input("Confirm this metadata is correct? [Y/n] ")
    if res == "n" or res == "N":
        print("Aborting download.")
        sys.exit(1)

    # downloadAudio(config["yt-url"])

    audiofiles = getFilenames()

    map = tags.mapTitlesToFiles(metadata, audiofiles)

    for key in map:
        print(key, ":", map[key])

    res = input("Does this map look correct? [Y/n] ")
    if res == "N" or res == "n":
        print("Aborting.")
        sys.exit(1)

    tags.applyTags(metadata, map, "/home/rutrum/music")

    print("Done!")


def getFilenames():
    os.chdir("/tmp/album-dl")
    return glob.glob("*.mp3")
    

def downloadAudio(url):
    print("Audio download starting.")
    ytdl = ["youtube-dl",
        "--ignore-config",
        "-x", "--audio-format", "mp3",
        "-o", r"/tmp/album-dl/%(title)s.%(ext)s",
        url]
    subprocess.call(ytdl)

def askConfig():
    config = dict()

    print("Please enter playlist url:")
    ytURL = input()

    print("Please enter wikipedia album url:")
    wikiURL = input()

    config["yt-url"] = ytURL
    config["wiki-url"] = wikiURL
    
    return config


if __name__ == '__main__':
    main()