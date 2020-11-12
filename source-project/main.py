import sys
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from gtts import gTTS
import os
mainAppWidget: QApplication = QApplication(sys.argv)
class MainWindow(QMainWindow):
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(460, 191)
        self.setWindowIcon(QIcon('icon.ico'))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.mainTextField = QtWidgets.QTextEdit(self.centralwidget)
        self.mainTextField.setGeometry(QtCore.QRect(10, 10, 341, 171))
        self.mainTextField.setObjectName("mainTextField")
        self.speakButton = QtWidgets.QPushButton(self.centralwidget)
        self.speakButton.setGeometry(QtCore.QRect(360, 10, 93, 28))
        self.speakButton.setObjectName("speakButton")
        self.mp3SaveButton = QtWidgets.QPushButton(self.centralwidget)
        self.mp3SaveButton.setGeometry(QtCore.QRect(360, 40, 93, 28))
        self.mp3SaveButton.setObjectName("mp3SaveButton")
        self.slowSpeechCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.slowSpeechCheck.setGeometry(QtCore.QRect(360, 160, 101, 20))
        self.slowSpeechCheck.setObjectName("slowSpeechCheck")
        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setGeometry(QtCore.QRect(360, 70, 93, 28))
        self.resetButton.setObjectName("resetButton")
        self.aboutButton = QtWidgets.QPushButton(self.centralwidget)
        self.aboutButton.setGeometry(QtCore.QRect(360, 100, 93, 28))
        self.aboutButton.setObjectName("aboutButton")
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        self.quitButton.setGeometry(QtCore.QRect(360, 130, 93, 28))
        self.quitButton.setObjectName("quitButton")
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Vaulatile Text to Speech"))
        self.mainTextField.setPlaceholderText(_translate("MainWindow", "Enter text you wish to be spoken here"))
        self.speakButton.setText(_translate("MainWindow", "Speak"))
        self.mp3SaveButton.setText(_translate("MainWindow", "Save to mp3"))
        self.slowSpeechCheck.setText(_translate("MainWindow", "Slow Speech"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.aboutButton.setText(_translate("MainWindow", "About"))
        self.quitButton.setText(_translate("MainWindow", "Quit"))

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()
        self.closeEvent(self.beforeClosing)
        self.mainTextField: QTextEdit = self.findChild(QTextEdit, "mainTextField")
        self.slowSpeechCheck = self.findChild(QCheckBox, "slowSpeechCheck")
        self.tmpFolder: str = 'C:/VaulTTStmp'
        self.tmpFilePath: str = self.tmpFolder + '/tmpSpeak.mp3'
        speakButton: QPushButton = self.findChild(QPushButton, "speakButton")
        speakButton.setMouseTracking(True)
        speakButton.clicked.connect(self.speakButtonClick)
        mp3SaveButton: QPushButton=self.findChild(QPushButton,"mp3SaveButton")
        mp3SaveButton.setMouseTracking(True)
        mp3SaveButton.clicked.connect(self.saveMp3ButtonClick)
        quitButton: QPushButton=self.findChild(QPushButton,"quitButton")
        quitButton.setMouseTracking(True)
        quitButton.clicked.connect(self.quitButtonClick)
        resetButton: QPushButton=self.findChild(QPushButton,"resetButton")
        resetButton.setMouseTracking(True)
        resetButton.clicked.connect(self.resetButtonClick)
        aboutButton: QPushButton=self.findChild(QPushButton,"aboutButton")
        aboutButton.setMouseTracking(True)
        aboutButton.clicked.connect(self.aboutDisplay)

    def speakButtonClick(self):
        speakableGTTSObj: gTTS = gTTS(text=self.mainTextField.toPlainText(), lang='en',
                                        slow=self.slowSpeechCheck.isChecked())
        if not os.path.exists(self.tmpFolder):
            os.mkdir(path=self.tmpFolder)
        if os.path.exists(self.tmpFilePath):
            os.remove(self.tmpFilePath)
        speakableGTTSObj.save(savefile=self.tmpFilePath)

    def aboutDisplay(self):
        aboutMsg: QMessageBox = QMessageBox()
        aboutMsg.setIcon(QMessageBox.Information)
        aboutMsg.setText('Creator: HyperFluxx\n'
                         'Version: Prototype\n'
                         'Tools Used:-\n'
                         'UI: PyQt5\n'
                         'TTS: gTTS\n'
                         'Audio: PyAudio')
        aboutMsg.setWindowTitle('About')
        aboutMsg.setWindowIcon(QIcon('icon.ico'))
        aboutMsg.setStandardButtons(QMessageBox.Ok)
        aboutMsg.exec_()

    def saveMp3ButtonClick(self):
        fileDialog: QFileDialog=QFileDialog()
        fileDialog.setWindowIcon(QIcon('icon.ico'))
        saveFilePath: str=fileDialog.getSaveFileName(parent=self, caption='Save mp3 file',
                                                           filter='mp3 files (*.mp3)')[0]
        gTTS(text=self.mainTextField.toPlainText(),lang='en',slow=self.slowSpeechCheck.isChecked()).save(saveFilePath)

    def quitButtonClick(self):
        #self.beforeClosing()
        self.close()

    def resetButtonClick(self):
        self.mainTextField.setText('')

    def beforeClosing(self):
        if os.path.exists('C:/VaulTTStmp'):
            if os.path.exists('C:/VaulTTStmp/tmpSpeak.mp3'):
                os.remove('C:/VaulTTStmp/tmpSpeak.mp3')
            os.rmdir('C:/VaulTTStmp')

    def closeEvent(self,event):
        self.beforeClosing()


if __name__ == "__main__":
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(mainAppWidget.exec_())
