from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from socket import *
import select
import datetime
import time

Form = uic.loadUiType("ChatProgram.ui")[0]


# 서버측에서 접속자 관리 및 메세지 관리 스레드
class Server_Socket_Thread(QtCore.QThread):
    Entering_User_Signal = QtCore.pyqtSignal(object)
    Msg_Signal = QtCore.pyqtSignal(bytes, tuple)
    UserList_Signal = QtCore.pyqtSignal(object, object)

    def __init__(self, IP, PORT):
        super().__init__()
        self.Working = False

        self.SOCKET = socket(AF_INET, SOCK_STREAM)
        self.IP = IP
        self.PORT = int(PORT)
        self.input_list = [self.SOCKET]

    def run(self):
        # Socket 바인딩
        self.SOCKET.bind((self.IP, self.PORT))

        # Socket의 수신 대기
        self.SOCKET.listen(1)

        while self.Working == True:
            self.read_list, self.write_list, self.except_list = select.select(self.input_list, [], [])
            if self.Working == False:
                self.Close_Msg = Notice_To_User_Thread(self.input_list,"{CLOSED}|Server was closed",People=None)
                self.Close_Msg.start()
                break
            for i in self.read_list:
                if i == self.input_list[0]:
                    self.Cli, self.Adress = self.input_list[0].accept()
                    self.input_list.append(self.Cli)
                    self.Entering_User_Signal.emit(self.Adress)
                    self.UserList_Signal.emit(self.input_list, self.Adress)

                else:
                    self.DATA = i.recv(1024)
                    if self.DATA:
                        self.Msg_Signal.emit(self.DATA, i.getpeername())


# 각종 메시지 클라이언트에게 전달 스레드
class Notice_To_User_Thread(QtCore.QThread):
    def __init__(self, UserList, Notice, People):
        super().__init__()
        self.UserList = UserList
        self.Notice = Notice
        self.People = People

    def run(self):
        for i in self.UserList:
            if i == self.UserList[0]:
                continue
            else:
                if self.People is not None:
                    i.send((self.People).encode())
                    i.send((self.Notice).encode())
                else:
                    i.send((self.Notice).encode())


# 클라이언에서 메시지를 수신을 받는 스레드
class Cli_Receive_Msg_Thread(QtCore.QThread):
    Cli_Message_Signal = QtCore.pyqtSignal(str)

    def __init__(self, Socket):
        super().__init__()
        self.Socket = Socket
        self.Cli_Receive_Msg_Thread_Working = False

    def run(self):
        while self.Cli_Receive_Msg_Thread_Working is True:
            self.DATA = self.Socket.recv(1024).decode()
            if self.DATA:
                self.Cli_Message_Signal.emit(self.DATA)


# 서버에 시간을 갱신해주는 스레드
class Server_Time_Thread(QtCore.QThread):
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


# 클라이언트 시간을 갱신해주는 스레드
class Cli_Time_Thread(QtCore.QThread):
    Cli_Time_Signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            self.Time = str(datetime.datetime.now())
            self.Time = self.Time.split(".")
            self.Time = self.Time[0]
            self.Cli_Time_Signal.emit(self.Time)
            time.sleep(1)


