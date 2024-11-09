import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
st.title('Option Strategy Builder🐂🐻')

# Get number of option legs
num_options = st.sidebar.number_input("Total number of strikes/legs:", min_value=1, max_value=5, step=1, value=1, format="%d")

# Initialize an empty list to store option details
option_legs = []

# Collect details for each option leg from the user
for i in range(num_options):
    st.sidebar.write(f"Enter details for leg {i + 1}:")
    
    strike_price = st.sidebar.number_input(f"Strike Price for leg {i + 1}:", min_value=1, max_value=1000000, step=1, value=20000, format="%d", key=f"strike_price_{i}")
    premium = st.sidebar.number_input(f"Premium for leg {i + 1}:", min_value=1, max_value=100000, step=1, value=100, format="%d", key=f"premium_{i}")
    option_type = st.sidebar.text_input(f"Option Type ('call' or 'put') for leg {i + 1}:", value='call', key=f"option_type_{i}").strip().lower()
    position = st.sidebar.number_input(f"Position (1 for sell, -1 for buy) for leg {i + 1}:", min_value=-1, max_value=1, step=1, value=1, format="%d", key=f"position_{i}")

    option_legs.append({
        'strike_price': strike_price,
        'premium': premium,
        'type': option_type,
        'position': position
    })

# Payoff Calculation
min_price = min(option['strike_price'] for option in option_legs) - 500
max_price = max(option['strike_price'] for option in option_legs) + 500
price_range = np.arange(min_price, max_price, 10)

# Function to calculate payoff for individual option
def option_payoff(underlying_price, option):
    if option['type'] == 'put':
        intrinsic_value = max(option['strike_price'] - underlying_price, 0)
    elif option['type'] == 'call':
        intrinsic_value = max(underlying_price - option['strike_price'], 0)
    return option['position'] * (intrinsic_value - option['premium'])

# Calculate total payoff for the strategy
total_payoff = []
for price in price_range:
    payoff = sum(option_payoff(price, option) for option in option_legs)
    total_payoff.append(payoff)

# Plot the payoff diagram with color change at zero
fig, ax = plt.subplots(figsize=(10, 6))

# Separate the price range based on the payoff being positive or negative
for i in range(1, len(price_range)):
    if total_payoff[i - 1] >= 0 and total_payoff[i] >= 0:
        ax.plot(price_range[i-1:i+1], total_payoff[i-1:i+1], color='green', label="Profit" if i == 1 else "")
    elif total_payoff[i - 1] < 0 and total_payoff[i] < 0:
        ax.plot(price_range[i-1:i+1], total_payoff[i-1:i+1], color='red', label="Loss" if i == 1 else "")
    else:
        ax.plot(price_range[i-1:i+1], total_payoff[i-1:i+1], color='green' if total_payoff[i] >= 0 else 'red')

# Add labels and grid
ax.axhline(0, color='black', linewidth=0.5)
ax.set_xlabel("Underlying Price at Expiry")
ax.set_ylabel("Profit / Loss")
ax.set_title("Options Strategy Payoff Diagram")
ax.legend()
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)

if st.button('My GitHub'):
    st.markdown("[Click here to visit my GitHub](https://github.com/HitanshKumar?tab=repositories)", unsafe_allow_html=True)
st.write("Contact: hitanshkumar@gmail.com")
