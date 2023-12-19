import socket
import sqlite3


ip = '127.0.0.1'
port = 9000
addr = (ip, port)
clients_count = 3


def launch_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(addr)
        print(f'[!] The server is running. IP: {ip} Port {port}')
        return sock

    except socket.error as e:
        print(f"[ERR] Socket binding error: {e}")
        sock.close()
    return -1


def server_listen(sock):
    try:
        print('[!] The server waiting for connection')
        sock.listen(clients_count)
        while True:
            client_sock, client_address = sock.accept()
            print(f'[!] Connected! Client`s address: {client_address}')
            data = client_sock.recv(1024).decode('utf-8')
            command, arguments = parse_message(data)
            print(f'Command: {command}\nArguments: {arguments[0]} {arguments[1]}')
            exec_command(command, arguments)
            client_sock.send(f'Hello from server {ip}'.encode('utf-8'))
            print(f'[!] Hello message has been sent: {client_address}')
            client_sock.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        print('[END] The server has shut down')
        server.close()


def parse_message(msg):
    msg_list = msg.split(' ')
    return msg_list[0], msg_list[1:len(msg_list)]


def exec_command(cmd, args):
    if cmd == 'LOGIN':
        login()
    if cmd == 'REGISTER':
        register()


def login():
    pass


def register():
    pass


if __name__ == '__main__':
    server = launch_server()
    if server != -1:
        server_listen(server)
