from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

model = joblib.load("crime_model.pkl")


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    lat, lon, hour, dayofweek, month = data["Latitude"], data["Longitude"], data["Hour"], data["DayOfWeek"], data[
        "Month"]

    risk = model.predict([[lat, lon, hour, dayofweek, month]])[0]

    return jsonify({"Crime Risk Score": round(risk, 2)})


if __name__  == "__main__":
    app.run(debug=True)
