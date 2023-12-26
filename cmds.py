import sqlite3
from datetime import datetime as dt
import threading
import serv_settings
import PingPongServerPy as Pong


def login(args):
    data = (args[0], args[1])
    if is_player_registered(data):
        return 0, '[ERR] An incorrect username or password has been entered'
    return 1, '[SUCCESS] Player was logged in successfully'


def register(args):
    data = (args[0], args[1], 0, 0, 0, dt.now())
    if not is_player_name_unique(args[0]):
        return 0, f"[ERR] PlayerName '{args[0]}' is already in use"
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()

    cursor.execute(f"""INSERT INTO Player
        (PlayerName, HashPassword, Score, TotalGamesPlayed, TotalGamesWon, RegistrationDate)
        VALUES (?, ?, ?, ?, ?, ?)""", data)

    con.commit()
    con.close()
    return 1, f"[SUCCESS] PlayerName '{args[0]}' has been successfully registered"


def del_profile(args):
    if is_player_registered((args[0], args[1])):
        return 0, '[ERR] An incorrect username or password has been entered',
    data = (args[0],)
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('DELETE FROM Player WHERE PlayerName = ?', data)
    con.commit()
    con.close()
    return 1, f"[SUCCESS] Player with PlayerName '{data}' has been successfully removed from database"


def change_player_name(args):
    if is_player_registered((args[0], args[1])) or not is_player_name_unique(args[2]):
        return 0, f"[ERR] <{dt.now()}> An incorrect username or password has been entered or new name already in use"
    data = (args[2], args[0])
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('UPDATE Player SET PlayerName = ? WHERE PlayerName = ?', data)
    con.commit()
    con.close()
    return 1, f"[SUCCESS] PlayerName '{args[0]}' successfully changed to '{args[2]}'"


def get_user_score(args):
    if is_player_name_unique(args[0]):
        return 0, f"[ERR] <{dt.now()}> An incorrect username has been entered"
    data = (args[0],)
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('SELECT Score FROM Player WHERE PlayerName = ?', data)
    player_score = cursor.fetchone()
    con.close()
    return 1, f"[SUCCESS] Score of the player '{data[0]}': {player_score[0]}"


def update_user_score(args):
    if is_player_name_unique(args[0]):
        return 0, f"[ERR] An incorrect username has been entered"
    data = (int(args[1]), args[0])
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('UPDATE Player SET Score = Score + ? WHERE PlayerName = ?', data)
    con.commit()
    con.close()
    return 1, f"[SUCCESS] Score of the player '{data[1]}' has been changed"


def get_top_players():
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('SELECT PlayerName, Score FROM Player ORDER BY Score DESC LIMIT 5')
    top_players = cursor.fetchall()
    con.close()
    msg = ''
    for player in top_players:
        msg += f'{player[0]} {player[1]} '
    return 1, f"[SUCCESS] {msg}"


def run(args):
    if is_player_registered((args[0], args[1])):
        return 0, '[ERR] An incorrect username or password has been entered',
    thread = threading.Thread(target=Pong.Game.play)
    thread.start()
    return serv_settings.game_port, 'Game port'



# Child commands
def is_player_registered(data):
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('SELECT PlayerName FROM Player WHERE (PlayerName, HashPassword) = (?, ?)', data)
    is_correct = cursor.fetchone()
    con.close()
    return is_correct is None


def is_player_name_unique(player_name):
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('SELECT PlayerName FROM Player WHERE PlayerName = ?', (player_name,))
    existing_player = cursor.fetchone()
    con.close()
    return existing_player is None
