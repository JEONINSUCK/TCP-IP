
from socket import *
import threading
# 서버 주소와 포트 지정
IP = '127.0.0.1'
PORT = 6969
ADDRESS = (IP,PORT)


def Make_Socket(address):
    # 클라이언트 소켓 생성
    SOCKET = socket(AF_INET, SOCK_STREAM)
    print("소켓이 생성되었습니다.\n")

    # 서버와 연결
    SOCKET.connect(address)
    print("서버와 연결되었습니다.\n")

    return SOCKET

def Sand_Message(SOCKET):
    while True:
        MESSAGE = (input("나:"))
        SOCKET.sendall(MESSAGE.encode())


def Receive_Message(SOCKET):
    while True:
        DATA = SOCKET.recv(1024).decode()
        if DATA.find("administrator") == -1:
            print("\n상대:", DATA)
        else:
            DATA = DATA.replace("administrator","")
            print("\n공지:", DATA)

# 소켓 생성후 서버와 연결 함수
Socket = Make_Socket(ADDRESS)


tk1 = threading.Thread(target=Sand_Message,args=(Socket,))
tk2 = threading.Thread(target=Receive_Message,args=(Socket,))
tk1.start()
tk2.start()
