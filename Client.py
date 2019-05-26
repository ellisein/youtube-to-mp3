import os
import sys
import ctypes
import subprocess
from ctypes import windll, wintypes
from uuid import UUID
from functools import partial

import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import youtube_dl

import Path


YDL_OPTS = {
	"format": "bestaudio/best",
	"outtmpl": os.path.join(Path.get_music_path(), "%(title)s"),
	"postprocessors": [{
		"key": "FFmpegExtractAudio",
		"preferredcodec": "mp3",
		"preferredquality": "320"
	}]
}


class Application(QMainWindow):
	TITLE = "Youtube to MP3"

	def __init__(self):
		super().__init__()
		self.initWindow()
		self.startFlow()

	def initWindow(self):
		self.setWindowTitle(self.TITLE)
		self.setStyleSheet(open("Style.qss", "r").read())
		self.resize(480, 360)
		geometry = self.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		geometry.moveCenter(center)
		self.move(geometry.topLeft())

	def startFlow(self):
		self.UI_Main()

	def UI_Main(self):
		self.url = ""
		widget = QWidget(self)

		label = QLabel("Youtube to MP3", widget)
		label.setAlignment(Qt.AlignHCenter)
		label.resize(240, 32)
		label.move(120, 60)

		lineEdit = QLineEdit(widget)
		lineEdit.resize(400, 32)
		lineEdit.move(40, 200)
		lineEdit.setPlaceholderText("유튜브 링크를 복사해주세요.")
		lineEdit.textChanged[str].connect(self.EVENT_ChangeUrl)

		btn_accept = QPushButton("확인", widget)
		btn_accept.resize(160, 36)
		btn_accept.move(160, 260)
		btn_accept.clicked.connect(self.EVENT_AcceptUrl)

		self.setCentralWidget(widget)
		self.show()

	def UI_Preview(self):
		widget = QWidget(self)

		label = QLabel("다운로드 중", widget)
		label.setAlignment(Qt.AlignHCenter)
		label.resize(240, 32)
		label.move(120, 80)

		progressbar = QProgressBar(widget)
		progressbar.resize(360, 24)
		progressbar.move(80, 260)
		progressbar.setRange(0, 0)

		self.setCentralWidget(widget)
		self.show()

	def UI_Fail(self):
		widget = QWidget(self)

		label = QLabel("다운로드에 실패했습니다.", widget)
		label.setAlignment(Qt.AlignHCenter)
		label.resize(240, 32)
		label.move(120, 60)

		btn_return = QPushButton("처음으로", widget)
		btn_return.resize(160, 36)
		btn_return.move(160, 260)
		btn_return.clicked.connect(self.EVENT_ReturnToMain)

		self.setCentralWidget(widget)
		self.show()

	def UI_Complete(self):
		widget = QWidget(self)

		label = QLabel("다운로드를 마쳤습니다.", widget)
		label.setAlignment(Qt.AlignHCenter)
		label.resize(240, 32)
		label.move(120, 60)

		btn_return = QPushButton("처음으로", widget)
		btn_return.resize(120, 36)
		btn_return.move(90, 260)
		btn_return.clicked.connect(self.EVENT_ReturnToMain)

		btn_open = QPushButton("폴더 열기", widget)
		btn_open.resize(120, 36)
		btn_open.move(270, 260)
		btn_open.clicked.connect(self.EVENT_OpenFolder)

		self.setCentralWidget(widget)
		self.show()

	def EVENT_ChangeUrl(self, url):
		self.url = url

	def EVENT_AcceptUrl(self):
		url = "url" if len(self.url) == 0 else self.url
		self.UI_Preview()
		self.thread_download = Thread_Download(url)
		self.thread_download.start()
		self.thread_download.progress.connect(self.EVENT_Progress)

	def EVENT_Progress(self, progress):
		print(progress)
		if progress == -1:
			self.UI_Fail()
		elif progress == 1:
			self.UI_Complete()

	def EVENT_ReturnToMain(self):
		self.UI_Main()

	def EVENT_OpenFolder(self):
		path = os.path.realpath(Path.get_music_path())
		subprocess.Popen('explorer "{}"'.format(path))


class Thread_Download(QThread):
	progress = pyqtSignal(int)

	def __init__(self, url):
		QThread.__init__(self)
		self.url = url

	def run(self):
		self.running = True

		try:
			print(self.url)
			with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
				ydl.download([self.url])
		except:
			self.progress.emit(-1)
			self.running = False

		if self.running:
			self.progress.emit(1)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = Application()
	sys.exit(app.exec_())
