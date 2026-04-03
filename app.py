import streamlit as st
import pandas as pd
import os
import yt_dlp

# --- G: DRIVE PATH SETUP ---
# We use a fallback so it works on your PC and doesn't break on the web
BASE_DIR = r"G:\Craftify_Studio" if os.path.exists(r"G:") else os.getcwd()
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

# --- PAGE CONFIG ---
st.set_page_config(page_title="Craftify Amore Studio", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #ffb7c5; color: white; border: none; }
    .header-style { text-align: center; color: #2c3e50; font-family: 'Helvetica'; margin-top: -20px;}
    .slogan-style { text-align: center; color: #ffb7c5; font-size: 14px; letter-spacing: 2px; margin-bottom: 0px;}
    .metric-box { padding: 15px; border-radius: 10px; background-color: #fff0f3; border: 1px solid #ffb7c5; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'site_title' not in st.session_state:
    st.session_state['site_title'] = "CRAFTIFY AMORE"
if 'site_slogan' not in st.session_state:
    st.session_state['site_slogan'] = "HANDMADE TREASURES"

# --- SIDEBAR ---
with st.sidebar:
    st.caption("📍 Digital Utility Suite")
    with st.expander("🔐 Admin Login"):
        admin_key = st.text_input("Enter Admin Key:", type="password")
        if admin_key == "axiom123":
            st.success("Admin Mode Active")
            st.session_state['site_title'] = st.text_input("Edit Title:", st.session_state['site_title'])
            st.session_state['site_slogan'] = st.text_input("Edit Slogan:", st.session_state['site_slogan'])
        elif admin_key:
            st.error("Incorrect Key")

    st.divider()
    tool_choice = st.selectbox("Select Tool:", 
        ["Individual Pricing", "Bulk/Batch Pricing", "TinyWow Suite (PDF & Media)", "Video Center", "Universal Converter"])
    
    st.info(f"System Path: {BASE_DIR}")

# --- HEADER ---
st.markdown(f"<p class='slogan-style'>{st.session_state['site_slogan']}</p>", unsafe_allow_html=True)
st.markdown(f"<h1 class='header-style'>{st.session_state['site_title']}</h1>", unsafe_allow_html=True)
st.divider()

# --- 1. INDIVIDUAL PRICING ---
if tool_choice == "Individual Pricing":
    st.header("💎 Individual Item Costing")
    col1, col2 = st.columns(2)
    with col1:
        mats = st.number_input("Materials (Direct)", min_value=0.0)
        labor = st.number_input("Labor (Hours)", min_value=0.0)
        rate = st.number_input("Hourly Rate (PKR)", min_value=0)
    with col2:
        packaging = st.number_input("Packaging Cost", min_value=0.0)
        profit_margin = st.slider("Profit Margin %", 0, 200, 30)
    
    base_cost = mats + (labor * rate) + packaging
    final_price = base_cost * (1 + profit_margin/100)
    
    st.markdown(f"""
    <div class='metric-box'>
        <h3 style='text-align: center; color: #2c3e50;'>Suggested Selling Price</h3>
        <h1 style='text-align: center; color: #ffb7c5;'>Rs. {final_price:.2f}</h1>
    </div>
    """, unsafe_allow_html=True)

# --- 2. BULK / BATCH PRICING ---
elif tool_choice == "Bulk/Batch Pricing":
    st.header("📦 Bulk Batch Calculator")
    # ... (Rest of your Bulk Pricing code remains the same)
    with st.container():
        st.subheader("1. Total Batch Expenses")
        c1, c2, c3 = st.columns(3)
        raw_mats = c1.number_input("Raw Materials (Entire Batch)", min
