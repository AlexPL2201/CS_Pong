import sqlite3


def create_db():
    con = sqlite3.connect("db.db")
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Player
                    (PlayerID INTEGER PRIMARY KEY AUTOINCREMENT,  
                    PlayerName TEXT, 
                    HashPassword TEXT,
                    Score INTEGER,
                    TotalGamesPlayed INTEGER,
                    TotalGamesWon INTEGER,
                    RegistrationDate DATE)
                """)
    con.commit()
    con.close()


if __name__ == '__main__':
    create_db()
