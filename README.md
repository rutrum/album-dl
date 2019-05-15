# album-dl

This script downloads an album and tags the songs from a wikipedia page.  The programs asks for a youtube playlist and a wikipedia link to the album.  It will download the music, scrape the wiki page for metadata, and then tag the songs.  It is _limited in its capabilities,_ but works for many cases nonetheless.

## Limitations of the Program
* Does not currently tag album art to songs
* Does not prompt for download location
* Only looks for the first track listing table on wikipedia.  Albums can be broken up by disc, or have different editions that do not align with playlist requested to download.  In these cases only half the songs can be tagged.
* Does not prompt the user nearly enough about condition of the metadata

These limitations will be addressed as development continues.

## Tags

Currently this program adds the following metadata to every mp3 file:
* Artist
* Album
* Track title
* Track number
* Total tracks on album
* Genre
* Year of release
* Album Art (when found)

## Requirements to Use
* python3
* [youtube-dl](https://github.com/ytdl-org/youtube-dl/blob/master/README.md) for downloading videos online
* [mutagen](https://mutagen.readthedocs.io/en/latest/) for tagging audio files
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/#Download) for scraping webpages