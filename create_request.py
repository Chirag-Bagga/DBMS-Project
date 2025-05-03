import sqlite3
import datetime

def create_request(ngo_id, food_type, quantity):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    request_date = datetime.date.today().isoformat()
    
    c.execute('''
    INSERT INTO requests (ngo_id, food_type, quantity, request_date, status) 
    VALUES (?, ?, ?, ?, 'Pending')
    ''', (ngo_id, food_type, quantity, request_date))
    
    request_id = c.lastrowid
    conn.commit()
    conn.close()
    return request_id