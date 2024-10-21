import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('monthly (1).csv')

# Convert 'Date' to datetime for proper time-based operations
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')

# Extract Year and Month as separate columns
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month_name()

# Sidebar filters for interactive exploration
st.sidebar.header("Filters")
year_range = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), 
                               (int(df['Year'].min()), int(df['Year'].max())))
selected_month = st.sidebar.multiselect("Select Month(s)", df['Month'].unique(), default=df['Month'].unique())

# Filter data based on selection
filtered_data = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) & df['Month'].isin(selected_month)]

# Remove the timestamp from 'Date' for display purposes
filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m')

# Title
st.title("Gold Price Analysis")

# Display filtered dataset without commas in 'Year' and clean Date
st.subheader(f"Gold Prices from {year_range[0]} to {year_range[1]} for selected months")
filtered_data['Year'] = filtered_data['Year'].astype(str)  # Convert 'Year' to string to avoid commas
st.dataframe(filtered_data)

# Plot price trends (filtered data)
st.subheader("Gold Price Trend")
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(pd.to_datetime(filtered_data['Date'], format='%Y-%m'), filtered_data['Price'], label='Price', color='blue', linewidth=2)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Price (USD)", fontsize=12)
ax.set_title(f"Gold Price Over Time ({year_range[0]} to {year_range[1]})", fontsize=14)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.xticks(rotation=45)  # Rotate x-axis labels to prevent overlap
st.pyplot(fig)

# Group by Year and show yearly statistics (filtered data)
yearly_data = filtered_data.groupby('Year').agg({'Price': ['mean', 'min', 'max']}).reset_index()
yearly_data.columns = ['Year', 'Mean Price', 'Min Price', 'Max Price']

# Display Yearly Gold Price Statistics
st.subheader("Yearly Gold Price Statistics")
st.dataframe(yearly_data.style.format({"Mean Price": "{:.2f}", "Min Price": "{:.2f}", "Max Price": "{:.2f}"}))

# Plotting yearly average gold prices
st.subheader("Yearly Average Gold Price")
fig2, ax2 = plt.subplots(figsize=(10,6))
ax2.plot(yearly_data['Year'], yearly_data['Mean Price'], label='Average Price', color='green', linewidth=2)
ax2.set_xlabel("Year", fontsize=12)
ax2.set_ylabel("Average Price (USD)", fontsize=12)
ax2.set_title(f"Yearly Average Gold Price ({year_range[0]} to {year_range[1]})", fontsize=14)
ax2.grid(True, linestyle='--', linewidth=0.5)
plt.xticks(rotation=45, ha='right')
if len(yearly_data['Year']) > 10:  # If there are too many years, reduce the number of ticks shown
    ax2.set_xticks(ax2.get_xticks()[::2])  # Show every other label
st.pyplot(fig2)

# Monthly average price graph (filtered data)
monthly_data = filtered_data.groupby('Month').agg({'Price': 'mean'}).reset_index().sort_values('Month')
st.subheader("Monthly Average Gold Price")
fig3, ax3 = plt.subplots(figsize=(10,6))
ax3.bar(monthly_data['Month'], monthly_data['Price'], color='orange')
ax3.set_xlabel("Month", fontsize=12)
ax3.set_ylabel("Average Price (USD)", fontsize=12)
ax3.set_title(f"Average Gold Price per Month ({year_range[0]} to {year_range[1]})", fontsize=14)
ax3.grid(axis='y', linestyle='--', linewidth=0.5)
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels and align them to the right
st.pyplot(fig3)

# Insights section
st.subheader("Key Insights")
st.write(f"The average gold price from {year_range[0]} to {year_range[1]} for the selected months is {filtered_data['Price'].mean():.2f} USD.")

# Footer for data source
st.markdown("""
    **Footnote**: Data on gold prices is sourced from the [World Bank Commodities Market](https://www.worldbank.org/en/research/commodity-markets).
""")
