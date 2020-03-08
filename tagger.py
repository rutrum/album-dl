import os
import eyed3
import sys

def tag_songs(tracks, meta, mapping):

    total_tracks = len(tracks)
    new_names = []

    # sys.stdout = open(os.devnull, "w")

    for track in tracks:
        
        filename = mapping[track["title"]]["filename"]
        if filename:
            path = "/tmp/album-dl/{}.mp3".format(filename)
            audiofile = eyed3.load(path)

            audiofile.tag.artist = meta["artist"]
            audiofile.tag.album = meta["album"]
            audiofile.tag.recording_date = eyed3.core.Date(int(meta["year"]))
            audiofile.tag.genre = meta["genre"]

            audiofile.tag.title = track["title"]
            audiofile.tag.track_num = (track["num"], total_tracks)

            if os.path.exists("/tmp/album-dl/art.jpg"):
                audiofile.tag.images.set(3, open("/tmp/album-dl/art.jpg", "rb").read(), 'image/jpeg')

            newname = "{:02d} {}".format(
                int(track["num"]), 
                track["title"]
            )
            # audiofile.rename(newname)
            audiofile.tag.save()
            new_names.append({
                "old": filename,
                "new": newname,
                "title": track["title"]
            })


    return new_names
    # sys.stdout = sys.__stdout__
