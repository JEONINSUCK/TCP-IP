from socket import *
import select
import threading

# 주소와 포트 지정
IP = ''
PORT = 6969
ADDRESS = (IP,PORT)

# 서버 공지
def brodcase(List):
    Message = input("공지: ")
    Message = Message + "administrator"
    for i in range(1,len(List)):
        List[i].send(Message.encode())


# 다른 클라이언트 접속과 보낸 메시지를 감시하여 처리
def opserver(List, Socket):
    tk1 = threading.Thread(target=brodcase,args=(List,))
    tk1.start()

    while True:
        input_list, write_list, except_list = select.select(List,[],[])
        for i in input_list:
            if i == Socket:
                Cli, Adress = Socket.accept()
                print("CONNECTED BY" , Adress)
                List.append(Cli)
            else:
                if i == List[1]:
                    i = List[1]
                    j = List[2]
                else:
                    i = List[2]
                    j = List[1]
                DATA = i.recv(1024)
                if DATA:
                    print(i.getsockname(), 'send :', DATA.decode())
                    j.send(DATA)

# 서버 활성화
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

    # 클라이언트 리스트 관리
    input_list = [SOCKET]


    opserver(input_list, SOCKET)

Connection(ADDRESS)