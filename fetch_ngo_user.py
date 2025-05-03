import sqlite3

def get_ngo_id_by_user_id(user_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    c.execute("SELECT ngo_id FROM ngos WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return None