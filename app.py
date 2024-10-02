import requests
import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_URL = "http://api.weatherapi.com/v1/current.json?key="
API_KEY = "a1b413b4110b4c71ac7103743241507"

time_now = datetime.datetime.today()

@app.route("/", methods=['GET'])
def index():
    try:
        city_name = request.args.get('city_name')
        if city_name and city_name != '':
            result = get_weather(city_name)
            return render_template("weather.html", result=result) # При удачном вводе города
        else:
            return render_template('main.html') # При неудачном вводе города
    except:
        return render_template('main.html')

def get_weather(city_name):
    URL = BASE_URL + API_KEY + "&q=" + city_name + "&lang=ru"
    response = requests.get(URL)
    data = response.json()
    temperature_c = data["current"]["temp_c"]
    region = data["location"]["region"]
    country = data["location"]["country"]
    feelslike_c = data["current"]["feelslike_c"]
    local_time = data["location"]["localtime"]
    humidity = data["current"]["humidity"]
    condition = data["current"]["condition"]["text"]
    wind_ms = str(round(int(data["current"]["wind_kph"]) * 0.277778, 1)).replace('.', ',')
    pressure_mm = str(round(int(data["current"]["pressure_mb"]) * 0.750062))
    result = {"city_name" : city_name,
              "temperature_c" : int(temperature_c),
              "local_time" : local_time,
              "region" : region,
              "country" : country,
              "feelslike_c" : int(feelslike_c),
              "humidity" : humidity,
              "condition" : condition,
              "wind_ms" : wind_ms,
              "pressure_mm" : pressure_mm}
    return result

if __name__ == '__main__':
    app.run(debug=True)
