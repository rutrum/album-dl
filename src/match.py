from fuzzywuzzy import fuzz
from fuzzywuzzy import process 


def mapTitlesToFiles(tracks, yt_titles):

    mapToFile = {}

    for track in tracks:

        # The scorer is a hack to let me add a processor to the yt_titles (choices)
        # since the processor only processes the query (which is trivial)
        selected_yt, how_well = process.extractOne(track.clean, yt_titles, 
            processor = None,
            scorer=lambda x,y: fuzz.WRatio(x, y.clean)
        )

        if how_well > 60:
            mapToFile[track] = selected_yt
        else:
            mapToFile[track] = "" 

    return mapToFile
