import socket
import sqlite3
from datetime import datetime as dt

db_path = 'db.db'
ip = '127.0.0.1'
port = 9000
addr = (ip, port)
clients_count = 3


def launch_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(addr)
        print(f'[!] <{dt.now()}> The server is running. IP: {ip} Port {port}')
        return sock

    except socket.error as e:
        print(f"[ERR] <{dt.now()}> Socket binding error: {e}")
        sock.close()
    return -1


def server_listen(sock):
    try:
        print(f'[!] <{dt.now()}> The server waiting for connection')
        sock.listen(clients_count)
        while True:
            client_sock, client_address = sock.accept()
            print(f'[!] <{dt.now()}> Connected! Client`s address: {client_address}')
            data = client_sock.recv(1024).decode('utf-8')
            command, arguments = parse_message(data)
            print(f'[!] Message received! Command: {command} | Arguments: {arguments[0]} {arguments[1]}')
            status, log = exec_command(command, arguments)
            answer = f'Status: {status} | Message: {log}'
            client_sock.send(answer.encode('utf-8'))
            print(f'[!] <{dt.now()}> Answer has been sent: {answer}')
            client_sock.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        print(f'[END] <{dt.now()}> The server has shut down')
        server.close()


def parse_message(msg):
    msg_list = msg.split(' ')
    return msg_list[0], msg_list[1:len(msg_list)]


def exec_command(cmd, args):
    if cmd == 'LOGIN':
        login()
    elif cmd == 'REGISTER':
        return register(args)


def login():
    pass


def register(args):
    data = (args[0], args[1], 0, 0, 0, dt.now())
    if not is_player_name_unique(args[0]):
        return 0, f"[ERR] <{dt.now()}> PlayerName '{args[0]}' is already in use"
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute(f"""INSERT INTO Player
        (PlayerName, HashPassword, Score, TotalGamesPlayed, TotalGamesWon, RegistrationDate)
        VALUES (?, ?, ?, ?, ?, ?)""", data)
    con.commit()
    con.close()
    return 1, f"[SUCCESS] <{dt.now()}> PlayerName '{args[0]}' has been successfully registered"


def is_player_name_unique(player_name):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute('SELECT PlayerName FROM Player WHERE PlayerName = ?', (player_name,))

    # Получаем первую строку результата
    existing_player = cursor.fetchone()
    con.close()

    # Возвращаем True, если имя уникально, и False в противном случае
    return existing_player is None


if __name__ == '__main__':
    server = launch_server()
    if server != -1:
        server_listen(server)
