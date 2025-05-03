import sqlite3
from hashing import hash_password

def register_user(username, password, user_type):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    try:
        # Insert into users table
        c.execute(
            "INSERT INTO users (username, password_hash, user_type) VALUES (?, ?, ?)",
            (username, hash_password(password), user_type)
        )
        user_id = c.lastrowid
        
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None