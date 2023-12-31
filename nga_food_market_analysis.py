# -*- coding: utf-8 -*-
"""NGA_food_market_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B1u_H-68JqAFY1xOAkmm2mj9f1m1bTSe

## Import libraries
"""

!pip install pmdarima
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Commented out IPython magic to ensure Python compatibility.
if not os.path.exists("sustainable_data_roo"):
  !git clone https://github.com/JixTheCat/sustainable_data_roo

# %cd sustainable_data_roo

"""## Data Preprocessing"""

url = "https://raw.githubusercontent.com/JixTheCat/sustainable_data_roo/main/data/wfp_food_prices_nga.csv"

# Use pandas to read the CSV data from the URL
df = pd.read_csv(url)
df = df[df['price'] != 0] # Removes rows with zero values in column 'price'
df["Country"] = "Nigeria"
df

# OR RUN THIS STEP
# downlaod and read the data
df = pd.read_csv("data/wfp_food_prices_nga.csv")    # Downlaod the dataset from https://data.humdata.org/dataset/wfp-food-prices-for-nigeria or use the above Github account
df = df[df['price'] != 0] # Removes rows with zero values in column 'price'
df["Country"] = "Nigeria"
df

# Assuming you have a DataFrame named df
df = df.iloc[1:]  # This removes the first row (index 0)

# If you want to reset the index after removing the first row
df.reset_index(drop=True, inplace=True)
df

df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['usdprice'] = pd.to_numeric(df['usdprice'], errors='coerce')

# Plot the counts of unique values in the 'commodity' column
commodity_counts = df["commodity"].value_counts()

# Create a bar plot
plt.figure(figsize=(22, 10))
commodity_counts.plot(kind='bar', color='skyblue')
#plt.xlabel('Commodity')
plt.ylabel('Count')
#plt.title('Count of Each Commodity')
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility

plt.show()

# Select the 'rice' commodity from the entire dataset, as rice is one of the most widely consumed commodities in Nigeria.
rice_commodities = df[df['commodity'].str.contains('rice', case=False, na=False)]

commodity_market_counts = rice_commodities.groupby(['commodity', 'market']).size().unstack(fill_value=0)

# Create a bar plot
commodity_market_counts.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.xlabel('Commodity')
plt.ylabel('Count')
plt.title('Count of Commodity by Market')
plt.xticks(rotation=90)  # Rotate x-axis labels for better visibility

plt.show()

#Creating plots of possible market for rice seeling in Nigeria
market_counts = rice_commodities['market'].value_counts()

# Create a bar plot
market_counts.plot(kind='bar', figsize=(22, 10), color='red')
plt.xlabel('Market')
plt.ylabel('Count')
plt.title('Rice distribution in avilable Market')
plt.xticks(rotation=45)  # Rotate x-axis labels for better visibility

plt.show()

rice_commodities.info()

df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['usdprice'] = pd.to_numeric(df['usdprice'], errors='coerce')

# Create a dictionary of conversion factors for different units to 100 KG
unit_conversion = {'1.4 KG': 100 / 1.4, 'KG': 100 / 1, '100 KG': 1, '50 KG': 2, 'Unit': 100 / 1}

# Create new columns with updated units and prices
rice_commodities['unit_updated'] = '100 KG'  # Set the unit to '100 KG' for all rows
rice_commodities['price_updated'] = rice_commodities.apply(lambda row: row['price'] * unit_conversion.get(row['unit'], 1), axis=1)
rice_commodities['usdprice_updated'] = rice_commodities.apply(lambda row: row['usdprice'] * unit_conversion.get(row['unit'], 1), axis=1)



# Print the updated DataFrame
rice_commodities

"""## Time Series Visualisation"""

# Assuming your DataFrame is named 'rice_commodities'
selected_columns = rice_commodities[['commodity','price_updated', 'usdprice_updated', 'date', 'market']]

# Print the selected columns
selected_columns

# Assuming your DataFrame is named 'rice_commodities' and contains a 'date' column
rice_prices = rice_commodities[rice_commodities['commodity'].isin(['Rice (local)', 'Rice (imported)', 'Rice (milled, local)'])]

# Set the figure size and style
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# Plot the time series for each commodity
for commodity, data in rice_prices.groupby('commodity'):
    sns.lineplot(x='date', y='price_updated', data=data, label=commodity)

# Set labels and title
plt.xlabel('Date')
plt.ylabel('Price (Nigerian Currency)')
#plt.title('Nigeria Rice Price Trends Over Two Decades (Jan 2002 - Jan 2023)')

# Add a legend
plt.legend()

# Show the plot
plt.show()

rice_prices.info()

# Convert the 'date' column to a datetime object
rice_prices['date'] = pd.to_datetime(rice_prices['date'])

# The 'format' parameter is used to specify the format of your date strings. You need to provide the format that matches your date strings.

# Now, the 'date' column is converted to a proper date format.

# Set the figure size and style
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

# Extract the year from the date
rice_prices['year'] = rice_prices['date'].dt.year

# Plot the time series for each commodity year-wise
sns.lineplot(x='year', y='price_updated', hue='commodity', data=rice_prices)

# Set labels and title
plt.xlabel('Year')
plt.ylabel('Price (Nigerian Currency)')
plt.title('Yearly Time Series of Rice Prices')

