from PyQt5 import QtCore, QtGui, QtWidgets
from socket import *
import select
import datetime
import time

# 주소와 포트 지정
"""IP = ''
PORT = 5376
ADDRESS = (IP,PORT)
"""
#Gui 클래스
class MyGui(object):
    def __init__(self, ChatProgram):
        ChatProgram.setObjectName("ChatProgram")
        ChatProgram.resize(1054, 1112)
        self.centralwidget = QtWidgets.QWidget(ChatProgram)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1031, 1061))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.Server_Tab = QtWidgets.QWidget()
        self.Server_Tab.setObjectName("Server_Tab")
        self.Start_Button = QtWidgets.QToolButton(self.Server_Tab)
        self.Start_Button.setGeometry(QtCore.QRect(550, 10, 221, 31))
        self.Start_Button.setObjectName("Start_Button")
        self.Stop_Button = QtWidgets.QToolButton(self.Server_Tab)
        self.Stop_Button.setGeometry(QtCore.QRect(550, 50, 221, 31))
        self.Stop_Button.setObjectName("Stop_Button")
        self.IP_ComboBox = QtWidgets.QComboBox(self.Server_Tab)
        self.IP_ComboBox.setGeometry(QtCore.QRect(110, 10, 431, 31))
        self.IP_ComboBox.setObjectName("IP_ComboBox")
        self.IP_Label = QtWidgets.QLabel(self.Server_Tab)
        self.IP_Label.setGeometry(QtCore.QRect(40, 10, 32, 31))
        font = QtGui.QFont()
        font.setFamily("HY나무B")
        font.setPointSize(18)
        self.IP_Label.setFont(font)
        self.IP_Label.setObjectName("IP_Label")
        self.PORT_ComboBox = QtWidgets.QComboBox(self.Server_Tab)
        self.PORT_ComboBox.setGeometry(QtCore.QRect(110, 50, 431, 31))
        self.PORT_ComboBox.setObjectName("PORT_ComboBox")
        self.Message_Browser = QtWidgets.QTextBrowser(self.Server_Tab)
        self.Message_Browser.setGeometry(QtCore.QRect(20, 130, 751, 781))
        self.Message_Browser.setObjectName("Message_Browser")
        self.Broadcase_Edit = QtWidgets.QTextEdit(self.Server_Tab)
        self.Broadcase_Edit.setGeometry(QtCore.QRect(20, 920, 751, 81))
        self.Broadcase_Edit.setObjectName("Broadcase_Edit")
        self.PORT_Label = QtWidgets.QLabel(self.Server_Tab)
        self.PORT_Label.setGeometry(QtCore.QRect(20, 50, 81, 36))
        font = QtGui.QFont()
        font.setFamily("HY나무B")
        font.setPointSize(18)
        self.PORT_Label.setFont(font)
        self.PORT_Label.setObjectName("PORT_Label")
        self.LOGO_Label = QtWidgets.QLabel(self.Server_Tab)
        self.LOGO_Label.setGeometry(QtCore.QRect(350, 97, 111, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.LOGO_Label.setFont(font)
        self.LOGO_Label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.LOGO_Label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LOGO_Label.setObjectName("LOGO_Label")
        self.Time_Browser = QtWidgets.QTextBrowser(self.Server_Tab)
        self.Time_Browser.setGeometry(QtCore.QRect(790, 10, 221, 71))
        self.Time_Browser.setObjectName("Time_Browser")
        self.LOGO_Label_2 = QtWidgets.QLabel(self.Server_Tab)
        self.LOGO_Label_2.setGeometry(QtCore.QRect(880, 100, 48, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.LOGO_Label_2.setFont(font)
        self.LOGO_Label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.LOGO_Label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.LOGO_Label_2.setObjectName("LOGO_Label_2")
        self.UserList_Browser = QtWidgets.QTextBrowser(self.Server_Tab)
        self.UserList_Browser.setGeometry(QtCore.QRect(790, 130, 221, 781))
        self.UserList_Browser.setObjectName("UserList_Browser")
        self.Trans_Button = QtWidgets.QToolButton(self.Server_Tab)
        self.Trans_Button.setGeometry(QtCore.QRect(790, 920, 221, 81))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Trans_Button.setFont(font)
        self.Trans_Button.setObjectName("Trans_Button")
        self.tabWidget.addTab(self.Server_Tab, "")
        self.Client_Tab = QtWidgets.QWidget()
        self.Client_Tab.setObjectName("Client_Tab")
        self.Cli_Message_Browser = QtWidgets.QTextBrowser(self.Client_Tab)
        self.Cli_Message_Browser.setGeometry(QtCore.QRect(20, 130, 751, 781))
        self.Cli_Message_Browser.setObjectName("Cli_Message_Browser")
        self.Entere_Button = QtWidgets.QToolButton(self.Client_Tab)
        self.Entere_Button.setGeometry(QtCore.QRect(550, 10, 221, 31))
        self.Entere_Button.setObjectName("Entere_Button")
        self.Cli_PORT_ComboBox = QtWidgets.QComboBox(self.Client_Tab)
        self.Cli_PORT_ComboBox.setGeometry(QtCore.QRect(110, 50, 431, 31))
        self.Cli_PORT_ComboBox.setObjectName("Cli_PORT_ComboBox")
        self.Cli_UserList_Browser = QtWidgets.QTextBrowser(self.Client_Tab)
        self.Cli_UserList_Browser.setGeometry(QtCore.QRect(790, 130, 221, 781))
        self.Cli_UserList_Browser.setObjectName("Cli_UserList_Browser")
        self.Cli_Chat_Edit = QtWidgets.QTextEdit(self.Client_Tab)
        self.Cli_Chat_Edit.setGeometry(QtCore.QRect(20, 920, 751, 81))
        self.Cli_Chat_Edit.setObjectName("Cli_Chat_Edit")
        self.Cli_IP_Label = QtWidgets.QLabel(self.Client_Tab)
        self.Cli_IP_Label.setGeometry(QtCore.QRect(40, 10, 32, 36))
        font = QtGui.QFont()
        font.setFamily("HY나무B")
        font.setPointSize(18)
        self.Cli_IP_Label.setFont(font)
        self.Cli_IP_Label.setObjectName("Cli_IP_Label")
        self.Cli_Time_Browser = QtWidgets.QTextBrowser(self.Client_Tab)
        self.Cli_Time_Browser.setGeometry(QtCore.QRect(790, 10, 221, 71))
        self.Cli_Time_Browser.setObjectName("Cli_Time_Browser")
        self.Cli_IP_ComboBox = QtWidgets.QComboBox(self.Client_Tab)
        self.Cli_IP_ComboBox.setGeometry(QtCore.QRect(110, 10, 431, 31))
        self.Cli_IP_ComboBox.setObjectName("Cli_IP_ComboBox")
        self.Cli_PORT_Label = QtWidgets.QLabel(self.Client_Tab)
        self.Cli_PORT_Label.setGeometry(QtCore.QRect(20, 50, 81, 36))
        font = QtGui.QFont()
        font.setFamily("HY나무B")
        font.setPointSize(18)
        self.Cli_PORT_Label.setFont(font)
        self.Cli_PORT_Label.setObjectName("Cli_PORT_Label")
        self.Cli_Trans_Button = QtWidgets.QToolButton(self.Client_Tab)
        self.Cli_Trans_Button.setGeometry(QtCore.QRect(790, 920, 221, 81))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.Cli_Trans_Button.setFont(font)
        self.Cli_Trans_Button.setObjectName("Cli_Trans_Button")
        self.Exit_Button = QtWidgets.QToolButton(self.Client_Tab)
        self.Exit_Button.setGeometry(QtCore.QRect(550, 50, 221, 31))
        self.Exit_Button.setObjectName("Exit_Button")
        self.Cli_Message_Label = QtWidgets.QLabel(self.Client_Tab)
        self.Cli_Message_Label.setGeometry(QtCore.QRect(380, 90, 69, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Cli_Message_Label.setFont(font)
        self.Cli_Message_Label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Cli_Message_Label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Cli_Message_Label.setObjectName("Cli_Message_Label")
        self.Cli_LOGO_Label = QtWidgets.QLabel(self.Client_Tab)
        self.Cli_LOGO_Label.setGeometry(QtCore.QRect(880, 100, 48, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.Cli_LOGO_Label.setFont(font)
        self.Cli_LOGO_Label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Cli_LOGO_Label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Cli_LOGO_Label.setObjectName("Cli_LOGO_Label")
        self.tabWidget.addTab(self.Client_Tab, "")
        ChatProgram.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ChatProgram)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1054, 34))
        self.menubar.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("HY나무B")
        font.setPointSize(10)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("HY나무B")
        font.setPointSize(10)
        self.menuEdit.setFont(font)
        self.menuEdit.setObjectName("menuEdit")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setFamily("HY나무B")
        font.setPointSize(10)
        self.menuhelp.setFont(font)
        self.menuhelp.setObjectName("menuhelp")
        ChatProgram.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ChatProgram)
        self.statusbar.setObjectName("statusbar")
        ChatProgram.setStatusBar(self.statusbar)
        self.Open = QtWidgets.QAction(ChatProgram)
        self.Open.setObjectName("Open")
        self.Save = QtWidgets.QAction(ChatProgram)
        self.Save.setObjectName("Save")
        self.SaveAs = QtWidgets.QAction(ChatProgram)
        self.SaveAs.setObjectName("SaveAs")
        self.Print = QtWidgets.QAction(ChatProgram)
        self.Print.setObjectName("Print")
        self.Exit = QtWidgets.QAction(ChatProgram)
        self.Exit.setObjectName("Exit")
        self.Undo = QtWidgets.QAction(ChatProgram)
        font = QtGui.QFont()
        font.setFamily("HY나무B")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.Undo.setFont(font)
        self.Undo.setObjectName("Undo")
        self.Settings = QtWidgets.QAction(ChatProgram)
        self.Settings.setObjectName("Settings")
        self.Redo = QtWidgets.QAction(ChatProgram)
        self.Redo.setObjectName("Redo")
        self.Cut = QtWidgets.QAction(ChatProgram)
        self.Cut.setObjectName("Cut")
        self.Copy = QtWidgets.QAction(ChatProgram)
        self.Copy.setObjectName("Copy")
        self.Paste = QtWidgets.QAction(ChatProgram)
        self.Paste.setObjectName("Paste")
        self.Delete = QtWidgets.QAction(ChatProgram)
        self.Delete.setObjectName("Delete")
        self.Find = QtWidgets.QAction(ChatProgram)
        self.Find.setObjectName("Find")
        self.SelectAll = QtWidgets.QAction(ChatProgram)
        self.SelectAll.setObjectName("SelectAll")
        self.Help = QtWidgets.QAction(ChatProgram)
        self.Help.setObjectName("Help")
        self.About = QtWidgets.QAction(ChatProgram)
        self.About.setObjectName("About")
        self.menuFile.addAction(self.Open)
        self.menuFile.addAction(self.Save)
        self.menuFile.addAction(self.SaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.Print)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.Settings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.Exit)
        self.menuEdit.addAction(self.Undo)
        self.menuEdit.addAction(self.Redo)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.Cut)
        self.menuEdit.addAction(self.Copy)
        self.menuEdit.addAction(self.Paste)
        self.menuEdit.addAction(self.Delete)
        self.menuEdit.addAction(self.SelectAll)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.Find)
        self.menuhelp.addAction(self.Help)
        self.menuhelp.addSeparator()
        self.menuhelp.addAction(self.About)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())

        self.retranslateUi(ChatProgram)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(ChatProgram)

    def retranslateUi(self, ChatProgram):
        _translate = QtCore.QCoreApplication.translate
        ChatProgram.setWindowTitle(_translate("ChatProgram", "Chat Program - V1.0"))
        self.Start_Button.setText(_translate("ChatProgram", "Start"))
        self.Stop_Button.setText(_translate("ChatProgram", "Stop"))
        self.IP_Label.setText(_translate("ChatProgram", "IP"))
        self.Broadcase_Edit.setHtml(_translate("ChatProgram",
                                               "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                               "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                               "p, li { white-space: pre-wrap; }\n"
                                               "</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                               "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">공지: </span></p></body></html>"))
        self.PORT_Label.setText(_translate("ChatProgram", "PORT"))
        self.LOGO_Label.setText(_translate("ChatProgram", "LOGO MESSAGE"))
        self.Time_Browser.setHtml(_translate("ChatProgram",
                                             "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                             "p, li { white-space: pre-wrap; }\n"
                                             "</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                             "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.LOGO_Label_2.setText(_translate("ChatProgram", "USERS"))
        self.UserList_Browser.setHtml(_translate("ChatProgram",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.Trans_Button.setText(_translate("ChatProgram", "전송"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Server_Tab), _translate("ChatProgram", "Server"))
        self.Entere_Button.setText(_translate("ChatProgram", "Enter"))
        self.Cli_UserList_Browser.setHtml(_translate("ChatProgram",
                                                     "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                     "p, li { white-space: pre-wrap; }\n"
                                                     "</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                                     "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.Cli_Chat_Edit.setHtml(_translate("ChatProgram",
                                              "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                              "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">나:</p></body></html>"))
        self.Cli_IP_Label.setText(_translate("ChatProgram", "IP"))
        self.Cli_Time_Browser.setHtml(_translate("ChatProgram",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'Agency FB\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.Cli_PORT_Label.setText(_translate("ChatProgram", "PORT"))
        self.Cli_Trans_Button.setText(_translate("ChatProgram", "전송"))
        self.Exit_Button.setText(_translate("ChatProgram", "exit"))
        self.Cli_Message_Label.setText(_translate("ChatProgram", "MESSAGE"))
        self.Cli_LOGO_Label.setText(_translate("ChatProgram", "USERS"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Client_Tab), _translate("ChatProgram", "Client"))
        self.menuFile.setTitle(_translate("ChatProgram", "File"))
        self.menuEdit.setTitle(_translate("ChatProgram", "Edit"))
        self.menuTools.setTitle(_translate("ChatProgram", "Tools"))
        self.menuhelp.setTitle(_translate("ChatProgram", "Help"))
        self.Open.setText(_translate("ChatProgram", "Open                   Ctrl + O"))
        self.Save.setText(_translate("ChatProgram", "Save                    Ctrl + S"))
        self.SaveAs.setText(_translate("ChatProgram", "Save As      Ctrl + Shift + S"))
        self.Print.setText(_translate("ChatProgram", "Print                    Ctrl + P"))
        self.Exit.setText(_translate("ChatProgram", "Exit"))
        self.Undo.setText(_translate("ChatProgram", "Undo                   Ctrl + Z"))
        self.Settings.setText(_translate("ChatProgram", "Settings"))
        self.Redo.setText(_translate("ChatProgram", "Redo         Ctrl + Shift + Z"))
        self.Cut.setText(_translate("ChatProgram", "Cut                      Ctrl + X"))
        self.Copy.setText(_translate("ChatProgram", "Copy                    Ctrl + C"))
        self.Paste.setText(_translate("ChatProgram", "Paste                    Ctrl + P"))
        self.Delete.setText(_translate("ChatProgram", "Delete                   Delete"))
        self.Find.setText(_translate("ChatProgram", "Find                      Ctrl + F"))
        self.SelectAll.setText(_translate("ChatProgram", "Select all                Ctrl + A"))
        self.Help.setText(_translate("ChatProgram", "Help"))
        self.About.setText(_translate("ChatProgram", "About"))

class Socket_Thread(QtCore.QThread):
    First_Signal = QtCore.pyqtSignal(object)
    Second_Signal = QtCore.pyqtSignal(bytes, tuple)
    List_Signal = QtCore.pyqtSignal(object)

    def __init__(self,IP,PORT):
        super().__init__()

        self.SOCKET = socket(AF_INET, SOCK_STREAM)
        self.IP = IP
        self.PORT = PORT
        self.input_list = [self.SOCKET]

    def run(self):
        # Socket 바인딩
        self.SOCKET.bind((self.IP, self.PORT))

        # Socket의 수신 대기
        self.SOCKET.listen(1)
        while True:
            self.read_list, self.write_list, self.except_list = select.select(self.input_list, [], [])
            for i in self.read_list:
                if i == self.input_list[0]:
                    self.Cli, self.Adress = self.input_list[0].accept()
                    self.input_list.append(self.Cli)
                    self.Cli.send((str(self.Adress) + " is Enter").encode())
                    self.List_Signal.emit(self.input_list)
                    self.First_Signal.emit(self.Adress)
                else:
                    self.DATA = i.recv(1024)
                    if self.DATA:
                        self.Second_Signal.emit(self.DATA, i.getpeername())
                        i.send(self.DATA)


class Time_Thread(QtCore.QThread):
    Time_Signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            self.Time = str(datetime.datetime.now())
            self.Time = self.Time.split(".")
            self.Time = self.Time[0]
            self.Time_Signal.emit(self.Time)
            time.sleep(1)



class MyMain(MyGui):
    def __init__(self):
        super().__init__(ChatProgram)

        # IP, PORT 리스트 생성
        self.IP_ComboBox.addItem("127.0.0.1")
        self.PORT_ComboBox.addItem(str(5376))

        # 버튼 연결
        self.Start_Button.clicked.connect(self.connect)
        self.Trans_Button.clicked.connect(self.transmission)
        self.Stop_Button.clicked.connect(self.Thread_Quit)

        # 스레드 객채 생성
        self.tk1 = Socket_Thread(str(self.IP_ComboBox.currentText()),int(self.PORT_ComboBox.currentText()))
        self.tk2 = Time_Thread()
        self.tk2.start()


        # 소켓 스레드 신호 받기
        self.tk1.List_Signal.connect(self.Menu)
        self.tk1.First_Signal.connect(self.Connection_Msg)
        self.tk1.Second_Signal.connect(self.Data_Msg)
        self.tk2.Time_Signal.connect(self.Show_Time)

    def Menu(self,List):
        List = list(List)
        self.List = List

    def connect(self):
        self.tk1.start()
        self.Message_Browser.append("Waiting for Request.....")

    def Thread_Quit(self):
        self.tk1.quit()
        self.Message_Browser.append("Server was quit")

    def Connection_Msg(self,address):
        address = str(address)
        address = address.replace(","," : ")
        address = address.replace("'","")
        self.Message_Browser.append("connected by " + str(address))
        self.UserList_Browser.append(str(address))



    def Data_Msg(self,msg,who):
        who = str(who)
        who = who.replace(","," : ")
        who = who.replace("'","")
        self.Message_Browser.append(str(self.Time_Browser.toPlainText()) + " " + (who) + " send: " + str(msg.decode()))

    def transmission(self):
        self.txt = ""
        self.txt = self.Broadcase_Edit.toPlainText()
        self.txt = self.txt + "administrator"
        for i in range(1, len(self.List)):
            self.List[i].send(self.txt.encode())
        self.txt = self.txt.replace("administrator","")
        self.Message_Browser.append(self.txt)
        self.Broadcase_Edit.setText("공지: ")

    def Show_Time(self,LiveTime):
        self.Time_Browser.setText(LiveTime)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChatProgram = QtWidgets.QMainWindow()
    ui = MyMain()
    ChatProgram.show()
    sys.exit(app.exec_())

