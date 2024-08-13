import streamlit as st
import pandas as pd
import random
import time

# Function to simulate a wheel of fortune spinner
def simulate_wheel_spinner(customer_codes):
    st.write("## Spinning the wheel...")
    time.sleep(2)  # Add suspense by sleeping for a few seconds
    return random.choice(customer_codes)

st.title("Lottery Winner Selector with Wheel Spinner")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Load the Excel file
    df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
    
    if "Customer Code" in df.columns:
        customer_codes = df["Customer Code"].dropna().tolist()
        if st.button("Spin the Wheel for First Prize Winner"):
            first_prize_winner = simulate_wheel_spinner(customer_codes)
            st.success(f"The First Prize Winner is: {first_prize_winner}")
            customer_codes.remove(first_prize_winner)
        
        if st.button("Spin the Wheel for Second Prize Winners"):
            second_prize_winners = random.sample(customer_codes, 2)
            st.success(f"The Second Prize Winners are: {second_prize_winners}")
            for winner in second_prize_winners:
                customer_codes.remove(winner)
        
        if st.button("Spin the Wheel for Third Prize Winners"):
            third_prize_winners = random.sample(customer_codes, 10)
            st.success(f"The Third Prize Winners are: {third_prize_winners}")
            for winner in third_prize_winners:
                customer_codes.remove(winner)
        
        if st.button("Spin the Wheel for Fourth Prize Winners"):
            fourth_prize_winners = random.sample(customer_codes, 25)
            st.success(f"The Fourth Prize Winners are: {fourth_prize_winners}")
            for winner in fourth_prize_winners:
                customer_codes.remove(winner)
    else:
        st.error("The sheet does not contain a 'Customer Code' column.")
