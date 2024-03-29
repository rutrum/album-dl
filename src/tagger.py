import os
import eyed3
import sys

def tag_songs(tracks, meta, mapping):

    total_tracks = len(tracks)
    new_names = []

    # sys.stdout = open(os.devnull, "w")

    for track in tracks:
        
        yt_video = mapping[track]
        if yt_video:
            path = "/tmp/album-dl/{}.mp3".format(yt_video.id)
            audiofile = eyed3.load(path)

            audiofile.tag.artist = meta["artist"]
            audiofile.tag.album = meta["album"]
            audiofile.tag.recording_date = eyed3.core.Date(int(meta["year"]))
            audiofile.tag.genre = meta["genre"]

            audiofile.tag.title = track.title
            audiofile.tag.track_num = (track.num, total_tracks)

            if os.path.exists("/tmp/album-dl/art.jpg"):
                audiofile.tag.images.set(3, open("/tmp/album-dl/art.jpg", "rb").read(), 'image/jpeg')

            clean_title = track.title.replace("/", "-")

            newname = "{:02d} {}".format(
                int(track.num), 
                clean_title
            )
            # audiofile.rename(newname)
            audiofile.tag.save()
            new_names.append({
                "old": yt_video.id,
                "new": newname
            })


    return new_names
    # sys.stdout = sys.__stdout__
