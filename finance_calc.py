import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Suzuki Swift Finance Lab", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- CONSTANTS FROM YOUR QUOTES ---
CASH_PRICE = 22049.00  # [cite: 17, 54]
MONTHLY_PAYMENT = 200.00 # [cite: 14, 53]
TERM_MONTHS = 48 # Number of regular payments 
BASE_MILEAGE = 12000 # [cite: 13]
BASE_GFV = 8984.00 # 
# Calculated depreciation: (£8,984 - £8,315) / (3,000 miles) = £0.223/mile 
DEPRECIATION_RATE = 0.223 

st.title("🚗 Suzuki Swift Finance Lab")
st.markdown("Experiment with mileage and track how the deposit shifts to maintain **£200/month** at **0% APR**.")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Configure Quote")
    mileage = st.slider("Annual Mileage", 5000, 25000, 12000, step=500)
    
    # Calculation Logic
    mileage_diff = mileage - BASE_MILEAGE
    est_gfv = BASE_GFV - (mileage_diff * DEPRECIATION_RATE)
    total_monthly = MONTHLY_PAYMENT * TERM_MONTHS
    req_deposit = CASH_PRICE - total_monthly - est_gfv
    
    if st.button("➕ Add to History"):
        new_entry = {
            "Mileage": f"{mileage:,}",
            "Deposit": f"£{req_deposit:,.2f}",
            "Final Payment (GFV)": f"£{est_gfv:,.2f}",
            "Monthly": f"£{MONTHLY_PAYMENT}",
            "Total Payable": f"£{CASH_PRICE:,.2f}"
        }
        st.session_state.history.append(new_entry)
        st.success("Added to history!")

# --- MAIN DISPLAY ---
col1, col2, col3 = st.columns(3)
col1.metric("Required Deposit", f"£{req_deposit:,.2f}")
col2.metric("Final Payment (GFV)", f"£{est_gfv:,.2f}")
col3.metric("Total Interest", "0.0%")

# --- HISTORY SECTION ---
st.divider()
st.subheader("📜 Calculation History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.table(df) # Display the history table
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("No history yet. Adjust the slider and click 'Add to History' to compare options.")

# --- TECHNICAL FOOTNOTE ---
with st.expander("See the Math"):
    st.write("Since the interest rate is **0.0%** , the total amount payable is always exactly the cash price[cite: 17, 54].")
    st.latex(r"Cash Price (£22,049) = Deposit + (48 \times £200) + GFV")
    st.write("When mileage increases, the GFV (resale value) decreases. To keep the equation balanced without changing the £200 monthly payment, the Deposit must increase by the exact amount the GFV dropped.")
