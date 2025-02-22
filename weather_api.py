

from fastapi import FastAPI, Query
import requests

app = FastAPI()

OPENWEATHER_API_KEY = "d220a1b133c215e83c381ebc061d2980"
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"

@app.get("/weather")
def get_weather(
    city: str = Query(..., description="اسم المدينة"),
    lat: float = Query(..., description="خط العرض"),
    lon: float = Query(..., description="خط الطول")
):
    
    params = {
        "q": city,
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ar"
    }

    response = requests.get(OPENWEATHER_URL, params=params)
    if response.status_code != 200:
        return {"error": f"خطأ في جلب البيانات: {response.status_code}"}

    data = response.json()

    forecast_list = []
    for forecast in data["list"]:  
        forecast_list.append({
            "date_time": forecast["dt_txt"],
            "temperature": forecast["main"]["temp"],
            "wind_speed": forecast["wind"]["speed"],
            "humidity": forecast["main"]["humidity"],
            "pressure": forecast["main"]["pressure"],
            "description": forecast["weather"][0]["description"]
        })

    return {
        "city": city,
        "latitude": lat,
        "longitude": lon,
        "forecasts": forecast_list
    }

