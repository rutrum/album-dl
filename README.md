# album-dl

This script downloads an album from youtube and tags the songs from a wikipedia page.  The programs asks for a youtube playlist and a wikipedia link to the album.  It will download the music, scrape the wiki page for metadata, and then tag the songs.  There are edge cases where scraping and matching tags doesn't provide the correct results, but it works for a majority of cases regardless.

## Limitations

The program is automated to work on my machine.  It doesn't prompt the user or read a configuration file for things like where to store the music after tagging.  In addition, when something fails, there is no opportunity to manually make changes.  Either everything gets tagged by the algorithm or the user can abort the program.  If you plan on trying out the application, be aware.

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

## Future features

* Better loading bars
* Configuration file/prompt for download location
* Even better metadata to video matching
