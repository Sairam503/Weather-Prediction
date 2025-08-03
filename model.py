# model.py

# 📦 Import Required Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# 📥 Load Dataset
df = pd.read_csv("./processed_weather_data.csv")

# 🧹 Data Preprocessing
# Encode categorical features
le_state = LabelEncoder()
le_weather = LabelEncoder()
df['State'] = le_state.fit_transform(df['State'])
df['WeatherType'] = le_weather.fit_transform(df['WeatherType'])

# 🎯 Features and Target
X = df[['State', 'Month', 'Day', 'Hour', 'Temperature', 'Humidity', 'WindSpeed']]
y = df['WeatherType']

# 🔀 Split Dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🧠 Train Model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 📊 Evaluate Model
y_pred = model.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))

# 💾 Save Model and Encoders
joblib.dump(model, "weather_model.pkl")
joblib.dump(le_state, "state_encoder.pkl")
joblib.dump(le_weather, "weather_encoder.pkl")
