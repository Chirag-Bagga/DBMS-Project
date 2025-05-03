import sqlite3

def get_donor_info(donor_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    # Using JOIN to get complete donor information
    c.execute('''
    SELECT d.name, dc.email, dc.phone, da.street, da.city
    FROM donors d
    JOIN donor_contacts dc ON d.donor_id = dc.donor_id
    JOIN donor_addresses da ON d.donor_id = da.donor_id
    WHERE d.donor_id = ?
    ''', (donor_id,))
    
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