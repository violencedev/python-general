

from __future__ import unicode_literals
from threading import Thread
from turtle import title
from urllib import request
from PyQt5 import QtCore, QtGui, QtWidgets
from urllib.request import urlopen
from bs4 import BeautifulSoup
from random import randint
import youtube_dl
import re
import threading

class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
                self.mainThread = threading.Thread()
                self.mainThread.start()
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(505, 176)
                MainWindow.setFixedSize(505, 176)
                MainWindow.setStyleSheet("background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(194, 21, 0, 255), stop:1 rgb(255, 197, 0))")
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
                self.lineEdit.setGeometry(QtCore.QRect(30, 60, 421, 31))
                font = QtGui.QFont()
                font.setFamily("Segoe UI")
                self.lineEdit.setFont(font)
                self.lineEdit.setStyleSheet("QLineEdit {\n"
        "background: rgb(11, 79, 108);\n"
        "selection-background-color:  rgb(11, 79, 108);\n"
        "border-radius: 7px;\n"
        "color: whitesmoke;\n"
        ""
        "}\n"
        "\n"
        "QLineEdit:hover {\n"
        "    background:  rgb(24, 108, 101);\n"
        "\n"
        "}")
                self.lineEdit.setObjectName("lineEdit")
                self.frame = QtWidgets.QFrame(self.centralwidget)
                self.frame.setGeometry(QtCore.QRect(-10, -10, 521, 51))
                self.frame.setStyleSheet("text-align: center;")
                self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
                self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
                self.frame.setObjectName("frame")
                self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
                self.verticalLayout.setObjectName("verticalLayout")
                self.label = QtWidgets.QLabel(self.frame)
                font = QtGui.QFont()
                font.setFamily("Segoe UI")
                font.setPointSize(15)
                self.label.setFont(font)
                self.label.setStyleSheet("text-align: center;\n"
        "color: whitesmoke;")
                self.label.setAlignment(QtCore.Qt.AlignCenter)
                self.label.setObjectName("label")
                self.verticalLayout.addWidget(self.label)
                self.label_2 = QtWidgets.QLabel(self.centralwidget)
                self.label_2.setGeometry(QtCore.QRect(0, 30, 501, 16))
                font = QtGui.QFont()
                font.setFamily("Segoe UI")
                self.label_2.setFont(font)
                self.label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.label_2.setObjectName("label_2")
                self.pushButton = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton.setGeometry(QtCore.QRect(140, 130, 221, 31))
                font = QtGui.QFont()
                font.setFamily("Segoe UI")
                font.setPointSize(10)
                font.setBold(False)
                font.setWeight(50)
                self.pushButton.setFont(font)
                self.pushButton.setStyleSheet("border: solid 1px;\n"
        "background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0, stop:0 rgb(198, 255, 221), stop:1 rgb(251, 215, 134), stop: 2 rgb(247, 121, 125));\n"
        "border-radius: 4px;")
                self.pushButton.setObjectName("pushButton")
                self.label_3 = QtWidgets.QLabel(self.centralwidget)
                self.label_3.setGeometry(QtCore.QRect(-10, 100, 521, 20))
                font = QtGui.QFont()
                font.setFamily("Segoe UI")
                self.label_3.setFont(font)
                self.label_3.setAlignment(QtCore.Qt.AlignCenter)
                self.label_3.setObjectName("label_3")
                MainWindow.setCentralWidget(self.centralwidget)

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)
                self.mainThread.join()

        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
                #self.lineEdit.setText(_translate("MainWindow", "Youtube linki veya anahtar kelime giriniz."))
                self.lineEdit.setPlaceholderText(_translate("MainWindow", "Youtube linki veya anahtar kelimesi girin."))
                self.label.setText(_translate("MainWindow", "Youtube MP3 D??n????t??r??c??"))
                self.label_2.setText(_translate("MainWindow", "D??n????t??rmek istedi??iniz linki veya anahtar kelimeyi a??a????daki kutucu??a yaz??n??z."))
                self.pushButton.setText(_translate("MainWindow", "D??n????t??rmeye Ba??la!"))
                self.label_3.setText(_translate("MainWindow", "Bulunan Video : Hi??bir video bulunamad??."))
                self.thread = {}
                self.pushButton.clicked.connect(self.start_Worker)

        def start_Worker(self):
                if self.lineEdit.text().count(' ') == 0 and re.findall("youtube.com/watch?v=", self.lineEdit.text()) == True:
                        lineEdit_Text = self.lineEdit.text()
                        self.thread[1] = ThreadClass(parent=None, index=1, lineEdit=lineEdit_Text, label=self.label_3)
                        self.thread[1].start()
                        self.thread[1].any_signal.connect(self.my_function)
                        self.pushButton.setEnabled(False)
                else:
                        print('hi')
                        self.thread[1] = ThreadClass(parent=None, index=1, lineEdit=self.lineEdit.text(), label=self.label_3, formaturl=True)
                        self.thread[1].start()
                        self.thread[1].any_signal.connect(self.my_function)
                        self.pushButton.setEnabled(False)

        def stop_worker(self):
                self.thread[1].stop()
                

        def my_function(self, title):
                self.pushButton.setEnabled(True)
                currentText = self.label_3.text()
                currentBody = currentText.split('Downloanded - ')[0]
                _translate = QtCore.QCoreApplication.translate
                self.label_3.setText(_translate('MainWindow', f'Ba??ar??yla ??ndirildi : {currentBody}'))

class ThreadClass(QtCore.QThread):

        any_signal = QtCore.pyqtSignal(int)
        def __init__(self, parent, index, lineEdit, label, formaturl=False) -> None:
                super(ThreadClass, self).__init__(parent)
                self.is_Running = True 
                self.label_3 = label
                self.lineEdit = lineEdit
                self.formaturl = formaturl
        def run(self):
                print('Starting thread')
                try:
                        if self.formaturl == True:
                                myLine_temp = self.lineEdit.replace(' ', '+')
                                templateUrl = 'https://www.youtube.com/results?search_query='
                                newUrl = templateUrl + myLine_temp
                                html = urlopen(newUrl)
                                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                                self.lineEdit = 'https://www.youtube.com/watch?v=' + video_ids[0]
                        soup = BeautifulSoup(urlopen(self.lineEdit), 'html.parser')
                        baslik = soup.title.get_text()
                        _translate = QtCore.QCoreApplication.translate
                        self.label_3.setText(_translate('MainWindow', f'Bulunan Video : {baslik}'))
                        ydl_opts = {
                                'format':'bestaudio/best',
                                'keepvideo':False,
                                'outtmpl':f'Downloanded - {baslik}.mp3',}
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                ydl.download([self.lineEdit])
                except:
                        print('Unexpected Error Occured')
                self.any_signal.emit('control')
                
        def stop(self):
                print('Stopping thread')
                self.is_Running = False
                self.terminate()

if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
