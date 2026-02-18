from package import *
import config_

class User:
    def __init__(self, id:int, name:str, count:int, description:str):
        self.id = id
        self.name = name
        self.description = description
        self.count = count

db_local = local()

def get_connection():
    if not hasattr(db_local, 'conn'):
        db_local.conn = sqlite3.connect('./data/user.db', check_same_thread=True)
    return db_local.conn

def close_connection():
    if hasattr(db_local, 'conn'):
        db_local.conn.close()
        del db_local.conn

if not os.path.exists("./data"):
    os.mkdir("./data")
if not os.path.exists("./data/user.db"):
    user_db = sqlite3.connect("./data/user.db")
    db_cur = user_db.cursor()
    db_cur.execute('''CREATE TABLE USERDATA
        (ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERID           TEXT    NOT NULL,
        COUNT           INT     NOT NULL,
        DESCRIPTION     TEXT    NOT NULL
                   );''')
    user_db.commit()
    db_cur.close()
    user_db.close()

def give_user(uid:str):
    conn = get_connection()
    db_cur = conn.cursor()
    db_cur.execute("SELECT COUNT FROM USERDATA WHERE USERID = ?", (uid,))
    res = db_cur.fetchone()
    if res is None:
        return -1
    db_cur.execute("UPDATE USERDATA SET COUNT = COUNT + 1 WHERE USERID = ?", (uid,))
    conn.commit()
    return 0

def get_user_count(uid:str) -> int:
    conn = get_connection()
    db_cur = conn.cursor()
    db_cur.execute("SELECT COUNT FROM USERDATA WHERE USERID = ?", (uid,))
    res = db_cur.fetchone()
    if res is None:
        return -1
    return res[0]

def get_all_users() -> list:
    conn = get_connection()
    db_cur = conn.cursor()
    db_cur.execute("SELECT * FROM USERDATA")
    res = db_cur.fetchall()
    users = []
    for r in res:
        users.append(User(r[0], r[1], r[2], r[3]))
    return users

def add_user(uid:str, description:str, password:str) -> bool:
    if password != config_.KEY_ADMIN:
        return False
    conn = get_connection()
    db_cur = conn.cursor()
    db_cur.execute("SELECT COUNT FROM USERDATA WHERE USERID = ?", (uid,))
    res = db_cur.fetchone()
    if res is not None:
        return False
    db_cur.execute("INSERT INTO USERDATA (USERID, COUNT, DESCRIPTION) VALUES (?, ?, ?)", (uid, 0, description))
    conn.commit()
    return True

def delete_user(uid:str, password:str):
    if password != config_.KEY_ADMIN:
        return False
    conn = get_connection()
    db_cur = conn.cursor()
    db_cur.execute("DELETE FROM USERDATA WHERE USERID = ?", (uid,))
    conn.commit()
    return

def update_user(uid:str, name_new:str, count:int, description:str, password:str):
    if password != config_.KEY_ADMIN:
        return False
    conn = get_connection()
    db_cur = conn.cursor()
    db_cur.execute("UPDATE USERDATA SET USERID = ?, COUNT = ?, DESCRIPTION = ? WHERE USERID = ?", (name_new, count, description, uid))
    conn.commit()
    return