# album-dl

This script downloads an album and tags the songs from a wikipedia page.  The programs asks for a youtube playlist and a wikipedia link to the album.  It will download the music, scrape the wiki page for metadata, and then tag the songs.  It is _limited in its capabilities,_ but works for many cases nonetheless.

## Limitations of the Program
* Does not currently tag album art to songs
* Does not prompt for download location
* Only looks for the first track listing table on wikipedia.  Albums can be broken up by disc, or have different editions that do not align with playlist requested to download.  In these cases only half the songs can be tagged.
* Maps metadata to mp3 files by some pretty strict pattern matching.  This mapping is prompted to the user, but if the youtube video title has a different name than that in wikipedia, it might not be matched and therefore the mp3 file is never tagged.
* Does not prompt the user nearly enough about condition of the metadata

These limitations will be addressed as development continues.

## Requirements to Use
* python3
* [youtube-dl](https://github.com/ytdl-org/youtube-dl/blob/master/README.md) for downloading videos online
* [mutagen](https://mutagen.readthedocs.io/en/latest/) for tagging audio files
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/#Download) for scraping webpages