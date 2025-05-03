import streamlit as st
import sqlite3
import hashlib
import datetime
import pandas as pd
from PIL import Image
import os
import time
import base64
from io import BytesIO

def init_db():
    conn = sqlite3.connect('food_waste_management.db')
    c = conn.cursor()
    
    # Create tables in 3NF
    
    # Users table to store authentication data
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        user_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Donors table - normalized to store donor details
    c.execute('''
    CREATE TABLE IF NOT EXISTS donors (
        donor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    
    # Donor_contacts table - normalized to store contact information
    c.execute('''
    CREATE TABLE IF NOT EXISTS donor_contacts (
        contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER NOT NULL,
        email TEXT,
        phone TEXT,
        FOREIGN KEY (donor_id) REFERENCES donors(donor_id)
    )
    ''')
    
    # Donor_addresses table - normalized to store address information
    c.execute('''
    CREATE TABLE IF NOT EXISTS donor_addresses (
        address_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER NOT NULL,
        street TEXT,
        city TEXT,
        FOREIGN KEY (donor_id) REFERENCES donors(donor_id)
    )
    ''')
    
    # NGOs table - normalized to store NGO details
    c.execute('''
    CREATE TABLE IF NOT EXISTS ngos (
        ngo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')
    
    # NGO_contacts table - normalized to store contact information
    c.execute('''
    CREATE TABLE IF NOT EXISTS ngo_contacts (
        contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ngo_id INTEGER NOT NULL,
        email TEXT,
        phone TEXT,
        FOREIGN KEY (ngo_id) REFERENCES ngos(ngo_id)
    )
    ''')
    
    # NGO_addresses table - normalized to store address information
    c.execute('''
    CREATE TABLE IF NOT EXISTS ngo_addresses (
        address_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ngo_id INTEGER NOT NULL,
        street TEXT,
        city TEXT,
        FOREIGN KEY (ngo_id) REFERENCES ngos(ngo_id)
    )
    ''')
    
    # Food_donations table
    c.execute('''
    CREATE TABLE IF NOT EXISTS food_donations (
        donation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_id INTEGER NOT NULL,
        ngo_id INTEGER,
        food_type TEXT NOT NULL,
        donation_date DATE NOT NULL,
        expiry_date DATE NOT NULL,
        quantity REAL NOT NULL,
        status TEXT DEFAULT 'Available',
        FOREIGN KEY (donor_id) REFERENCES donors(donor_id),
        FOREIGN KEY (ngo_id) REFERENCES ngos(ngo_id)
    )
    ''')
    
    # Requests table
    c.execute('''
    CREATE TABLE IF NOT EXISTS requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        ngo_id INTEGER NOT NULL,
        food_type TEXT NOT NULL,
        quantity REAL NOT NULL,
        request_date DATE NOT NULL,
        status TEXT DEFAULT 'Pending',
        FOREIGN KEY (ngo_id) REFERENCES ngos(ngo_id)
    )
    ''')
    
    # Request_donations mapping table (for many-to-many relationship)
    c.execute('''
    CREATE TABLE IF NOT EXISTS request_donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id INTEGER NOT NULL,
        donation_id INTEGER NOT NULL,
        FOREIGN KEY (request_id) REFERENCES requests(request_id),
        FOREIGN KEY (donation_id) REFERENCES food_donations(donation_id)
    )
    ''')
    
    # Create stored procedure using SQLite's CREATE TRIGGER syntax
    # This trigger will update the status of a food donation when it's assigned to an NGO
    c.execute('''
    CREATE TRIGGER IF NOT EXISTS update_donation_status
    AFTER UPDATE OF ngo_id ON food_donations
    FOR EACH ROW
    WHEN NEW.ngo_id IS NOT NULL
    BEGIN
        UPDATE food_donations SET status = 'Assigned' WHERE donation_id = NEW.donation_id;
    END;
    ''')
    
    # Trigger to update request status when all donations are assigned
    c.execute('''
    CREATE TRIGGER IF NOT EXISTS update_request_status
    AFTER INSERT ON request_donations
    BEGIN
        UPDATE requests 
        SET status = 'Fulfilled' 
        WHERE request_id = NEW.request_id 
        AND (SELECT COUNT(*) FROM request_donations WHERE request_id = NEW.request_id) > 0;
    END;
    ''')
    
    conn.commit()
    conn.close()
