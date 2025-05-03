import sqlite3
from hashing import hash_password

def authenticate(username, password):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    c.execute(
        "SELECT user_id, user_type FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password))
    )
    result = c.fetchone()
    conn.close()
    
    if result:
        return {"user_id": result[0], "user_type": result[1]}
    return None