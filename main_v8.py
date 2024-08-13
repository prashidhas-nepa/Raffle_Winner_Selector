import streamlit as st
import pandas as pd
import random
import time

# Function to simulate a flashing highlight effect
def simulate_flashing_spinner(customer_codes, prize_name, num_winners, progress_bar):
    st.write(f"## Selecting {num_winners} winner(s) for {prize_name}...")
    selected_winners = []

    for i in range(num_winners):
        final_choice = None
        # Simulate the flashing effect by showing random customer codes
        for _ in range(20):  # Flash 20 times for effect
            current_choice = random.choice(customer_codes)
            st.markdown(f"<h1 style='text-align: center; color: red;'>{current_choice}</h1>", unsafe_allow_html=True)
            time.sleep(0.1)

        # Final selection
        final_choice = random.choice(customer_codes)
        selected_winners.append(final_choice)
        customer_codes.remove(final_choice)  # Remove the winner from the pool
        
        # Flash the final choice for a longer time
        st.markdown(f"<h1 style='text-align: center; color: green;'>{final_choice} - WINNER!</h1>", unsafe_allow_html=True)
        time.sleep(1)
        progress_bar.progress((i + 1) / num_winners)
    
    return selected_winners

st.title("Lottery Winner Selector with Flashing Highlight Animation")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Load the Excel file
    df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
    
    if "Customer Code" in df.columns:
        customer_codes = df["Customer Code"].dropna().astype(str).tolist()  # Convert codes to string
        if st.button("Select All Winners"):
            progress_bar = st.progress(0)
            # Select winners for each prize
            first_prize_winner = simulate_flashing_spinner(customer_codes, "First Prize", 1, progress_bar)
            second_prize_winners = simulate_flashing_spinner(customer_codes, "Second Prize", 2, progress_bar)
            third_prize_winners = simulate_flashing_spinner(customer_codes, "Third Prize", 10, progress_bar)
            fourth_prize_winners = simulate_flashing_spinner(customer_codes, "Fourth Prize", 25, progress_bar)
            
            # Combine all winners into a DataFrame
            all_winners = {
                "Prize": ["First Prize"] * len(first_prize_winner) +
                         ["Second Prize"] * len(second_prize_winners) +
                         ["Third Prize"] * len(third_prize_winners) +
                         ["Fourth Prize"] * len(fourth_prize_winners),
                "Customer Code": first_prize_winner + second_prize_winners + 
                                 third_prize_winners + fourth_prize_winners
            }
            winners_df = pd.DataFrame(all_winners)
            
            # Display the winners
            st.write("### Winners:")
            st.dataframe(winners_df)
            
            # Export to Excel with Customer Code as text
            winners_df.to_excel("winners_list.xlsx", index=False)
            st.write("### Winners have been saved to `winners_list.xlsx`.")
            
    else:
        st.error("The sheet does not contain a 'Customer Code' column.")
