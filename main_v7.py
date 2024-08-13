import streamlit as st
import pandas as pd
import random
import time
import numpy as np
import matplotlib.pyplot as plt

# Function to create a wheel-like structure and simulate spinning
def simulate_wheel_spinner(customer_codes, prize_name, num_winners, progress_bar):
    st.write(f"## Selecting {num_winners} winner(s) for {prize_name}...")
    selected_winners = []
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    for i in range(num_winners):
        # Simulate the spinning wheel by rotating through customer codes
        for _ in range(20):  # Spin the wheel 20 times for effect
            current_choice = random.choice(customer_codes)
            ax.clear()
            wheel_codes = random.sample(customer_codes, min(10, len(customer_codes)))  # Show up to 10 random codes
            angles = np.linspace(0, 2 * np.pi, len(wheel_codes), endpoint=False).tolist()
            angles += angles[:1]
            wheel_codes += wheel_codes[:1]
            ax.plot(angles, [1] * len(angles), 'o-', linewidth=2)
            for angle, code in zip(angles[:-1], wheel_codes[:-1]):
                ax.text(angle, 1.05, code, horizontalalignment='center', verticalalignment='center')
            plt.gca().set_aspect('equal')
            st.pyplot(fig)
            time.sleep(0.1)
        
        # Final selection
        final_choice = random.choice(customer_codes)
        selected_winners.append(final_choice)
        customer_codes.remove(final_choice)  # Remove the winner from the pool
        progress_bar.progress((i + 1) / num_winners)
    
    return selected_winners

st.title("Lottery Winner Selector with Wheel Spinner and Animation")

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
            first_prize_winner = simulate_wheel_spinner(customer_codes, "First Prize", 1, progress_bar)
            second_prize_winners = simulate_wheel_spinner(customer_codes, "Second Prize", 2, progress_bar)
            third_prize_winners = simulate_wheel_spinner(customer_codes, "Third Prize", 10, progress_bar)
            fourth_prize_winners = simulate_wheel_spinner(customer_codes, "Fourth Prize", 25, progress_bar)
            
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
