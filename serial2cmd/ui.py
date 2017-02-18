#!/usr/bin/env python3
#encoding: utf-8
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, \
	QMenu, QAction, QStyle, qApp
from PyQt5.QtCore import QSize,pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from functools import partial
import threading, time, json, os
import shutil
from serial2cmd.main_object import MainObject
from serial2cmd.editor_dialog import EditorDialog
from serial2cmd.config import *


class ExecThread(threading.Thread):
	def __init__(self,func):
            super().__init__()
            self.func = func

	def run(self):
            self.func()

class TrayMenu(QSystemTrayIcon):

    scanPorts = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setIcon(QIcon(TRAY_ICON_FILE))
    
    def setMenu(self, mainWindow):

        # Init QSystemTrayIcon
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(mainWindow.appQuit)

        tray_menu = QMenu()
        tray_menu.addAction("Monitor...").setEnabled(False)

        self.sub_menu_port = tray_menu.addMenu("Choose port")
        self.rescan = QAction('Rescan')
        self.rescan.triggered.connect(self.scanPorts.emit)

        edit_bindings = tray_menu.addAction("Edit Bindings...")
        edit_bindings.triggered.connect(mainWindow.editorWindow.show)

        # baud submenu
        sub_menu_baud = tray_menu.addMenu("Choose baud")
        l = [1200,2400,4800,9600,14400,19200,28800,38400,57600,115200]
        for i in l:
                action = sub_menu_baud.addAction(str(i))
                action.font().bold = False
                action.triggered.connect(partial(mainWindow.chooseBaud,i))
                action.checkable = True
                if i == mainWindow.baud:
                        action.checked = True

        tray_menu.addAction(quit_action)

        self.setContextMenu(tray_menu)
        self.show()
        self.scanPorts.connect(lambda: self.addPortsToMenu(mainWindow))
        self.scanPorts.emit()
    

    def addPortsToMenu(self, mainWindow):
            menu = self.sub_menu_port
            menu.clear()
            ports = mainWindow.mainObject.serial_ports()
            if mainWindow.port == None and len(ports) > 0:
                    mainWindow.port = ports[0]
            for i in ports:
                    action = menu.addAction(i)
                    action.checkable = True
                    action.triggered.connect(partial(mainWindow.choosePort,action,i))
            menu.addSeparator()
            menu.addAction(self.rescan)

    

class MainWindow(QMainWindow):
	"""
		TODO
	"""
	startLoop = pyqtSignal()
	runningThread = None
	config = CONFIG_FILE
	mainObject = None
	editorWindow = None

	# Override the class constructor
	def __init__(self):
            super().__init__()
# Be sure to call the super class method
            self.checkIfConfigFileExists()

            self.port = None
            self.baud = 9600
            self.mainObject = MainObject(self.config,self.port,\
            self.baud)

            self.editorWindow = EditorDialog(self.mainObject, okFunc=self.saveJsonConfigFile)

            self.trayMenu = TrayMenu()
            self.trayMenu.setMenu(self)


#set signal
            self.startLoop.connect(self.runLoop)
            self.startLoop.emit()
            


	def saveJsonConfigFile(self, map):
		if not os.path.exists(CONFIG_DIR):
			os.makedirs(CONFIG_DIR)
			print('Diretório criado em ',CONFIG_DIR)
		f = open(CONFIG_FILE,'w')
		f.write(json.dumps(map, indent=4))
		f.close()
		print('Arquivo de configuração gravado')



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



	def appQuit(self):
		self.mainObject.running = False
		while self.thread.is_alive():
			print("Desligando thread")
			time.sleep(0.5)
		self.thread.join()
		print("Thread desligada")
		qApp.quit()

	def checkIfConfigFileExists(self):
		if not os.path.isdir(CONFIG_DIR):
			os.mkdir(CONFIG_DIR)
			shutil.copy2(DEFAULT_CONFIG_FILE,CONFIG_FILE)
		else:
			if not os.path.exists(CONFIG_FILE):
				file = open(CONFIG_FILE,'w')
				file.write('{}')
				file.close()


def main():
	import sys
	app = QApplication(sys.argv)
	mw = MainWindow()
	QApplication.setQuitOnLastWindowClosed(False)
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
