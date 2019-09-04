import re           # for regular expressions
import subprocess   # subprocess.call runs shell commands

def applyTags(data, map, save):

    # Create new folder to move files into
    newDir = save + "/" + data["artist"] + "/" + data["album"]
    subprocess.call(["mkdir", "-p", newDir])

    for track in data["tracks"]:
        audiofile = map[track[1]]
        if audiofile == "": continue # When track was not downloaded
        
        # First apply tags
        tagCommand = ["mid3v2", audiofile,
            "-a", data["artist"],
            "-A", data["album"],
            "-g", data["genre"],
            "-y", data["year"],
            "-T", track[0] + "/" + data["trackTotal"],
            "-t", track[1]]
        subprocess.call(tagCommand)

        # Add image tag if it was found
        if data["image"]:
            tagCommand = ["mid3v2", audiofile,
                "-p", "/tmp/album-dl/art.jpg"]
            subprocess.call(tagCommand)
            

        # Now rename the file
        title = re.sub("/", " - ", track[1])
        newName = track[0] + " " + track[1] + ".mp3"
        renameCommand = ["mv", audiofile, newName]
        subprocess.call(renameCommand)

        # Move the file to ~/music/artist/album/
        subprocess.call(["mv", newName, newDir])


# Currently pattern matches on song titles,
# in future should probably be song index, since song titles
# can vary greatly across documentation
def mapTitlesToFiles(data, audiofiles):
    mapToFile = dict()

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