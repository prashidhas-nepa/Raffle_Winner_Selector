import streamlit as st
import pandas as pd
import random

# Function to select lottery winners
def select_lottery_winners(customer_codes):
    if len(customer_codes) >= 38:  # 1 + 2 + 10 + 25 = 38
        first_prize_winner = random.sample(customer_codes, 1)
        remaining_customers = list(set(customer_codes) - set(first_prize_winner))
        
        second_prize_winners = random.sample(remaining_customers, 2)
        remaining_customers = list(set(remaining_customers) - set(second_prize_winners))
        
        third_prize_winners = random.sample(remaining_customers, 10)
        remaining_customers = list(set(remaining_customers) - set(third_prize_winners))
        
        fourth_prize_winners = random.sample(remaining_customers, 25)

        return {
            "First Prize": first_prize_winner,
            "Second Prize": second_prize_winners,
            "Third Prize": third_prize_winners,
            "Fourth Prize": fourth_prize_winners
        }
    else:
        return "Not enough customer codes to select all winners."

# Streamlit app
st.title("Lottery Winner Selector")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Load the Excel file
    try:
        df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
        
        if "Customer Code" in df.columns:
            customer_codes = df["Customer Code"].dropna().tolist()
            winners = select_lottery_winners(customer_codes)
            
            if isinstance(winners, dict):
                st.success("Winners selected successfully!")
                st.write("### First Prize Winner:")
                st.write(winners["First Prize"])
                st.write("### Second Prize Winners:")
                st.write(winners["Second Prize"])
                st.write("### Third Prize Winners:")
                st.write(winners["Third Prize"])
                st.write("### Fourth Prize Winners:")
                st.write(winners["Fourth Prize"])
            else:
                st.error(winners)
        else:
            st.error("The sheet does not contain a 'Customer Code' column.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
