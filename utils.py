from urllib.request import urlopen
from dataclasses import dataclass
from typing import Union
from spotipy import util
import re

SCOPE = 'user-library-read'



@dataclass
class Song:
    '''
    Song class to store useful track information
    '''
    vidurl: str
    title: str
    artist: str
    album: str
    imgurl: str


@dataclass
class SpotifyClientManager:
    scope: str = SCOPE
    user_id: str = 'excelshad0wz'
    client_id: str = 'acb20e9671e443d9ba8939197764e1c8'
    client_secret: str = 'acab8e29efd0405789be22ad22373bae'
    redirect_uri: str = 'http://localhost:8888/callback'

    @property
    def get_token(self):
        '''
        Return the access token
        '''
        return util.prompt_for_user_token(
            self.user_id,
            scope=self.scope,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri
        )


def get_yt_url(song_name: str) -> Union[str, None]:
    '''Get youtube video url from  song name'''
    song_name = '+'.join(song_name.split()).encode('utf8') # Replacing whitespace with '+' symbol
    print(song_name)
    search_url = f"https://www.youtube.com/results?search_query={song_name}"
    html = urlopen(search_url).read().decode()
    video_ids = re.findall(r"watch\?v=(\S{11})", html)
    if video_ids:
        return f"https://www.youtube.com/watch?v={video_ids[0]}"
    
    return None