class MyMain(QtWidgets.QMainWindow, Form):
    def __init__(self):
        super().__init__()
        # ui 불러오기
        self.setupUi(self)

        # 서버 IP, PORT 리스트 생성
        self.IP_ComboBox.addItem("127.0.0.1")
        self.PORT_ComboBox.addItem(str(5376))

        # 서버 버튼 연결
        self.Start_Button.clicked.connect(self.Server_Starting)
        self.Stop_Button.clicked.connect(self.Server_Stopping)
        self.Trans_Button.clicked.connect(self.Server_Notice_Msg)

        # 서버 스레드 객체 생성
        self.Server_Time_TK = Server_Time_Thread()
        self.Server_Time_TK.start()
        self.Server_Socket_TK = Server_Socket_Thread(IP=self.IP_ComboBox.currentText(),
                                                     PORT=self.PORT_ComboBox.currentText())

        # 서버 스레드 신호 받기
        self.Server_Socket_TK.Entering_User_Signal.connect(self.Entering_User_Logo)
        self.Server_Socket_TK.UserList_Signal.connect(self.User_List_Sync)
        self.Server_Socket_TK.Msg_Signal.connect(self.User_Send_Data)
        self.Server_Time_TK.Time_Signal.connect(self.Server_Time_Show)

        # 클라이언트 소켓 생성
        self.Cli_SOCKET = socket(AF_INET, SOCK_STREAM)

        # 클라이언트 IP, PORT 리스트 생성
        self.Cli_IP_ComboBox.addItem("127.0.0.1")
        self.Cli_PORT_ComboBox.addItem(str(5376))

        # 클라이언트 버튼 연결
        self.Entere_Button.clicked.connect(self.Cli_Starting)
        self.Exit_Button.clicked.connect(self.Cli_Stopping)
        self.Cli_Trans_Button.clicked.connect(self.Cli_SendMessage)

        # 클라이언트 스레드 객체 생성
        self.Cli_Receive_Msg_TK = Cli_Receive_Msg_Thread(self.Cli_SOCKET)
        self.Cli_Time_TK = Cli_Time_Thread()
        self.Cli_Time_TK.start()

        # 클라이언트 스레스 신호 받기
        self.Cli_Receive_Msg_TK.Cli_Message_Signal.connect(self.Cli_Receive_Msg_Process)
        self.Cli_Time_TK.Cli_Time_Signal.connect(self.Cli_Time_Show)

    # 서버 Start 버튼 동작 함수 (소켓 스레드 실행)
    def Server_Starting(self):
        if self.Server_Socket_TK.Working == False:
            self.Server_Starting_Conform = QMessageBox.question(self, "Message", "Are you sure that Turn on the Server?",
                                                QMessageBox.Yes | QMessageBox.No)
            if self.Server_Starting_Conform == QMessageBox.Yes:
                self.Server_Socket_TK.Working = True
                self.Server_Socket_TK.start()
                self.Message_Browser.append("Waiting for Request.....")
            else:
                pass
        else:
            QMessageBox.about(self,"ERROR","Server is already working.....")

    # 서버 Stop 버튼 동작 함수 (소켓 스레드 중지)
    def Server_Stopping(self):
        if self.Server_Socket_TK.Working == True:
            self.Server_Stopping_Conform = QMessageBox.question(self, "Message", "Are you sure that Turn off the Server?",
                                                QMessageBox.Yes | QMessageBox.No)
            if self.Server_Stopping_Conform == QMessageBox.Yes:
                self.Server_Socket_TK.Working = False
                self.Shutdown_Msg = Notice_To_User_Thread(self.UserList,"{CLOSED}|Server was closed",People=None)
                self.Shutdown_Msg.start()
                self.Message_Browser.append("Stopped to your request")
            else:
                pass
        else:
            QMessageBox.about(self,"ERROR","Server was already Stopped")


    # 접속한 유저들 기록을 남기는 함수
    def Entering_User_Logo(self, UserAddress):
        self.UserAddress = str(UserAddress)
        self.UserAddress = self.UserAddress.replace(",", " : ")
        self.UserAddress = self.UserAddress.replace("'", "")
        self.Message_Browser.append(self.Time_Browser.toPlainText() + " connected by " + self.UserAddress)
        self.UserList_Browser.append(self.UserAddress)

    # 서버에서 보내는 공지
    def Server_Notice_Msg(self):
        self.Get_Server_Msg = ""
        self.Get_Server_Msg = self.Broadcase_Edit.toPlainText()
        self.Message_Browser.append(self.Time_Browser.toPlainText() + "공지: " + self.Get_Server_Msg)
        self.Get_Server_Msg = "{ADMINISTRATOR}|" + self.Time_Browser.toPlainText() + "|" + self.Get_Server_Msg
        self.Send_Server_Msg_TK = Notice_To_User_Thread(self.UserList, self.Get_Server_Msg, People=None)
        self.Send_Server_Msg_TK.start()
        self.Broadcase_Edit.setText("")

    # 서버에 접속해는 유저 목록 동기화와 접속자 공지
    def User_List_Sync(self, UserList, EnteringUserAddress):
        self.UserList = list(UserList)
        self.EnteringUserAddress = "{HI}|" + self.Time_Browser.toPlainText() + " " + str(EnteringUserAddress)
        self.People = "{LIST}|" + self.UserList_Browser.toPlainText()
        self.Entering_User_Msg_TK = Notice_To_User_Thread(list(self.UserList), str(self.EnteringUserAddress),
                                                          str(self.People))
        self.Entering_User_Msg_TK.start()

    # 유저가 보낸 메시지 전파 및 로그 남기기
    def User_Send_Data(self, UserData, UserIP):
        self.UserData = UserData.decode()
        self.UserIP = str(UserIP).replace(",", " : ")
        self.UserIP = self.UserIP.replace("'", "")
        self.Send_Users_Msg = "DATA|" + self.Time_Browser.toPlainText() + " |" + self.UserIP + "|" + self.UserData
        self.Message_Browser.append(self.Time_Browser.toPlainText() + " " + self.UserIP + "send: " + self.UserData)
        self.Send_Users_Msg_TK = Notice_To_User_Thread(self.UserList, self.Send_Users_Msg, People=None)
        self.Send_Users_Msg_TK.start()

    # 서버에 현재 시간 표시
    def Server_Time_Show(self, ServerTime):
        self.Time_Browser.setText(ServerTime)

    # 클라이언트 Enter 버튼 동작 함수 (클라이언트에서 메시지 수신하는 스레드 실행)
    def Cli_Starting(self):
        if self.Cli_Receive_Msg_TK.Cli_Receive_Msg_Thread_Working == False:
            self.Cli_Starting_Confrom = QMessageBox.question(self,"Message","Are you sure that Enter the Chat?",QMessageBox.Yes | QMessageBox.No)
            if self.Cli_Starting_Confrom == QMessageBox.Yes:
                self.Cli_Receive_Msg_TK.Cli_Receive_Msg_Thread_Working = True
                self.Cli_SOCKET.connect((str(self.Cli_IP_ComboBox.currentText()), int(self.Cli_PORT_ComboBox.currentText())))
                self.Cli_Receive_Msg_TK.start()
                self.Cli_Message_Browser.append("Complete the connection with Server...")
            else:
                pass
        else:
            QMessageBox.about(self,"ERROR","Already entered the chat")

    # 클라이언트 exit 버튼 동작 함수 (서버에서 오는 메시지를 받는 스레드 종료)
    def Cli_Stopping(self):
        if self.Cli_Receive_Msg_TK.Cli_Receive_Msg_Thread_Working == True:
            self.Cli_Stopping_Confrom = QMessageBox.question(self,"Message","Are you sure that Stop the Chat?",QMessageBox.Yes | QMessageBox.No)
            if self.Cli_Stopping_Confrom == QMessageBox.Yes:
                self.Cli_Receive_Msg_TK.Cli_Receive_Msg_Thread_Working = False
                self.Cli_Message_Browser.settext("")
                self.Cli_Message_Browser.append("Client was exit")
            else:
                pass
        else:
            QMessageBox.about(self,"ERROR","Client was already stopped")

    # 서버에서 온 메시지를 파싱해서 GUI에 보여주기
    def Cli_Receive_Msg_Process(self, GetData):
        self.GetData = GetData
        self.GetData = self.GetData.split("|")
        if self.GetData[0] == "{LIST}":
            self.Cli_UserList_Browser.setText(self.GetData[1])
        elif self.GetData[0] == "{HI}":
            self.Cli_Message_Browser.append(self.GetData[1])
        elif self.GetData[0] == "{ADMINISTRATOR}":
            self.Cli_Message_Browser.append(self.GetData[1] + "공지:" + self.GetData[2])
        elif self.GetData[0] == "{CLOSED}":
            QMessageBox.about(self,"ERROR",self.GetData[1])
        else:
            self.Compare = str(self.Cli_SOCKET.getsockname()).replace("'", "")
            self.Compare = self.Compare.replace(",", " : ")
            if self.GetData[2] == self.Compare:
                self.Cli_Message_Browser.append(self.GetData[1] + "Me: " + self.GetData[3])
            else:
                self.Cli_Message_Browser.append(self.GetData[1] + self.GetData[2] + "Send: " + self.GetData[3])

    # 클라이언트에서 메시지 보내기
    def Cli_SendMessage(self):
        if self.Server_Working == True:
            self.My_Msg = ""
            self.My_Msg = self.Cli_Chat_Edit.toPlainText()
            self.Cli_SOCKET.send(self.My_Msg.encode())
            self.Cli_Chat_Edit.setText("")

    # 클라이언트에 현재 시간 표시
    def Cli_Time_Show(self, CliTime):
        self.Cli_Time_Browser.setText(CliTime)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = MyMain()
    ui.show()
    sys.exit(app.exec_())