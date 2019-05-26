import os
import subprocess

import youtube_dl


def read_urls():
	_FILENAME = "url-to-download.txt"
	with open(_FILENAME, "r") as f:
		urls = f.readlines()
	return urls


if __name__ == "__main__":
	ydl_opts = {
		"format": "bestaudio/best",
		"postprocessors": [{
			"key": "FFmpegExtractAudio",
			"preferredcodec": "mp3",
			"preferredquality": "320"
		}]
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download(read_urls())
