#!/bin/bash

echo "Please enter youtube playlist url: "
read PLAYLISTURL
echo "Please enter wikipedia album url: "
read WIKIURL

echo ""
echo -e "Playlist:\t"$PLAYLISTURL
echo -e "Wiki:    \t"$WIKIURL

echo -n "Are you sure about this configuration? [Y/n] "
read CONFIRM
if [ -n $CONFIRM ] && [ "n" = "$CONFIRM" ]; then
    echo "Aborting download."
    exit
fi

echo "Downloading videos now."
youtube-dl --config-location $HOME/album-web-scraper/youtube-dl.conf $PLAYLISTURL

