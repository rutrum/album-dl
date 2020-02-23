from youtube_dl import YoutubeDL

msg_status = ""

class QuietLogger(object):
    def debug(self, msg):
        global msg_status
        if "[download] Downloading video" in msg:
            msg_status = msg[11:]

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class JustPrintDownload(object):
    def debug(self, msg):
        global msg_status
        if "[download] Downloading video" in msg:
            print(msg[11:])

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def song_titles(url):
    ydl_opts = { 'logger': QuietLogger() }

    with YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
        entries = meta["entries"]

        return list(map(lambda x: { "title": x["title"]}, entries))

def download_songs(url):
    ydl_opts = { 
        'logger': JustPrintDownload(),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'format': 'bestaudio/best',
        # 'outtmpl': '%(title)s.%(ext)s'
        'outtmpl': '/tmp/album-dl/%(title)s.%(ext)s'
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    download_songs("https://www.youtube.com/watch?v=GtUxPg9jRLM")
