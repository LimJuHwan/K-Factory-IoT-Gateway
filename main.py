import time

import socket
from multiprocessing import Process, Queue
from threading import Thread

def connect_server(q):
    HOST = "localhost"
    PORT = 8899

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    while True:
        # client_socket.send("hello3".encode())
        # print("hello4")

        if q.empty():
            continue

        data = q.get()
        client_socket.send(data.encode())


    client_socket.close()

def handle_client(client_socket, addr, q):
    print("Client address : ", addr)

    while True:
        recv_data = client_socket.recv(1024).decode()
        print("Receive data : ", recv_data)

        # send to server
        q.put(recv_data)
        # print("jellow")
        # q.put("hello1")

        time.sleep(1)

    client_socket.close()


def create_gateway(q):
    HOST = ""
    PORT = 8989

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    #     server_socket.bind((HOST, PORT))  # 주소 바인딩
    #     server_socket.listen()  # 클라이언트의 요청을 받을 준비
    #
    #     client_socket, client_addr = server_socket.accept()  # 수신대기, 접속한 클라이언트 정보 (소켓, 주소) 반환
    #
    #     # 무한루프 진입
    #     while True:
    #         msg = client_socket.recv(1024)  # 클라이언트가 보낸 메시지 반환
    #         print("[{}] message : {}".format(client_addr, msg))  # 클라이언트가 보낸 메시지 출력
    #
    #         client_socket.sendall("welcome!".encode())  # 클라이언트에게 응답
    #
    #     client_socket.close()  # 클라이언트 소켓 종료

    gateway_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    gateway_socket.bind((HOST, PORT))
    gateway_socket.listen()

    while True:
        try:
            client_socket, addr = gateway_socket.accept()

            print("Accept")
        except:
            gateway_socket.close()

        client_thread = Thread(target=handle_client, args=(client_socket, addr, q))
        client_thread.daemon = True
        client_thread.start()

if __name__ == "__main__":

    q = Queue()

    process_list = []

    # Create multi processing
    process_connect_server = Process(target=connect_server, args=(q,))
    process_create_gateway = Process(target=create_gateway, args=(q,))

    process_list.append(process_connect_server)
    process_list.append(process_create_gateway)

    process_connect_server.start()
    process_create_gateway.start()

    while True:
        pass
