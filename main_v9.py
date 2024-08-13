import streamlit as st
import pandas as pd
import random
import time
from streamlit_lottie import st_lottie
import json

# Function to load a Lottie animation from a JSON file
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# Function to simulate winner selection and display results
def simulate_winner_selection(customer_codes, num_winners, lottie_animation, prize_name):
    # Display the animation
    st_lottie(lottie_animation, height=300, key=f"animation_{prize_name}")
    
    time.sleep(3)  # Show the animation for 3 seconds
    
    # Select the winners
    selected_winners = random.sample(customer_codes, num_winners)
    for winner in selected_winners:
        customer_codes.remove(winner)  # Remove the winner from the pool
    
    # Display the winners
    st.markdown(f"### {prize_name} Winners:")
    for winner in selected_winners:
        st.write(f"- {winner}")
    
    return selected_winners

st.title("Lottery Winner Selector with Lottie Animation")

# Load the Lottie animation (replace with your actual file path)
lottie_spinner = load_lottiefile("wheel-animation-red.json")
#lottie_spinner = load_lottiefile("wheel-animation.json")

# File upload
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Load the Excel file
    df = pd.read_excel(uploaded_file, sheet_name='Sheet1')
    
    if "Customer Code" in df.columns:
        customer_codes = df["Customer Code"].dropna().astype(str).tolist()  # Convert codes to string
        if st.button("Select All Winners"):
            # Progress bar
            progress_bar = st.progress(0)
            
            # Select winners for each prize
            first_prize_winner = simulate_winner_selection(customer_codes, 1, lottie_spinner, "First Prize")
            progress_bar.progress(0.1)
            
            second_prize_winners = simulate_winner_selection(customer_codes, 2, lottie_spinner, "Second Prize")
            progress_bar.progress(0.3)
            
            third_prize_winners = simulate_winner_selection(customer_codes, 10, lottie_spinner, "Third Prize")
            progress_bar.progress(0.6)
            
            fourth_prize_winners = simulate_winner_selection(customer_codes, 25, lottie_spinner, "Fourth Prize")
            progress_bar.progress(1.0)
            
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
            st.write("### All Winners:")
            st.dataframe(winners_df)
            
            # Export to Excel with Customer Code as text
            winners_df.to_excel("winners_list.xlsx", index=False)
            st.write("### Winners have been saved to `winners_list.xlsx`.")
            
    else:
        st.error("The sheet does not contain a 'Customer Code' column.")
