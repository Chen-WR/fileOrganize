import os
import sys
import shutil
from PyQt5.QtWidgets import QWidget, QFileDialog, QApplication, QDesktopWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class App(QWidget):
	def __init__(self):
		super().__init__()
		sys.setrecursionlimit(10**8)
		self.title = 'File Organizer'
		self.left = 0
		self.top = 0 
		self.width = 500
		self.height = 150
		self.destination = ''
		self.dirsList = []
		self.filesList = []

	def initUI(self):
		self.makeMain()
		self.makeButton()
		self.show()

	def makeMain(self):
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.setWindowTitle(self.title)
		self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		win = self.frameGeometry()
		center = QDesktopWidget().availableGeometry().center()
		win.moveCenter(center)
		self.move(win.topLeft())

	def makeButton(self):
		self.button1 = QPushButton("From Folder: ", self)
		self.button1.setGeometry(30, 20, 90, 30)
		self.button1.clicked.connect(self.getFromFolder)

		self.button2 = QPushButton("To Folder: ", self)
		self.button2.setGeometry(30, 60, 90, 30)
		self.button2.clicked.connect(self.getToFolder)

		self.button3 = QPushButton("Start", self)
		self.button3.setGeometry(200, 110, 90, 30)
		self.button3.clicked.connect(self.start)

		self.label1 = QLabel("Choose Origin Directory", self)
		self.label1.setGeometry(140, 20, 300, 20)
		self.label1.setWordWrap(True)

		self.label2 = QLabel("Choose Destination Directory", self)
		self.label2.setGeometry(140, 70, 300, 20)
		self.label2.setWordWrap(True)

	def getFromFolder(self):
		self.dialog1 = QFileDialog()
		self.dialog1.setFileMode(QFileDialog.Directory)
		if self.dialog1.exec_():
			self.dirsList.append(self.dialog1.selectedFiles()[0])
			self.label1.setText(self.dirsList[0])

	def getToFolder(self):
		self.dialog2 = QFileDialog()
		self.dialog2.setFileMode(QFileDialog.Directory)
		if self.dialog2.exec_():
			self.destination = self.dialog2.selectedFiles()[0]
			self.label2.setText(self.destination)

	def disableButton(self):
		self.button1.setEnabled(False)
		self.button2.setEnabled(False)
		self.button3.setEnabled(False)

	def enableButton(self):
		self.button1.setEnabled(True)
		self.button2.setEnabled(True)
		self.button3.setEnabled(True)
		self.label1.setText('Choose Origin Directory')

	def popWarning1(self):
		self.popup1 = QMessageBox()
		self.popup1.setWindowTitle("Warning")
		self.popup1.setText("Choose Origin Folder")
		# self.popup1.setWindowIcon(self.icon)
		self.popup1.exec_()

	def popWarning2(self):
		self.popup2 = QMessageBox()
		self.popup2.setWindowTitle("Warning")
		self.popup2.setText("Choose Destination Folder")
		# self.popup1.setWindowIcon(self.icon)
		self.popup2.exec_()


	def start(self):
		if not self.dirsList or not self.destination:
			if not self.dirsList:
				self.popWarning1()
			elif not self.destination:
				self.popWarning2()
		else:
			self.disableButton()
			path = self.dirsList[0]
			os.chdir(path)		
			self.dirsList.remove(path)	
			for temp in os.listdir(path):
				if os.path.isfile(temp):
					self.filesList.append(os.path.join(path, temp))
				if os.path.isdir(temp):
					self.dirsList.append(os.path.join(path, temp))
			if self.dirsList:
				self.start()
			else:
				for i in range(len(self.filesList)):
					try:
						shutil.move(self.filesList[i], self.destination)
					except shutil.Error:
						pass
				self.filesList = []
			self.enableButton()	

def main():
	app = QApplication(sys.argv)
	software = App()
	software.initUI()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()