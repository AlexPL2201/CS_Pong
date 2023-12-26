import socket
from datetime import datetime as dt
import serv_settings
import cmds


def launch_server():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(serv_settings.addr)
        print(f'[!] <{dt.now()}> The server is running. IP: {serv_settings.ip} Port {serv_settings.port}.')
        return sock

    except socket.error as e:
        print(f"[ERR] <{dt.now()}> Socket binding error: {e}.")
        sock.close()
    return -1


def server_listen(sock):
    try:
        print(f'[!] <{dt.now()}> The server waiting for connection.')
        sock.listen(serv_settings.clients_count)
        while True:
            client_sock, client_address = sock.accept()
            print(f'[!] <{dt.now()}> Connected! Client`s address: {client_address}.')
            data = client_sock.recv(1024).decode('utf-8')
            command, arguments = parse_message(data)
            print(f'[!] <{dt.now()}> Message received! Command: {command} | Arguments: {arguments}.')
            status, log = exec_command(command, arguments)
            answer = f'Status: {status} | Message: {log}'
            client_sock.send(answer.encode('utf-8'))
            print(f'[!] <{dt.now()}> Answer has been sent: {answer}.')
            client_sock.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        print(f'[END] <{dt.now()}> The server has shut down.')
        server.close()


def parse_message(msg):
    msg_list = msg.split(' ')
    return msg_list[0], msg_list[1:len(msg_list)]


def exec_command(cmd, args):
    if cmd == 'LOGIN': # LOGIN PlayerName PassWord
        return cmds.login(args)
    elif cmd == 'REGISTER': # REGISTER PlayerName PassWord
        return cmds.register(args)
    elif cmd == 'CHANGE': # CHANGE PlayerName Password NewPlayerName
        return cmds.change_player_name(args)
    elif cmd == 'DELETE': # DELETE PlayerName Password
        return cmds.del_profile(args)
    elif cmd == 'GETSCORE': # GETSCORE PlayerName
        return cmds.get_user_score(args)
    elif cmd == 'ENDGAME': # ENDGAME PlayerName Score
        return cmds.update_user_score(args)
    elif cmd == 'TOPSCORE':
        return cmds.get_top_players()
    elif cmd == 'RUNGAME': # RUNGAME PlayerName Password
        return cmds.run(args)


if __name__ == '__main__':
    server = launch_server()
    if server != -1:
        server_listen(server)
