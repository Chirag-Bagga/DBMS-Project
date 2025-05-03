import sqlite3

def get_donor_donations(donor_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    c.execute('''
    SELECT fd.donation_id, fd.food_type, fd.donation_date, fd.expiry_date, 
           fd.quantity, fd.status, COALESCE(n.name, 'None')
    FROM food_donations fd
    LEFT JOIN ngos n ON fd.ngo_id = n.ngo_id
    WHERE fd.donor_id = ?
    ORDER BY fd.donation_date DESC
    ''', (donor_id,))
    
    columns = ['donation_id', 'food_type', 'donation_date', 'expiry_date', 
               'quantity', 'status', 'ngo_name']
    result = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return result