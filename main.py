import socket


ip = '127.0.0.1'
port = 9000
addr = (ip, port)
clients_count = 3


def launch_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    print(f'[!] The server is running. IP: {ip} Port {port}')
    return sock


def server_listen(sock):
    try:
        print('[!] The server waiting for connection')
        sock.listen(clients_count)
        while True:
            client_sock, client_address = sock.accept()
            print(f'[!] Connected! Client`s address: {client_address}')
            data = client_sock.recv(1024).decode('utf-8')
            print(data)
            client_sock.send(f'Hello from server {ip}'.encode('utf-8'))
            print(f'[!] Hello message has been sent: {client_address}')
            client_sock.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    server = launch_server()
    server_listen(server)
