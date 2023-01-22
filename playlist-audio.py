from pytube import YouTube
from pytube import Playlist
import os
import moviepy.editor as mp  # to convert the mp4 to wavv then mp3
import re
username = os.getlogin()
playlist = Playlist(
    "https://www.youtube.com/playlist?list=PLcT36g1Z9qTcB8Hiv6pShGWlxjwDi83GW")
playlist.video_urls
for url in playlist:
    print(url)
for vid in playlist.videos:
    print(vid)
for url in playlist:
    YouTube(url).streams.filter(
        only_audio=True).first().download("./converted/")
folder = "./converted/"
for file in os.listdir(folder):
    if re.search('mp4', file):
        print("Converting : " + file)
        mp4_path = os.path.join(folder, file)
        mp3_path = os.path.join(folder, os.path.splitext(file)[0]+'.mp3')
        new_file = mp.AudioFileClip(mp4_path)
        new_file.write_audiofile(mp3_path)
        os.remove(mp4_path)
