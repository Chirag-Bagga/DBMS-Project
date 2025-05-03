import sqlite3

def get_top_donors():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    c.execute('''
    SELECT 
        d.name as donor_name,
        COUNT(fd.donation_id) as donation_count,
        SUM(fd.quantity) as total_donated
    FROM donors d
    JOIN food_donations fd ON d.donor_id = fd.donor_id
    GROUP BY d.donor_id
    ORDER BY total_donated DESC
    LIMIT 10
    ''')
    
    columns = ['donor_name', 'donation_count', 'total_donated']
    result = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return result