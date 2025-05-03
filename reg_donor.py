import sqlite3

def register_donor(user_id, name, email, phone, street, city):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    # Insert into donors table
    c.execute("INSERT INTO donors (user_id, name) VALUES (?, ?)", (user_id, name))
    donor_id = c.lastrowid
    
    # Insert into donor_contacts table
    c.execute("INSERT INTO donor_contacts (donor_id, email, phone) VALUES (?, ?, ?)", 
              (donor_id, email, phone))
    
    # Insert into donor_addresses table
    c.execute("INSERT INTO donor_addresses (donor_id, street, city) VALUES (?, ?, ?)", 
              (donor_id, street, city))
    
    conn.commit()
    conn.close()
    return donor_id