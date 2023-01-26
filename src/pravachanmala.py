from pytube import YouTube
from pytube import Playlist
from concurrent.futures import ThreadPoolExecutor
import os
import re
import moviepy.editor as mp  # to convert the mp4 to wavv then mp3

class pravachans:
    def __init__(self, args):
        self.playlist = args.playlist
        self.savedir = args.save_dir
        self.jobs = args.jobs
        self.urls = []

    def start_download(self):
        # "https://youtube.com/playlist?list=PLcT36g1Z9qTevM_Xzqf6VX6KnTAt7QcIH"
        playlist = Playlist(self.playlist)

        for url in playlist:
            self.urls.append(url)

        if self.jobs > os.cpu_count() or self.jobs == -1:
                self.jobs = os.cpu_count()

        futures = []
        with ThreadPoolExecutor(self.jobs) as executor:
            futures = [executor.submit(self.start_task, url, self.urls.index(url)) for url in self.urls]

            for future in futures:
                future.add_done_callback(self.progress_indicator)

        print("")
        print ("--- starting converting the videos ---")
        print("")

        with ThreadPoolExecutor(self.jobs) as executor:
            futures = [executor.submit(self.start_converting, i) for i in os.listdir(self.savedir)]

            for future in futures:
                future.add_done_callback(self.progress_indicator)

    def start_converting(self, file):
        if re.search('mp4', file):
            print("Converting : " + file)
            mp4_path = os.path.join(self.savedir, file)
            mp3_path = os.path.join(self.savedir, os.path.splitext(file)[0]+'.mp3')
            new_file = mp.AudioFileClip(mp4_path)
            new_file.write_audiofile(mp3_path)
            os.remove(mp4_path)

    def start_task(self, url, count):
        print ("Downloading {} url = {} ".format(url, count))
        YouTube(url).streams.filter(
            only_audio=True).first().download(self.savedir, filename_prefix="{}-".format(count))

    def progress_indicator(self, future):
        print('.', end='', flush=True)
