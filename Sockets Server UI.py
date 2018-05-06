from socket import *
import select
import threading
from PyQt5 import QtCore, QtGui, QtWidgets

# 주소와 포트 지정
IP = ''
PORT = 5376
ADDRESS = (IP,PORT)

#class User_Manager:

class connection(QtCore.QThread):
    First_Signal = QtCore.pyqtSignal(object)
    Second_Signal = QtCore.pyqtSignal(bytes,tuple)
    List_Signal = QtCore.pyqtSignal(object)
    def __init__(self):
        super().__init__()

        self.SOCKET = socket(AF_INET, SOCK_STREAM)
        print("소켓을 생성했습니다.\n")

        # Socket 바인딩
        self.SOCKET.bind(ADDRESS)
        print("바인딩에 성공했습니다.\n")

        # Socket의 수신 대기
        self.SOCKET.listen(1)
        print("수신 대기 중 입니다.\n")

        self.input_list = [self.SOCKET]

    def run(self):

       while True:
            self.read_list, self.write_list, self.except_list = select.select(self.input_list, [], [])
            for i in self.read_list:
                if i == self.input_list[0]:
                    self.Cli, self.Adress = self.input_list[0].accept()
                    self.input_list.append(self.Cli)
                    self.List_Signal.emit(self.input_list)
                    self.First_Signal.emit(self.Adress)
                else:
                    if i == self.input_list[1]:
                        i = self.input_list[1]
                        j = self.input_list[2]
                    else:
                        i = self.input_list[2]
                        j = self.input_list[1]
                    self.DATA = i.recv(1024)
                    if self.DATA:
                        print(i.getpeername())
                        print(type(i.getpeername()))
                        self.Second_Signal.emit(self.DATA,i.getpeername())
                        j.send(self.DATA)


