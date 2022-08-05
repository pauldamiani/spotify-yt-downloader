# spotify-yt-downloader

Spotify/YouTube Downloader and Converter

Forked from an old repo and updated... forget where it's from...

## Setup

TODO

## Dependencies

To install all modules run `pip install -r requirements.txt`

## Usage

`python main.py`

## How it works

```
* Program Gets the deatils of the songs from spotify api (for spotify songs)  
  and youtube music api (for youtube songs)  
* It then searches the song on youtube and extracts the youtube song url
* The song is then downloaded as m4a from youtube using yt_dlp module
* Metadata are added to the m4a song (Artist, title, album, album art image)
```
