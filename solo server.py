from socket import *
import threading
import select

# 주소와 포트 지정
IP = ''
PORT = 6969
ADDRESS = (IP,PORT)

def Connection(address):
    # Socket 생성
    SOCKET = socket(AF_INET, SOCK_STREAM)
    print("소켓을 생성했습니다.\n")

    # Socket 바인딩
    SOCKET.bind(address)
    print("바인딩에 성공했습니다.\n")

    # Socket의 수신 대기
    SOCKET.listen(1)
    print("수신 대기 중 입니다.\n")

    CON, SOCKET_ADDRES = SOCKET.accept()

    return CON, SOCKET_ADDRES

def Receive_Message(CON):
    while True:
        DATA = CON.recv(1024)
        print("\n상대:\n", DATA.decode())
        Sand_Message

def Sand_Message(CON):
    while True:
        DATA = input("나:")
        CON.send(DATA.encode())

# 클라이언트 연결 함수 호출
CON, SOCKET_ADDRES= Connection(ADDRESS)


tk1 = threading.Thread(target=Sand_Message,args=(CON,))
tk2 = threading.Thread(target=Receive_Message,args=(CON,))
tk1.start()
tk2.start()