#encoding: utf-8
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QSystemTrayIcon, \
	QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import QSize,pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from functools import partial
import threading, time
import main
from util import set_interval

class ExecThread(threading.Thread):
	def __init__(self,func):
		super().__init__()
		self.func = func

	def run(self):
		self.func()

class MainWindow(QDialog):
	"""
		 Сheckbox and system tray icons.
		 Will initialize in the constructor.
	"""
	scanPorts = pyqtSignal()
	startLoop = pyqtSignal()
	runningThread = None
	config = 'config.json'
	mainObject = None

	# Override the class constructor
	def __init__(self):
		# Be sure to call the super class method
		super().__init__()

		self.port = None
		self.baud = 9600
		self.mainObject = main.MainObject(self.config,self.port,\
		self.baud)

		# Init QSystemTrayIcon
		self.tray_icon = QSystemTrayIcon(self)
		self.tray_icon.setIcon(QIcon('icon.png'))

		quit_action = QAction("Exit", self)
		quit_action.triggered.connect(self.appQuit)

		tray_menu = QMenu()

		self.sub_menu_port = tray_menu.addMenu("Choose port")
		self.rescan = QAction('Rescan')
		self.rescan.triggered.connect(self.scanPorts.emit)
		# baud submenu
		sub_menu_baud = tray_menu.addMenu("Choose baud")
		l = [1200,2400,4800,9600,14400,19200,28800,38400,57600,115200]
		for i in l:
			action = sub_menu_baud.addAction(str(i))
			action.font().bold = False
			action.triggered.connect(partial(self.chooseBaud,i))
			action.checkable = True
			if i == self.baud:
				action.checked = True

		tray_menu.addAction(quit_action)

		self.tray_icon.setContextMenu(tray_menu)
		self.tray_icon.show()

		#set signal
		self.scanPorts.connect(self.addPortsToMenu)
		self.scanPorts.emit()
		self.startLoop.connect(self.runLoop)
		self.startLoop.emit()

	def runLoop(self):
		self.mainObject.configSerial(self.port, self.baud)
		if not self.mainObject.isRunning():
			self.thread = ExecThread(lambda: 	self.mainObject.exec_loop())
			self.thread.start()

	def configSerial(self):
		self.mainObject.configSerial(self.port, self.baud)

	def choosePort(self,action,port):
		self.port = port
		action.checked = True
		print("Chosen port is " + self.port)
		self.configSerial()

	def chooseBaud(self, baud):
		self.baud = baud
		print("Chosen baud is " + str(self.baud))
		self.configSerial()


	def addPortsToMenu(self):
		menu = self.sub_menu_port
		menu.clear()
		ports = self.mainObject.serial_ports()
		if self.port == None and len(ports) > 0:
			self.port = ports[0]
		for i in ports:
			action = menu.addAction(i)
			action.checkable = True
			action.triggered.connect(partial(self.choosePort,action,i))
		menu.addSeparator()
		menu.addAction(self.rescan)

	def appQuit(self):
		self.mainObject.running = False
		while self.thread.is_alive():
			print("Desligando thread")
			time.sleep(0.5)
		self.thread.join()
		print("Thread desligada")
		qApp.quit()


if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	mw = MainWindow()
	sys.exit(app.exec_())
