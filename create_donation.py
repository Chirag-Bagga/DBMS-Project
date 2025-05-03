import sqlite3

def create_donation(donor_id, food_type, donation_date, expiry_date, quantity, ngo_id=None):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    c.execute('''
    INSERT INTO food_donations 
    (donor_id, food_type, donation_date, expiry_date, quantity, ngo_id, status) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (donor_id, food_type, donation_date, expiry_date, quantity, ngo_id, 
          'Assigned' if ngo_id else 'Available'))
    
    donation_id = c.lastrowid
    conn.commit()
    conn.close()
    return donation_id