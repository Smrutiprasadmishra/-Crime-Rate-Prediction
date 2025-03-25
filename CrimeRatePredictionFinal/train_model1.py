import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
import numpy as np

# Check if dataset exists
if not os.path.exists("processed_crime_data.csv"):
    print("❌ Error: File not found!!")
    exit()

# Load dataset
df = pd.read_csv("processed_crime_data.csv")

# Encode 'Primary Type' as numerical labels (if it's categorical)
df['Primary Type'] = df['Primary Type'].astype('category').cat.codes

# Define Features (X) and Target (y)
X = df[['Latitude', 'Longitude', 'Hour', 'DayOfWeek', 'Month']]
y = df['Primary Type']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training set shape:", X_train.shape, y_train.shape)
print("Test set shape:", X_test.shape, y_test.shape)

# Train the Model
model = RandomForestRegressor(n_estimators=5, random_state=42)
model.fit(X_train, y_train)

# Check Training Accuracy
print("🔄 Checking training score...")
train_score = model.score(X_train, y_train)
print("✅ Training Accuracy:", train_score)

# Save Model
joblib.dump(model, "crime_model.pkl")
print("✅ Model Trained and Saved!")

# Load Model
loaded_model = joblib.load("crime_model.pkl")

# Define input data as a Pandas DataFrame (Fixes the Warning)
input_data = pd.DataFrame([[40.7128, -74.0060, 22, 5, 10]], columns=['Latitude', 'Longitude', 'Hour', 'DayOfWeek', 'Month'])

# Make Prediction
prediction = loaded_model.predict(input_data)
print("🚔 Predicted Crime Type Code:", prediction[0])

# Convert back to original category (optional)
crime_mapping = dict(enumerate(df['Primary Type'].astype('category').cat.categories))
predicted_crime_type = crime_mapping[int(prediction[0])]
print("🚔 Predicted Crime Type:", predicted_crime_type)

