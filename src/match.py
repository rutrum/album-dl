from fuzzywuzzy import fuzz
from fuzzywuzzy import process 


def mapTitlesToFiles(tracks, yt_titles):

    mapToFile = {}
    mapped_yt = []

    for track in tracks:

        # The scorer is a hack to let me add a processor to the yt_titles (choices)
        # since the processor only processes the query (which is trivial)
        # Finds a score for everything in list
        selected = process.extractWithoutOrder(track.clean, yt_titles, 
            processor = None,
            scorer=lambda x,y: fuzz.WRatio(x, y.clean)
        )
        selected = list(selected)

        # adjust score by difference in track numbers
        for j, selection in enumerate(selected):
            yt, score = selection
            selected[j] = yt, score + (10 - abs(int(track.num) - j))

        best, how_well = max(selected, key=lambda x: x[1])

        mapped_yt.append(best)

        if how_well > 50:
            mapToFile[track] = best
        else:
            mapToFile[track] = "" 


    unmapped_yt = [ title for title in yt_titles if title not in mapped_yt ]
    
    return mapToFile, unmapped_yt
