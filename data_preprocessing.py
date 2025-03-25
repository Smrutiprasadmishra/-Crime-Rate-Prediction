import pandas as pd

# load csv file
df = pd.read_csv("Crime_data from 2001 to present.csv")

df["Date"] = pd.to_datetime(df["Date"])

df['Hour'] = df['Date'].dt.hour
df['Month'] = df['Date'].dt.month
df['DayOfWeek'] = df['Date'].dt.dayofweek

# Encode crime types as numerical labels
df['Primary Type'] = df['Primary Type'].astype('category').cat.codes

# Select relevant features
df = df[['Latitude', 'Longitude', 'Hour', 'DayOfWeek', 'Month', 'Primary Type']]

# Save preprocessed data
df.to_csv("processed_crime_data.csv", index=False)
print("Data Preprocessing Complete!")
