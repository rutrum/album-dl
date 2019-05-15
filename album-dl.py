import sys          # sys.exit
import subprocess   # subprocess.call runs shell commands
import os           # os.chdir
import glob         # finding files in pwd
import re           # substituting characters in filenames

import scrapewiki
import tags

def main():
    
    config = askConfig()

    # res = input("Are you sure about this operation? [Y/n] ")
    # if res == "n" or res == "N":
    #     print("Aborting download.")
    #     sys.exit(1)

    print("Downloading metadata...")
    metadata = scrapewiki.scrape(config["wiki-url"])

    print("")
    for key in metadata:
        if key != "tracks" and key != "trackTotal" and key != "image":
            print(key, "\t", metadata[key])
    for track in metadata["tracks"]:
        print(" ", track[0], track[1])
    if metadata["image"]:
        print("Image found.")
    else:
        print("Image was not found.")

    res = input("Confirm this metadata is correct? [Y/n] ")
    if res == "n" or res == "N":
        print("Aborting download.")
        sys.exit(1)

    downloadAudio(config["yt-url"])

    audiofiles = renameFiles()

    map = tags.mapTitlesToFiles(metadata, audiofiles)

    for key in map:
        print("{:<25} {}".format(key, map[key]))

    res = input("Does this map look correct? [Y/n] ")
    if res == "N" or res == "n":
        print("Aborting.")
        sys.exit(1)

    tags.applyTags(metadata, map, "/home/rutrum/music")

    print("Done!")


# Renames mp3 files to ones without symbols
# Returns list of those filesnames
def renameFiles():
    os.chdir("/tmp/album-dl")
    names = glob.glob("*.mp3")
    newNames = []
    for name in names:
        newName = name[:-4] # remove .mp3
        newName = re.sub("[,\-\s'()*.]", "", newName)
        newName = newName + ".mp3"
        subprocess.call(["mv", name, newName])
        newNames.append(newName)
    return newNames
    

def downloadAudio(url):
    print("Audio download starting.")
    ytdl = ["youtube-dl",
        "--ignore-config",
        "-i",
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