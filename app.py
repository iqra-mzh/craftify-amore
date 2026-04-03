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
    
    with st.container():
        st.subheader("1. Total Batch Expenses")
        c1, c2, c3 = st.columns(3)
        # FIXED LINE BELOW:
        raw_mats = c1.number_input("Raw Materials (Entire Batch)", min_value=0.0)
        batch_labor = c2.number_input("Total Labor (Full Batch)", min_value=0.0)
        utilities = c3.number_input("Utilities (Elec/Gas/Rent)", min_value=0.0)
        
        c4, c5 = st.columns(2)
        equip = c4.number_input("Equipment Usage/Depreciation", min_value=0.0)
        bulk_pkg = c5.number_input("Advance Packaging (Full Batch)", min_value=0.0)
        
        total_batch_cost = raw_mats + batch_labor + utilities + equip + bulk_pkg

    st.divider()
    st.subheader("2. Production & Wastage")
    w1, w2 = st.columns(2)
    total_produced = w1.number_input("Total Units Produced", min_value=1)
    wasted_items = w2.number_input("Wasted/Damaged Items", min_value=0)
    
    real_units = total_produced - wasted_items
    if real_units <= 0:
        st.error("Wastage cannot exceed production!")
    else:
        cost_per_unit = total_batch_cost / real_units
        st.info(f"Actual Cost Per Unit: **Rs. {cost_per_unit:.2f}**")

        st.divider()
        st.subheader("3. Market Strategy & Profit")
        p1, p2 = st.columns(2)
        cust_type = p1.selectbox("Customer Type", ["Budget", "Standard", "Premium"])
        bulk_qty = p2.number_input("If customer buys this quantity:", min_value=1)
        
        margin = 25 if cust_type == "Budget" else (50 if cust_type == "Standard" else 100)
        bulk_discount = 0.15 if bulk_qty >= 10 else 0.0
        
        selling_price = cost_per_unit * (1 + margin/100)
        discounted_price = selling_price * (1 - bulk_discount)
        
        st.success(f"Recommended Price: Rs. {discounted_price:.2f} per unit")
        if bulk_discount > 0: st.caption(f"Includes {bulk_discount*100}% Bulk Discount")
# --- 3. TINYWOW SUITE ---
elif tool_choice == "TinyWow Suite (PDF & Media)":
    st.header("🛠️ TinyWow AI Media Suite")
    task = st.selectbox("Select Conversion", ["PDF to Word", "Word to PDF", "PDF to JPG", "JPG to PDF"])
    files = st.file_uploader(f"Upload files for {task}", accept_multiple_files=True)
    if st.button("Process & Download"):
        if files:
            st.balloons()
            st.success(f"Files processed and simulated saving to {DOWNLOADS_DIR}")
        else:
            st.warning("Please upload files first.")

# --- 4. VIDEO CENTER (Deployed Version) ---
elif tool_choice == "Video Center":
    st.header("🎥 Bulk Video Center")
    st.caption("Note: If you get a 'Forbidden' error, try a different video or wait a few minutes.")
    urls_input = st.text_area("Paste Video URLs (one per line):", placeholder="https://youtube.com/...")
    
    # Path for Cookies (Make sure youtube_cookies.txt is uploaded to GitHub)
    cookie_path = "youtube_cookies.txt"

    if st.button("Start Bulk Download"):
        if urls_input:
            urls_list = [u.strip() for u in urls_input.split('\n') if u.strip()]
            
            for url in urls_list:
                try:
                    with st.status(f"Processing: {url}", expanded=True) as status:
                        ydl_opts = {
                            # FORCE single file to avoid merging issues on Cloud
                            'format': 'best[ext=mp4]/best', 
                            'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
                            'noplaylist': True,
                            'nocheckcertificate': True,
                            'quiet': True,
                            # THE BYPASS: Pretend to be a mobile user
                            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                            'referer': 'https://www.google.com/',
                        }
                        
                        # Use cookies if you uploaded them to GitHub
                        if os.path.exists(cookie_path):
                            ydl_opts['cookiefile'] = cookie_path
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(url, download=True)
                            video_filename = ydl.prepare_filename(info)
                        
                        status.update(label="✅ Download Complete!", state="complete")

                    with open(video_filename, "rb") as file:
                        st.download_button(
                            label=f"💾 Save '{info.get('title', 'Video')[:20]}...' to Phone",
                            data=file,
                            file_name=os.path.basename(video_filename),
                            mime="video/mp4",
                            key=f"cloud_dl_{url}"
                        )
                except Exception as e:
                    st.error(f"YouTube Blocked this request: {str(e)}")
                    st.info("Tip: YouTube is very strict with cloud servers. If it fails, try a different link.")
# --- 5. UNIVERSAL CONVERTER ---
elif tool_choice == "Universal Converter":
    st.header("🌍 Universal Exchange & Units")
    mode = st.tabs(["Currency", "Length", "Weight"])
    with mode[0]:
        st.subheader("Currency Exchange")
        amount = st.number_input("Amount", value=1.0)
        st.write("Result: Calculating...")
    # (Rest of converter code remains same)
