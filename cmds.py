import sqlite3
from datetime import datetime as dt
import serv_settings


def login(args):
    data = (args[0], args[1])
    if is_player_registered(data):
        return 0, f'[ERR] <{dt.now()}> An incorrect username or password has been entered'
    return 1, f'[SUCCESS] <{dt.now()}> The account was logged in successfully'


def register(args):
    data = (args[0], args[1], 0, 0, 0, dt.now())
    if not is_player_name_unique(args[0]):
        return 0, f"[ERR] <{dt.now()}> PlayerName '{args[0]}' is already in use"
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()

    cursor.execute(f"""INSERT INTO Player
        (PlayerName, HashPassword, Score, TotalGamesPlayed, TotalGamesWon, RegistrationDate)
        VALUES (?, ?, ?, ?, ?, ?)""", data)

    con.commit()
    con.close()
    return 1, f"[SUCCESS] <{dt.now()}> PlayerName '{args[0]}' has been successfully registered"


def change_player_name(args):
    data = (args[0], args[1])
    if is_player_registered(data) or not is_player_name_unique(args[2]):
        return 0, f"[ERR] <{dt.now()}> An incorrect username or password has been entered or new name already in use",
    data = (args[2], args[0])
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('UPDATE Player SET PlayerName = ? WHERE PlayerName = ?', data)
    con.commit()
    con.close()
    return 1, f"[SUCCESS] <{dt.now()}> PlayerName '{args[0]}' Successfully changed to '{args[2]}'"


def is_player_registered(data):
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('SELECT PlayerName FROM Player WHERE (PlayerName, HashPassword) = (?, ?)', data)
    is_correct = cursor.fetchone()
    con.close()
    return is_correct is None


# Child commands
def is_player_name_unique(player_name):
    con = sqlite3.connect(serv_settings.db_path)
    cursor = con.cursor()
    cursor.execute('SELECT PlayerName FROM Player WHERE PlayerName = ?', (player_name,))
    existing_player = cursor.fetchone()
    con.close()
    return existing_player is None
