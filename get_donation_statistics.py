import sqlite3

def get_donation_statistics():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    # Using GROUP BY for analytics
    c.execute('''
    SELECT 
        food_type, 
        COUNT(donation_id) as total_donations,
        SUM(quantity) as total_quantity,
        AVG(quantity) as avg_quantity,
        MIN(donation_date) as first_donation,
        MAX(donation_date) as last_donation
    FROM food_donations
    GROUP BY food_type
    ORDER BY total_quantity DESC
    ''')
    
    columns = ['food_type', 'total_donations', 'total_quantity', 
               'avg_quantity', 'first_donation', 'last_donation']
    result = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return result