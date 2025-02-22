from fastapi import FastAPI, Query
import requests
import os  # To access environment variables

app = FastAPI()

# Read the API key from environment variables
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"

@app.get("/weather")
def get_weather(
    city: str = Query(..., description="اسم المدينة"),
    lat: float = Query(..., description="خط العرض"),
    lon: float = Query(..., description="خط الطول")
):
    """إرجاع بيانات الطقس لمدة 5 أيام كـ JSON"""

    # Ensure the API key is available
    if OPENWEATHER_API_KEY is None:
        return {"error": "API key is not set in environment variables"}

    # استدعاء API الطقس
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

    # تجميع بيانات الطقس لمدة 5 أيام
    forecast_list = []
    for forecast in data["list"]:  # تحتوي القائمة على توقعات كل 3 ساعات
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
