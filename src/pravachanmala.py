from pytube import YouTube
from pytube import Playlist
from concurrent.futures import ThreadPoolExecutor
import os

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

    def start_task(self, url, count):
        print ("Downloading {} url = {} ".format(url, count))
        YouTube(url).streams.filter(
            only_audio=True).first().download(self.savedir, filename_prefix="{}-".format(count))

    def progress_indicator(self, future):
        print('.', end='', flush=True)
