import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load the dataset
df = pd.read_csv('processed_weather_data.csv')

# Fix date parsing
df = df.dropna(subset=['year', 'month', 'day'])
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day']], errors='coerce')
df = df.dropna(subset=['datetime'])

# Target variable: Let's assume "temperature" exists
target = 'temperature'

# Drop unwanted columns
features = df.drop(columns=[target, 'datetime', 'station', 'year', 'month', 'day'])

# Final features
X = features
y = df[target]

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, preds))
print(f"RMSE: {rmse:.2f}")

# Save model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
