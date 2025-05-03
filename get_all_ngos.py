import sqlite3

def get_all_ngos():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    c.execute("SELECT ngo_id, name FROM ngos ORDER BY name")
    result = c.fetchall()
    conn.close()
    
    return [(row[0], row[1]) for row in result]