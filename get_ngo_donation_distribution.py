import sqlite3

def get_ngo_donation_distribution():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    # Using JOIN and GROUP BY together
    c.execute('''
    SELECT 
        n.name as ngo_name,
        COUNT(fd.donation_id) as donations_received,
        SUM(fd.quantity) as total_quantity
    FROM ngos n
    JOIN food_donations fd ON n.ngo_id = fd.ngo_id
    GROUP BY n.ngo_id
    ORDER BY total_quantity DESC
    ''')
    
    columns = ['ngo_name', 'donations_received', 'total_quantity']
    result = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return result
