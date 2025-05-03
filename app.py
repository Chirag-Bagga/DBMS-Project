import streamlit as st
import datetime
import time
import pandas as pd
from create_tables import init_db
from authentication import authenticate
from fetch_doner_user import get_donor_id_by_user_id
from fetch_ngo_user import get_ngo_id_by_user_id
from reg_user import register_user
from reg_donor import register_donor
from reg_ngo import register_ngo
from doner_info import get_donor_info
from get_all_ngos import get_all_ngos
from create_donation import create_donation
from get_donor_donations import get_donor_donations
from get_donation_statistics import get_donation_statistics
from get_top_donors import get_top_donors
from ngo_info import get_ngo_info
from get_available_donations import get_available_donations
from claim_donation import claim_donation
from get_ngo_request import get_ngo_requests
from create_request import create_request
from get_donation_trends import get_donation_trends
from get_donation_statistics import get_donation_statistics
from get_ngo_donation_distribution import get_ngo_donation_distribution

def main():
    # Initialize the database
    init_db()
    
    # Set page configuration and custom CSS
    st.set_page_config(
        page_title="Food Waste Management System",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Updated CSS with input field fixes
    st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stTextInput > div > div > input {
        color: white !important;
        border-radius: 5px;
    }
    .stTextInput input::placeholder {
        color: white !important;
        opacity: 1 !important;
    }
    .st-eb {
        border-radius: 5px;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    label {
        color: #1E3A8A !important;
        font-weight: bold !important;
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        color: black;
    }
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        color: black;
    }
    .success-message {
        background-color: #D5F5E3;
        color: #196F3D;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-message {
        background-color: #FADBD8;
        color: #943126;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-message {
        background-color: #D6EAF8;
        color: #21618C;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .dashboard-stats {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
    }
    .stat-card {
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
        min-width: 200px;
        flex: 1;
        margin-right: 10px;
        color: black;
    }
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 16px;
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #f0f2f6;
        color: #1E88E5;
    }
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: black;
    }
    .stTabs [aria-selected="true"]:hover {
        background-color: #1a73e8;
    }
    div[data-testid="stNotification"] div[data-testid="stMarkdownContainer"] p {
    color: #1E3A8A !important;
    }
    div[data-testid="stNotification"] {
        background-color: #D6EAF8 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Session state initialization
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    if 'entity_id' not in st.session_state:
        st.session_state.entity_id = None
    
    # Navigation based on authentication state
    if not st.session_state.authenticated:
        show_login_page()
    else:
        if st.session_state.user_type == 'Donor':
            show_donor_dashboard()
        elif st.session_state.user_type == 'NGO':
            show_ngo_dashboard()

def show_login_page():
    st.title("Food Waste Management System")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="card">
        <h2>Welcome to the Food Waste Management System</h2>
        <p>Our platform connects food donors with NGOs to reduce food waste and help those in need.</p>
        <ul>
            <li>Donors can contribute excess food</li>  
            <li>NGOs can request and receive food donations</li>
            <li>Track donations and requests in real-time</li>
            <li>Make a positive impact on the environment and society</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-message">
        Please login or sign up to start using the platform.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            st.subheader("Login")
            login_username = st.text_input("Username", key="login_username")
            login_password = st.text_input("Password", type="password", key="login_password")
            
            login_col1, login_col2 = st.columns([1, 1])
            with login_col1:
                if st.button("Login", key="login_button"):
                    if login_username and login_password:
                        user = authenticate(login_username, login_password)
                        if user:
                            st.session_state.authenticated = True
                            st.session_state.user_id = user["user_id"]
                            st.session_state.user_type = user["user_type"]
                            
                            if user["user_type"] == "Donor":
                                st.session_state.entity_id = get_donor_id_by_user_id(user["user_id"])
                            else:
                                st.session_state.entity_id = get_ngo_id_by_user_id(user["user_id"])
                            
                            st.success(f"Welcome back! You're logged in as a {user['user_type']}.")
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")
                    else:
                        st.warning("Please enter both username and password.")
        
        with tab2:
            st.subheader("Sign Up")
            signup_username = st.text_input("Username", key="signup_username")
            signup_password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            user_type = st.selectbox("I am a", ["Donor", "NGO"])
            
            name = st.text_input("Name (Individual/Organization)")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            
            col1, col2 = st.columns(2)
            with col1:
                street = st.text_input("Street Address")
            with col2:
                city = st.text_input("City")
            
            if st.button("Sign Up"):
                if signup_password != confirm_password:
                    st.error("Passwords do not match.")
                elif not (signup_username and signup_password and name and email and phone and street and city):
                    st.warning("Please fill in all fields.")
                else:
                    user_id = register_user(signup_username, signup_password, user_type)
                    
                    if user_id:
                        if user_type == "Donor":
                            entity_id = register_donor(user_id, name, email, phone, street, city)
                            st.session_state.entity_id = entity_id
                        else:  # NGO
                            entity_id = register_ngo(user_id, name, email, phone, street, city)
                            st.session_state.entity_id = entity_id
                        
                        st.session_state.authenticated = True
                        st.session_state.user_id = user_id
                        st.session_state.user_type = user_type
                        
                        st.success("Account created successfully!")
                        st.rerun()
                    else:
                        st.error("Username already exists. Please choose a different username.")

def show_donor_dashboard():
    st.title("Donor Dashboard")
    
    # Get donor information
    donor_info = get_donor_info(st.session_state.entity_id)
    
    # Sidebar with donor info and logout button
    with st.sidebar:
        st.header(f"Welcome, {donor_info['name']}")
        st.write(f"📧 {donor_info['email']}")
        st.write(f"📱 {donor_info['phone']}")
        st.write(f"📍 {donor_info['street']}, {donor_info['city']}")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_type = None
            st.session_state.entity_id = None
            st.rerun()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["Donate Food", "My Donations", "Analytics"])
    
    with tab1:
        st.header("Donate Food")
        
        st.markdown("""
        <div class="highlight">
        Help reduce food waste by donating your excess food to those in need.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            food_type = st.text_input("Food Type (e.g., Fruits, Vegetables, Prepared Meals)")
            quantity = st.number_input("Quantity (kg)", min_value=0.1, step=0.1)
            
        with col2:
            donation_date = st.date_input("Donation Date", datetime.date.today())
            expiry_date = st.date_input("Expiry Date", datetime.date.today() + datetime.timedelta(days=3))
        
        # Get list of all NGOs
        ngos = get_all_ngos()
        ngo_options = [("", "Select an NGO (Optional)")] + ngos
        selected_ngo = st.selectbox("Donate to specific NGO", ngo_options, format_func=lambda x: x[1] if x else "Select an NGO (Optional)")
        
        if st.button("Submit Donation"):
            if food_type and quantity > 0 and donation_date and expiry_date:
                if expiry_date < donation_date:
                    st.error("Expiry date cannot be before donation date.")
                else:
                    ngo_id = selected_ngo[0] if selected_ngo and selected_ngo[0] != "" else None
                    
                    donation_id = create_donation(
                        st.session_state.entity_id,
                        food_type,
                        donation_date.isoformat(),
                        expiry_date.isoformat(),
                        quantity,
                        ngo_id
                    )
                    
                    if donation_id:
                        st.success("Donation submitted successfully! Thank you for your contribution.")
                    else:
                        st.error("Failed to submit donation. Please try again.")
            else:
                st.warning("Please fill in all required fields.")
    
    with tab2:
        st.header("My Donations")
        
        donations = get_donor_donations(st.session_state.entity_id)
        
        if not donations:
            st.info("You haven't made any donations yet.")
        else:
            df = pd.DataFrame(donations)
            
            # Format DataFrame
            df['donation_date'] = pd.to_datetime(df['donation_date']).dt.strftime('%b %d, %Y')
            df['expiry_date'] = pd.to_datetime(df['expiry_date']).dt.strftime('%b %d, %Y')
            df['quantity'] = df['quantity'].apply(lambda x: f"{x} kg")
            
            st.dataframe(
                df.rename(columns={
                    'donation_id': 'ID',
                    'food_type': 'Food Type',
                    'donation_date': 'Donation Date',
                    'expiry_date': 'Expiry Date',
                    'quantity': 'Quantity',
                    'status': 'Status',
                    'ngo_name': 'NGO'
                }),
                use_container_width=True
            )
    
    with tab3:
        st.header("Donation Analytics")
        
        # Get analytics data
        donation_stats = get_donation_statistics()
        top_donors = get_top_donors()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Food Type Distribution")
            if donation_stats:
                chart_data = pd.DataFrame(donation_stats)
                chart_data = chart_data[['food_type', 'total_quantity']]
                st.bar_chart(chart_data.set_index('food_type'))
            else:
                st.info("No donation data available for analytics.")
        
        with col2:
            st.subheader("Your Contribution")
            donor_donations = get_donor_donations(st.session_state.entity_id)
            
            # Calculate total quantity donated by the current donor
            total_donated = sum(float(d['quantity']) for d in donor_donations) if donor_donations else 0
            
            st.markdown(f"""
            <div class="stat-card">
                <h3>Total Donations</h3>
                <p style="font-size: 24px; font-weight: bold;">{len(donor_donations)}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stat-card">
                <h3>Total Quantity</h3>
                <p style="font-size: 24px; font-weight: bold;">{total_donated:.2f} kg</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.subheader("Top Donors")
        if top_donors:
            top_donors_df = pd.DataFrame(top_donors)
            top_donors_df['total_donated'] = top_donors_df['total_donated'].apply(lambda x: f"{x:.2f} kg")
            
            st.dataframe(
                top_donors_df.rename(columns={
                    'donor_name': 'Donor',
                    'donation_count': 'Donations',
                    'total_donated': 'Total Donated'
                }),
                use_container_width=True
            )
        else:
            st.info("No donor data available for ranking.")

def show_ngo_dashboard():
    st.title("NGO Dashboard")
    
    # Get NGO information
    ngo_info = get_ngo_info(st.session_state.entity_id)
    
    # Sidebar with NGO info and logout button
    with st.sidebar:
        st.header(f"Welcome, {ngo_info['name']}")
        st.write(f"📧 {ngo_info['email']}")
        st.write(f"📱 {ngo_info['phone']}")
        st.write(f"📍 {ngo_info['street']}, {ngo_info['city']}")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_type = None
            st.session_state.entity_id = None
            st.rerun()
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["Available Donations", "My Requests", "Make Request", "Analytics"])
    
    with tab1:
        st.header("Available Food Donations")
        
        st.markdown("""
        <div class="highlight">
        Browse available food donations and claim them for your organization.
        </div>
        """, unsafe_allow_html=True)
        
        available_donations = get_available_donations(st.session_state.entity_id)
        
        if not available_donations:
            st.info("No available donations at the moment. Please check back later.")
        else:
            for i, donation in enumerate(available_donations):
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{donation['food_type']}</h3>
                        <p><strong>Donor:</strong> {donation['donor_name']}</p>
                        <p><strong>Quantity:</strong> {donation['quantity']} kg</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="card">
                        <p><strong>Donated:</strong> {donation['donation_date']}</p>
                        <p><strong>Expires:</strong> {donation['expiry_date']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if st.button("Claim", key=f"claim_{donation['donation_id']}"):
                        if claim_donation(donation['donation_id'], st.session_state.entity_id):
                            st.success("Donation claimed successfully!")
                            time.sleep(1)  # Short delay for UI feedback
                            st.rerun()
                        else:
                            st.error("Failed to claim donation. It may have been claimed by another NGO.")
    
    with tab2:
        st.header("My Requests")
        
        requests = get_ngo_requests(st.session_state.entity_id)
        
        if not requests:
            st.info("You haven't made any requests yet.")
        else:
            for request in requests:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <h3>{request['food_type']}</h3>
                        <p><strong>Quantity:</strong> {request['quantity']} kg</p>
                        <p><strong>Date:</strong> {request['request_date']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    status_color = {
                        "Pending": "#FFB74D",  # Orange
                        "Fulfilled": "#81C784",  # Green
                        "Cancelled": "#E57373"  # Red
                    }.get(request['status'], "#64B5F6")  # Default blue
                    
                    st.markdown(f"""
                    <div class="card">
                        <p style="background-color: {status_color}; padding: 10px; border-radius: 5px; text-align: center; color: white;">
                            <strong>{request['status']}</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.header("Make Food Request")
        
        st.markdown("""
        <div class="highlight">
        Submit a request for the type of food your organization needs.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            request_food_type = st.text_input("Food Type Needed")
        
        with col2:
            request_quantity = st.number_input("Quantity Needed (kg)", min_value=0.1, step=0.1)
        
        if st.button("Submit Request"):
            if request_food_type and request_quantity > 0:
                request_id = create_request(
                    st.session_state.entity_id,
                    request_food_type,
                    request_quantity
                )
                
                if request_id:
                    st.success("Request submitted successfully! We will try to match you with available donations.")
                else:
                    st.error("Failed to submit request. Please try again.")
            else:
                st.warning("Please fill in all required fields.")
    
    with tab4:
        st.header("Donation Analytics")
        
        # Get analytics data
        donation_trends = get_donation_trends()
        ngo_distribution = get_ngo_donation_distribution()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Monthly Donation Trends")
            if donation_trends:
                trend_data = pd.DataFrame(donation_trends)
                st.line_chart(trend_data.set_index('month')['total_quantity'])
            else:
                st.info("No trend data available.")
        
        with col2:
            st.subheader("NGO Distribution")
            if ngo_distribution:
                ngo_data = pd.DataFrame(ngo_distribution)
                st.bar_chart(ngo_data.set_index('ngo_name')['total_quantity'])
            else:
                st.info("No NGO distribution data available.")
        
        # Highlight current NGO's statistics
        if ngo_distribution:
            current_ngo_stats = next((item for item in ngo_distribution if item['ngo_name'] == ngo_info['name']), None)
            
            if current_ngo_stats:
                st.markdown(f"""
                <div class="dashboard-stats">
                    <div class="stat-card">
                        <h3>Your Donations Received</h3>
                        <p style="font-size: 24px; font-weight: bold;">{current_ngo_stats['donations_received']}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Total Food Received</h3>
                        <p style="font-size: 24px; font-weight: bold;">{current_ngo_stats['total_quantity']:.2f} kg</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Your organization hasn't received any donations yet.")


if __name__=="__main__":
    main()