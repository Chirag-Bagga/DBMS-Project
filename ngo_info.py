import sqlite3

def get_ngo_info(ngo_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    # Using JOIN to get complete NGO information
    c.execute('''
    SELECT n.name, nc.email, nc.phone, na.street, na.city
    FROM ngos n
    JOIN ngo_contacts nc ON n.ngo_id = nc.ngo_id
    JOIN ngo_addresses na ON n.ngo_id = na.ngo_id
    WHERE n.ngo_id = ?
    ''', (ngo_id,))
    
    result = c.fetchone()
    conn.close()
    
    if result:
        return {
            "name": result[0],
            "email": result[1],
            "phone": result[2],
            "street": result[3],
            "city": result[4]
        }
    return None