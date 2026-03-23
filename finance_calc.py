import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Suzuki Swift Finance Lab v2", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- CONSTANTS FROM YOUR QUOTES ---
CASH_PRICE = 22049.00  # 
TERM_MONTHS = 48       # 48 monthly payments + 1 final 
BASE_MILEAGE = 12000   # [cite: 13]
BASE_GFV = 8984.00     # GFV at 12k miles [cite: 15]
# Calculated depreciation: (£8,984 - £8,315) / (3,000 miles) = £0.223/mile 
DEPRECIATION_RATE = 0.223 

st.title("🚗 Suzuki Swift Finance Lab v2")
st.markdown("Now tracking how both **Mileage** and **Monthly Payments** impact your **Deposit**.")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("Configure Your Deal")
    
    # NEW: Editable Monthly Payment
    monthly_in = st.number_input("Monthly Payment (£)", min_value=100, max_value=500, value=200, step=10)
    
    # Mileage Slider
    mileage_in = st.slider("Annual Mileage", 5000, 25000, 12000, step=500)
    
    # --- CALCULATION LOGIC ---
    # 1. Calculate GFV based on mileage
    mileage_diff = mileage_in - BASE_MILEAGE
    est_gfv = BASE_GFV - (mileage_diff * DEPRECIATION_RATE)
    
    # 2. Total amount paid via monthly installments
    total_monthly_paid = monthly_in * TERM_MONTHS
    
    # 3. Solve for Deposit (0% APR Logic)
    # Deposit = Cash Price - Total Monthly Payments - GFV
    req_deposit = CASH_PRICE - total_monthly_paid - est_gfv
    
    st.divider()
    
    if st.button("➕ Save this Scenario"):
        new_entry = {
            "Mileage": f"{mileage_in:,}",
            "Monthly Pay": f"£{monthly_in}",
            "Deposit": f"£{max(0, req_deposit):,.2f}",
            "Final Payment (GFV)": f"£{est_gfv:,.2f}",
            "Total Payable": f"£{CASH_PRICE:,.2f}"
        }
        st.session_state.history.append(new_entry)
        st.success("Scenario saved!")

# --- MAIN DISPLAY ---
col1, col2, col3 = st.columns(3)

with col1:
    # Handle negative deposit math (where monthly pay is so high it covers the car)
    display_deposit = max(0, req_deposit)
    st.metric("Required Deposit", f"£{display_deposit:,.2f}")
    if req_deposit < 0:
        st.caption("⚠️ Monthly payments cover the car; deposit not required.")

with col2:
    st.metric("Final Payment (GFV)", f"£{est_gfv:,.2f}")
    st.caption(f"Based on {mileage_in:,} miles/year")

with col3:
    st.metric("Interest Rate", "0.0% APR")
    st.caption("Fixed Rate ")

# --- HISTORY TABLE ---
st.divider()
st.subheader("📊 Comparison History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.table(df)
    
    if st.button("🗑️ Clear All"):
        st.session_state.history = []
        st.rerun()
else:
    st.info("Adjust the settings and click 'Save this Scenario' to start a comparison table.")

# --- THE MATH ---
with st.expander("Show the Math (0% APR PCP Formula)"):
    st.write("Because there is no interest, we use a simple balancing equation:")
    st.latex(r"Deposit = CashPrice - (MonthlyPayment \times 48) - GFV")
    st.write(f"Currently: £{CASH_PRICE:,.2f} - (£{monthly_in} × 48) - £{est_gfv:,.2f} = **£{req_deposit:,.2f}**")
