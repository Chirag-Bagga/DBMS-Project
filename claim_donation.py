import sqlite3

def claim_donation(donation_id, ngo_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    c.execute('''
    UPDATE food_donations
    SET ngo_id = ?, status = 'Assigned'
    WHERE donation_id = ? AND (status = 'Available' OR ngo_id = ?)
    ''', (ngo_id, donation_id, ngo_id))
    
    success = c.rowcount > 0
    conn.commit()
    conn.close()
    return success
