#!/usr/bin/python2.7

import sys
import logging
from PyQt4 import QtGui, QtCore
import random
import urllib
import cv2
import numpy as np
import socket

HOST = '192.168.0.33'    # Symbolic name meaning all available interfaces
PORT = 8810              # Arbitrary non-privileged port

logging.basicConfig(level=logging.DEBUG,
                    format='[%(threadName)s] %(message)s',
) 

class Thread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent=parent)

    def run(self):
        stream = urllib.urlopen('http://192.168.0.33:8080/?action=stream')
        bytes=''
        while True:
            bytes+=stream.read(1024)
            a = bytes.find('\xff\xd8')
            b = bytes.find('\xff\xd9')
            if a!=-1 and b!=-1:
                jpg = bytes[a:b+2]
                bytes= bytes[b+2:]
                rgbImage = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
                rgbImage = cv2.cvtColor(rgbImage,cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QtGui.QImage.Format_RGB888)
                self.changePixmap.emit(convertToQtFormat)
                                                                                                                            
                
class Gui(QtGui.QMainWindow):
    
    def __init__(self,app,soc):
        super(Gui, self).__init__()        
        self.app = app
        self.soc = soc
        self.wid = None
        self.initWindow()
        self.initMenu()        
        self.initPage()                
        self.runWindow()
        
    def initWindow(self):        
        logging.debug("initializing window") 

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.wid = QtGui.QWidget(self)
        self.setCentralWidget(self.wid)
        
    def initMenu(self):
        logging.debug("initializing Menu/Tool/Status Bars") 

        exitAction = QtGui.QAction('&Exit', self)
        exitAction.triggered.connect(self.close)                        

        helpAction = QtGui.QAction("&Help", self)
        helpAction.triggered.connect(self.helpMessage)        
        
        menubar = self.menuBar()
        f_menu = menubar.addMenu('&File')
        f_menu.addAction(exitAction)        
        f_menu.addAction(helpAction)        
        
    def setScreen(self):
        desk_h = self.app.desktop().screenGeometry().height()
        desk_w = self.app.desktop().screenGeometry().width()
        self.resize((desk_w/2), (desk_h/2))
        win_h = self.frameGeometry().height()
        win_w = self.frameGeometry().width()        
        self.move((desk_w/4), (desk_h/4))
        logging.debug("res is " + str(desk_w) + 'x' + str(desk_h) + 
                      "frame is " + str(win_w) + 'x' + str(win_h))
        

    def runWindow(self):
        self.setScreen()
        self.setWindowTitle('Tool')
        self.setWindowIcon(QtGui.QIcon('tool.png'))
        self.show()

    def initPage(self):        
        logging.debug("setting Page") 

        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(self.close)        

        btn1 = QtGui.QPushButton('UP', self)
        btn1.clicked.connect(self.control("UP"))        

        btn2 = QtGui.QPushButton('DOWN', self)
        btn2.clicked.connect(self.control("DOWN"))        
        
        self.label = QtGui.QLabel(self)
        self.label.resize(640,480)
        th = Thread(self)
        th.changePixmap.connect(lambda p: self.setPmap(p))
        th.start()
        
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)        
        hbox.addWidget(qbtn)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.label)        
        vbox.addLayout(hbox)
        
        self.wid.setLayout(vbox)
                        
    def setPmap(self, p):
        p = QtGui.QPixmap.fromImage(p)
        p = p.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(p)
        
    def helpMessage(self):        
        help_msg = QtGui.QMessageBox.question(self, 'Select a valid file',
                                              'Please select an xlsx file by clicking on the excel icon ' \
                                              'on the top left and then start mapping', QtGui.QMessageBox.Ok)

    def control(self,msg):         
        logging.debug('sending ' + msg) 
        return lambda : self.soc.sendall(msg)

        
def main():

    #setup socket
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    except :
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    #Connect to remote server
    soc.connect((HOST , PORT))
    logging.info('Socket Connected to ' + HOST) 

    app = QtGui.QApplication(sys.argv)
    ex = Gui(app,soc)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
