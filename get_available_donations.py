import sqlite3
import datetime

def get_available_donations(ngo_id=None):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    query = '''
    SELECT fd.donation_id, d.name as donor_name, fd.food_type, 
           fd.donation_date, fd.expiry_date, fd.quantity
    FROM food_donations fd
    JOIN donors d ON fd.donor_id = d.donor_id
    WHERE fd.status = 'Available'
    AND fd.expiry_date >= ?
    '''
    
    params = [datetime.date.today().isoformat()]
    
    # If ngo_id is specified, exclude donations already assigned to this NGO
    if ngo_id:
        query += "AND fd.ngo_id IS NULL OR fd.ngo_id = ?"
        params.append(ngo_id)
    
    query += "ORDER BY fd.expiry_date ASC"
    
    c.execute(query, params)
    
    columns = ['donation_id', 'donor_name', 'food_type', 'donation_date', 
               'expiry_date', 'quantity']
    result = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return result