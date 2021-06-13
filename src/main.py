#!/usr/bin/env python3

# Something to improve: caching for when this certainly fails
# Just write progress to a file in tmp and initialize from it
# if the file exists

from models import YTVideo
from models import WikiTrack, Metadata

import scrapewiki as wiki
import ytdl
import match
import tagger as tag
import shutil

import progressbar

import youtube_dl
import os
from termcolor import cprint
import sys
from multiprocessing.pool import ThreadPool

def main():

    if len(sys.argv) < 3:
        print("usage: album-dl yt_url wiki_url")
        exit()

    pool = ThreadPool(processes=1)
    if not os.path.exists("/tmp/album-dl"):
        os.makedirs("/tmp/album-dl")

    yt_url = sys.argv[1]
    #yt_url = input("Enter youtube url:\n")
    # yt_url = "https://www.youtube.com/watch?v=DHd51Y7dhW0&list=PLONR6CCwpAARTIZ69LUgLW1cdEyM4Rn5e"
    song_downloader = pool.apply_async(ytdl.song_titles, (yt_url, )) 
    print("Downloading youtube playlist metadata...")

    wiki_url = sys.argv[2]
    # wiki_url = input("Enter wikipedia url:\n")
    # wiki_url = "https://en.wikipedia.org/wiki/When_Dream_and_Day_Unite"

    try:
        wiki_page = wiki.capture_page(wiki_url)

        metadata = wiki.get_metadata(wiki_page)

        wiki.download_art(wiki_page)

        track_tables = wiki.get_track_tables(wiki_page)

        table_indicies, track_renumber = select_tables(track_tables)
        tracks = wiki.get_tracks(track_tables, track_renumber, table_indicies)

        print()
        print(metadata)
        for track in tracks:
            print(track)

        while not confirm():
            print("What do you want to change?")
            print("[artist|album|year|genre|track ##]")
            k = input(": ").lower()
            if k in Metadata.keys():
                newval = input("New value for {}: ".format(k))
                metadata[k] = newval
            elif k and k.split()[0] == "track":
                num = k.split()[1]
                for track in tracks:
                    if num == track.num:
                        newval = input("New title for track {}: ".format(track.num))
                        track.title = newval
            else:
                print("Not a valid field.")

            print()
            print(metadata)
            for track in tracks:
                print(track)


        print("Downloading youtube playlist metadata...")
        last_msg = ""
        current, total = ytdl.msg_status
        while not song_downloader.ready():
            if ytdl.msg_status != last_msg:
                current, total = ytdl.msg_status

        yt_song_titles = song_downloader.get()  

        mapping, unmatched = match.mapTitlesToFiles(tracks, yt_song_titles) 

        print_mapping(mapping, unmatched)
            
        while not confirm():
            if unmatched:
                song = unmatched.pop(0)
                print()
                for track in mapping:
                    print(track)
                print("What does {} match with?".format(song.title))
                i = input("> ")
                success = False
                for track in mapping:
                    if track.num == i:
                        mapping[track] = song
                        print_mapping(mapping, unmatched)
                        success = True
                        break

                if not success:
                    print("Not a valid track number")
                    print_mapping(mapping, unmatched)

        ytdl.download_songs(yt_url)

        new_names = tag.tag_songs(tracks, metadata, mapping)

        path = "/home/rutrum/music/{}/{}".format(metadata["artist"], metadata["album"])
        os.makedirs(path, exist_ok=True)
        
        for name in new_names:
            old_path = "/tmp/album-dl/{}.mp3".format(name["old"])
            new_path = "{}/{}.mp3".format(path, name["new"])
            shutil.move(old_path, new_path) # can move across file systems
            #os.rename(old_path, new_path)  # cannot
        
        
    except Exception as ex:
        cprint(ex.args[0], "red", attrs=["bold"], file=sys.stderr)
        raise ex

def confirm():
    response = input("\nIs this correct? [Y/n] ")
    if response not in "Yy":
        return False
    else:
        return True

def select_tables(tables):
    if len(tables) > 1:
        print("Please enter which track tables you would like to use.")
        print("Please use space as delimeter, for example: 1 2")
        print("To append tracks to end, add * before number: 1 *2")
        print("By default, all tables will be used, in order.")

        for (i, table) in enumerate(tables):
            print("***{:^14}***".format(i))
            for track in table:
                print("{:>3}. ".format(track.num), track.title)

        res = input("Track tables: ")
        
        selected_tracks = []
        renumber = []

        for v in res.split():
            if v[0] == "*":
                renumber += [True]
                selected_tracks += [int(v[1:])]
            else:
                renumber += [False]
                selected_tracks += [int(v)]

        if len(selected_tracks) == 0:
            l = len(tables)
            renumber = [ False for i in range(l) ]
            selected_tracks = list(range(l))
            return selected_tracks, renumber

        for selection in selected_tracks:
            if selection > len(tables) or selection < 0:
                cprint("Please select valid tables.", "red")
                return select_tables(tables)
        
        return selected_tracks, renumber

    else:
        # Only found 1 table, return this
        return [False], [0]

def print_mapping(mapping, unmatched):
    print()
    cprint("{:>30}   {}".format("Song Title", "Video Title"), attrs=['bold'])
    for (key, val) in mapping.items():
        # Doesn't lookup when empty (string)
        # TODO
        if val:
            print("{:>30}   {}".format(key.title, val.title))
        else:
            print("{:>30}   {}".format(key.title, val))

    if unmatched:
        print()
        print("Unmatched songs:")
        for track in unmatched:
            print(track.title)

if __name__ == "__main__":
    main()
