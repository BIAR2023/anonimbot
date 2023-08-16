import sqlite3

#create talk stop
def create_chat_room(chat_id):
    con = sqlite3.connect('sqlite.db')
    cur = con.cursor()

    cur.execute(f"""INSERT INTO chat_room (chat_id1, status) """
                f"""values ('{chat_id}', 'create')""")
    con.commit()
    con.close()


def search_free_chat_rooms():
    con = sqlite3.connect('sqlite.db')
    cur = con.cursor()
    res = cur.execute("""SELECT * FROM chat_room where status = 'create'""").fetchall()
    con.close()
    return res


def start_chat_room(id1, chat_id2):
    print(id1)
    print(chat_id2)
    con = sqlite3.connect('sqlite.db')
    cur = con.cursor()
    print(chat_id2)
    cur.execute(f"""UPDATE chat_room SET (chat_id2, status) = ('{chat_id2}', 'talk') where id = {id1}""")
    con.commit()
    con.close()


def search_current_chat_room(chat_id):
    con = sqlite3.connect('sqlite.db')
    cur = con.cursor()
    res = cur.execute(f"""SELECT * FROM chat_room where (chat_id1 = '{chat_id}' or chat_id2 = '{chat_id}') 
and status = 'talk'""").fetchall()
    con.close()
    return res


def end_chat(chat_id):
    chat = search_current_chat_room(chat_id)
    con = sqlite3.connect('sqlite.db')
    cur = con.cursor()
    cur.execute(f"""UPDATE chat_room SET status = 'end' where id = {chat[0][0]}""")
    con.commit()
    con.close()
    if chat_id != chat[0][1]:
        return chat[0][1]
    return chat[0][2]






