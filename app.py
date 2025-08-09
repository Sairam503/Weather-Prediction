import os
from datetime import datetime
from collections import Counter
from flask import Flask, render_template, request, jsonify
import pandas as pd
import requests

# Initialize Flask app
app = Flask(__name__)

# Load dataset
df = pd.read_csv("processed_weather_data.csv")

# Get API key from environment variable
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# List of states for dropdown
states = sorted(df["State"].unique())


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    approximate = False

    if request.method == "POST":
        state = request.form.get("state", "")
        date_str = request.form.get("date", "")
        time_str = request.form.get("time", "")

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            hour = int(time_str)
            month, day = date.month, date.day

            # Exact match: state + month + day + hour
            matched = df[(df["State"].str.lower() == state.lower()) &
                         (df["Month"] == month) &
                         (df["Day"] == day) &
                         (df["Hour"] == hour)]

            # Fallback: same date (ignore hour)
            if matched.empty:
                matched = df[(df["State"].str.lower() == state.lower()) &
                             (df["Month"] == month) &
                             (df["Day"] == day)]
                approximate = True

            # Fallback: same month
            if matched.empty:
                matched = df[(df["State"].str.lower() == state.lower()) &
                             (df["Month"] == month)]
                approximate = True

            # Fallback: whole state
            if matched.empty:
                matched = df[df["State"].str.lower() == state.lower()]
                approximate = True

            if not matched.empty:
                prediction = {
                    "state": state.title(),
                    "date": date_str,
                    "time": f"{hour:02d}:00",
                    "temperature": round(matched["Temperature"].mean(), 2),
                    "humidity": round(matched["Humidity"].mean(), 2),
                    "wind_speed": round(matched["WindSpeed"].mean(), 2),
                    "weather_type": Counter(matched["WeatherType"]).most_common(1)[0][0],
                    "approximate": approximate
                }
            else:
                prediction = {"error": "No data available for that state."}

        except Exception as e:
            prediction = {"error": f"Error: {str(e)}"}

    return render_template("index.html", prediction=prediction, states=states)


@app.route("/get_weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "No city provided"}), 400

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            return jsonify({"error": data.get("message", "Failed to fetch weather")}), 400

        weather = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "location": data["name"]
        }
        return jsonify(weather)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