# UI 클래스
class MyGui(object):
    def __init__(self,Form):
        Form.setObjectName("Form")
        Form.resize(962, 826)
        self.Port_label = QtWidgets.QLabel(Form)
        self.Port_label.setGeometry(QtCore.QRect(670, 70, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Port_label.setFont(font)
        self.Port_label.setMouseTracking(False)
        self.Port_label.setTabletTracking(False)
        self.Port_label.setAutoFillBackground(False)
        self.Port_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Port_label.setObjectName("Port_label")
        self.Users_label = QtWidgets.QLabel(Form)
        self.Users_label.setGeometry(QtCore.QRect(700, 240, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Users_label.setFont(font)
        self.Users_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Users_label.setTextFormat(QtCore.Qt.AutoText)
        self.Users_label.setScaledContents(False)
        self.Users_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Users_label.setWordWrap(False)
        self.Users_label.setOpenExternalLinks(False)
        self.Users_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.Users_label.setObjectName("Users_label")
        self.Trans_Button = QtWidgets.QToolButton(Form)
        self.Trans_Button.setGeometry(QtCore.QRect(720, 650, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.Trans_Button.setFont(font)
        self.Trans_Button.setAutoRepeat(False)
        self.Trans_Button.setObjectName("Trans_Button")
        self.Address_label = QtWidgets.QLabel(Form)
        self.Address_label.setGeometry(QtCore.QRect(670, 140, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.Address_label.setFont(font)
        self.Address_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Address_label.setObjectName("Address_label")
        self.Search_Button = QtWidgets.QToolButton(Form)
        self.Search_Button.setGeometry(QtCore.QRect(720, 730, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.Search_Button.setFont(font)
        self.Search_Button.setAutoRepeat(False)
        self.Search_Button.setObjectName("Search_Button")
        self.Title_label = QtWidgets.QLabel(Form)
        self.Title_label.setGeometry(QtCore.QRect(250, 60, 191, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Title_label.setFont(font)
        self.Title_label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Title_label.setTextFormat(QtCore.Qt.AutoText)
        self.Title_label.setScaledContents(False)
        self.Title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Title_label.setWordWrap(False)
        self.Title_label.setOpenExternalLinks(False)
        self.Title_label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.Title_label.setObjectName("Title_label")
        self.Connect_Button = QtWidgets.QToolButton(Form)
        self.Connect_Button.setGeometry(QtCore.QRect(670, 200, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.Connect_Button.setFont(font)
        self.Connect_Button.setAutoRepeat(False)
        self.Connect_Button.setObjectName("Connect_Button")
        self.MessageBox = QtWidgets.QTextBrowser(Form)
        self.MessageBox.setGeometry(QtCore.QRect(30, 120, 621, 491))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.MessageBox.setFont(font)
        self.MessageBox.setObjectName("MessageBox")
        self.UsersList = QtWidgets.QTextBrowser(Form)
        self.UsersList.setGeometry(QtCore.QRect(670, 280, 256, 331))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        self.UsersList.setFont(font)
        self.UsersList.setObjectName("UsersList")
        self.Port_Browser = QtWidgets.QTextBrowser(Form)
        self.Port_Browser.setGeometry(QtCore.QRect(790, 70, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Port_Browser.setFont(font)
        self.Port_Browser.setObjectName("Port_Browser")
        self.Address_Browser = QtWidgets.QTextBrowser(Form)
        self.Address_Browser.setGeometry(QtCore.QRect(790, 140, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Address_Browser.setFont(font)
        self.Address_Browser.setObjectName("Address_Browser")
        self.Write_Box = QtWidgets.QTextEdit(Form)
        self.Write_Box.setGeometry(QtCore.QRect(30, 640, 621, 161))
        self.Write_Box.setObjectName("Write_Box")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        Form.show()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Port_label.setText(_translate("Form", "PORT"))
        self.Users_label.setText(_translate("Form", "USERS"))
        self.Trans_Button.setText(_translate("Form", "전 송"))
        self.Address_label.setText(_translate("Form", "ADDRESS"))
        self.Search_Button.setText(_translate("Form", "검 색"))
        self.Title_label.setText(_translate("Form", "실시간 채팅"))
        self.Connect_Button.setText(_translate("Form", "접 속"))


class MyMain(MyGui):
    def __init__(self):
        super().__init__(Form)



        # 버튼 연결
        self.Connect_Button.clicked.connect(self.sho)
        self.Connect_Button.clicked.connect(self.connect)

        self.tk1 = connection()
        self.Trans_Button.clicked.connect(self.transmission)
        self.tk1.List_Signal.connect(self.Menu)
        self.tk1.First_Signal.connect(self.gogogo)
        self.tk1.Second_Signal.connect(self.gogogo2)

    def Menu(self,List):
        List = list(List)
        self.List = List
        #self.MessageBox.append(str(List))

    def sho(self):
        self.Address_Browser.setText(str(IP))
        self.Address_Browser.setAlignment(QtCore.Qt.AlignCenter)
        self.Port_Browser.setText(str(PORT))
        self.Port_Browser.setAlignment(QtCore.Qt.AlignCenter)

    def connect(self):
        self.tk1.start()
    def gogogo(self,address):
        address = str(address)
        address = address.replace(","," : ")
        address = address.replace("'","")
        self.MessageBox.append("connected by " + str(address))

    def gogogo2(self,msg,who):
        who = str(who)
        who = who.replace(","," : ")
        who = who.replace("'","")
        self.MessageBox.append(str(who) + " send: " + str(msg.decode()))
    def transmission(self):
        self.txt = ""
        self.txt = self.Write_Box.toPlainText()
        self.txt = self.txt + "administrator"
        for i in range(1, len(self.List)):
            self.List[i].send(self.txt.encode())
        self.txt = self.txt.replace("administrator","")
        self.MessageBox.append("공지: " + self.txt)
        self.Write_Box.clear()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = MyMain()
    sys.exit(app.exec_())

