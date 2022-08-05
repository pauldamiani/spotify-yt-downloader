from mutagen.mp4 import MP4, MP4Cover
from urllib.request import urlopen
import requests
import re
import os
import json

import yt_dlp
from yt_dlp.postprocessor.common import PostProcessor

from utils import Song
from utils import get_yt_url

class MyLogger:
    def debug(self, msg):
        # For compatability with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

class MyCustomPP(PostProcessor):
    def run(self, info):
        self.to_screen('Doing stuff')
        return [], info

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

def download_song_from_yt(vid_url: str, song_name: str) -> None:
    '''Download song in the current directory and rename it'''
    try:
        # pafy.g.opener.addheaders.append(('Range', 'bytes=0-'))
        # vid = pafy.new(vid_url)
        # vid.getbestaudio(preftype='m4a')
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': song_name + ".webm",
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': '192',
            }],
            'logger': MyLogger(),
            'progress_hooks': [my_hook],
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.add_post_processor(MyCustomPP())
            info = ydl.download([vid_url])
            print(json.dumps(ydl.sanitize_info(info)))
    except Exception as e:
        return None

def addtags(songpath: str, song: Song) -> None:
    TITLE = "\xa9nam"
    ALBUM = "\xa9alb"
    ARTIST = "\xa9ART"
    ART = "covr"
    f = MP4(songpath)
    f[TITLE] = song.title
    f[ALBUM] = song.album
    f[ARTIST] = song.artist
    res = requests.get(song.imgurl)
    f[ART] = [MP4Cover(res.content, MP4Cover.FORMAT_JPEG)]
    f.save()

def download(song: Song) -> None:
    INVALID = r"[#<%>&\*\{\?\}/\\$+!`'\|\"=@\.\[\]:]*"
    song_name = re.sub(INVALID, "", f'{song.artist} {song.title}') # Remove invalid chars
    print(f"Downloading {song_name}")
    try:
        if song.vidurl is None:
            song.vidurl = get_yt_url(song_name)
        song_path = f"{song_name}.m4a"
        download_song_from_yt(song.vidurl, song_name)
        addtags(f"{song_name}.m4a", song)
    except Exception as e:
        if os.path.exists(song_path):
            os.remove(song_path)
        
        print(f"Error downloading {song_name}: {e}")