# Add a legend
plt.legend()

# Show the plot
plt.show()

selected_columns = rice_commodities[['date', 'price_updated']]


# Set 'date' as the index
selected_columns.set_index('date', inplace=True)

# Check if the time series is stationary (you might need to difference it)
result = adfuller(selected_columns['price_updated'])
if result[1] > 0.05:
    print("Time series is not stationary, you may need to difference it.")
else:
    print("Time series is stationary.")

# Split the data into training and testing sets
train_size = int(0.8 * len(selected_columns))
train, test = selected_columns.iloc[:train_size], selected_columns.iloc[train_size:]

# Determine the order of the ARIMA model (you can adjust p, d, q)
p, d, q = 1, 1, 1  #  you may need to adjust these
model = ARIMA(train, order=(p, d, q))
model_fit = model.fit()

# Forecast future values
forecast = model_fit.forecast(steps=len(test))

# Plot the original and forecasted time series
plt.figure(figsize=(12, 6))
plt.plot(train, label='Training Data')
plt.plot(test, label='Testing Data')
plt.plot(test.index, forecast, label='ARIMA Forecast', color='red')
plt.legend()
plt.title('ARIMA Forecast for Rice Prices')
plt.show()

# Convert 'date' column to datetime
rice_commodities['date'] = pd.to_datetime(rice_commodities['date'], dayfirst=True)

# Function to determine season based on month
def season(month):
    return 'Rainy' if 4 <= month <= 10 else 'Dry'

# Apply the function to the 'date' column to create a new 'season' column
rice_commodities['season'] = rice_commodities['date'].dt.month.apply(season)

# Group by season and date and calculate the mean price for each group
seasonal_prices = rice_commodities.groupby(['season', 'date'])['price_updated'].mean().reset_index()

# Split the data into two separate dataframes for rainy and dry seasons
rainy_season_data = seasonal_prices[seasonal_prices['season'] == 'Rainy']
dry_season_data = seasonal_prices[seasonal_prices['season'] == 'Dry']

# Find the global minimum and maximum price to unify y-axis across plots
global_min_price = seasonal_prices['price_updated'].min()
global_max_price = seasonal_prices['price_updated'].max()

# Plotting
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True, sharey=True)

# Rainy Season Plot
axes[0].plot(rainy_season_data['date'], rainy_season_data['price_updated'], label='Rainy Season')
axes[0].set_title('Price by Date During Rainy Season')
axes[0].set_ylabel('Price')
axes[0].set_ylim(global_min_price, global_max_price) # Uniform Y-Axis

# Dry Season Plot
axes[1].plot(dry_season_data['date'], dry_season_data['price_updated'], label='Dry Season', color='orange')
axes[1].set_title('Price by Date During Dry Season')
axes[1].set_ylabel('Price')
axes[1].set_ylim(global_min_price, global_max_price) # Uniform Y-Axis
axes[1].set_xlabel('Date')

# Set the x-axis to show the date labels
for tick in axes[1].get_xticklabels():
    tick.set_rotation(45)

# Show the legend
axes[0].legend()
axes[1].legend()

# Adjust layout
plt.tight_layout()
plt.show()

# Yearly Temporal Trends of Rice Commodity in Nigeria
commodities = rice_commodities["commodity"].unique()
# Define your custom color palette for the commodities
colors = {
    'Rice (local)': 'green',
    'Rice (imported)': 'blue',
    'Rice (milled, local)': 'darkorange',
}

# Since we need to plot by commodity, we will regroup the data including the commodity
seasonal_commodity_prices = rice_commodities.groupby(['season', 'date', 'commodity'])['price_updated'].mean().reset_index()

# Split the data into rainy and dry season data again, this time including commodity
rainy_season_commodity_data = seasonal_commodity_prices[seasonal_commodity_prices['season'] == 'Rainy']
dry_season_commodity_data = seasonal_commodity_prices[seasonal_commodity_prices['season'] == 'Dry']

# Plotting
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 12), sharex=True, sharey=True)

# Plot for each commodity in the rainy season
for commodity in commodities:
    commodity_data = rainy_season_commodity_data[rainy_season_commodity_data['commodity'] == commodity]
    axes[0].plot(commodity_data['date'], commodity_data['price_updated'], label=commodity, color=colors.get(commodity, 'gray'))

# Rainy Season Plot details
axes[0].set_title('Price during Rainy Season')
axes[0].set_ylabel('Price')
axes[0].set_ylim(global_min_price, global_max_price)  # Uniform Y-Axis
axes[0].legend()

# Plot for each commodity in the dry season
for commodity in commodities:
    commodity_data = dry_season_commodity_data[dry_season_commodity_data['commodity'] == commodity]
    axes[1].plot(commodity_data['date'], commodity_data['price_updated'], label=commodity, color=colors.get(commodity, 'gray'))

# Dry Season Plot details
axes[1].set_title('Price during Dry Season')
axes[1].set_ylabel('Price')
axes[1].set_ylim(global_min_price, global_max_price)  # Uniform Y-Axis
axes[1].set_xlabel('Date')
axes[1].legend()

# Set the x-axis to show the date labels
for tick in axes[1].get_xticklabels():
    tick.set_rotation(45)

# Adjust layout and show the plot
plt.tight_layout()
plt.show()

