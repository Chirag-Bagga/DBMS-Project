import sqlite3

def get_ngo_requests(ngo_id):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    c.execute('''
    SELECT request_id, food_type, quantity, request_date, status
    FROM requests
    WHERE ngo_id = ?
    ORDER BY request_date DESC
    ''', (ngo_id,))
    
    columns = ['request_id', 'food_type', 'quantity', 'request_date', 'status']
    result = [dict(zip(columns, row)) for row in c.fetchall()]
    conn.close()
    return result