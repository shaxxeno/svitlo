import sqlite3

conn = sqlite3.connect('db/database', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(user_id: int, address: str):
    cursor.execute('INSERT INTO user_info (user_id, address) VALUES (?, ?)', (user_id, address))
    conn.commit()

def get_address(user_id: int):
    cursor.execute("SELECT address FROM user_info WHERE user_id = ?", (user_id, ))
    result = cursor.fetchone()
    if result:
        return result[0]

def update_address(user_id: int, updated_address: str):
    cursor.execute('UPDATE user_info SET address= ? WHERE user_id = ?', (updated_address, user_id))
