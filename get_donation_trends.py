import sqlite3

def get_donation_trends():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    # Using subquery for complex analytics
    c.execute('''
    SELECT 
        strftime('%Y-%m', donation_date) as month,
        COUNT(donation_id) as donation_count,
        SUM(quantity) as total_quantity,
        (SELECT COUNT(DISTINCT donor_id) 
         FROM food_donations fd2 
         WHERE strftime('%Y-%m', fd2.donation_date) = strftime('%Y-%m', fd.donation_date)
        ) as active_donors
    FROM food_donations fd
    WHERE donation_date >= date('now', '-12 months')
    GROUP BY month
    ORDER BY month
    ''')
    
    columns = ['month', 'donation_count', 'total_quantity', 'active_donors']
    result = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return result