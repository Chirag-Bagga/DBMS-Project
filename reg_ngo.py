import sqlite3

def register_ngo(user_id, name, email, phone, street, city):
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    # Insert into ngos table
    c.execute("INSERT INTO ngos (user_id, name) VALUES (?, ?)", (user_id, name))
    ngo_id = c.lastrowid
    
    # Insert into ngo_contacts table
    c.execute("INSERT INTO ngo_contacts (ngo_id, email, phone) VALUES (?, ?, ?)", 
              (ngo_id, email, phone))
    
    # Insert into ngo_addresses table
    c.execute("INSERT INTO ngo_addresses (ngo_id, street, city) VALUES (?, ?, ?)", 
              (ngo_id, street, city))
    
    conn.commit()
    conn.close()
    return ngo_id