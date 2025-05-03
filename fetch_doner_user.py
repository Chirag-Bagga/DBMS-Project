import sqlite3

def get_donor_id_by_user_id(user_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    c.execute("SELECT donor_id FROM donors WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return result[0]
    return None