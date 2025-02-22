from fastapi import FastAPI, Query
import requests
import os  # To access environment variables

app = FastAPI()

# Read the API key from environment variables
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/forecast"

@app.get("/weather")
def get_weather(
    city: str = Query(None, description="اسم المدينة (اختياري)"),
    lat: float = Query(None, description="خط العرض (اختياري)"),
    lon: float = Query(None, description="خط الطول (اختياري)")
):
    """إرجاع بيانات الطقس لمدة 5 أيام كـ JSON"""

    # Ensure the API key is available
    if OPENWEATHER_API_KEY is None:
        return {"error": "API key is not set in environment variables"}

    # Validate if either city or lat/lon is provided
    if not city and (lat is None or lon is None):
        return {"error": "يجب توفير إما اسم المدينة أو إحداثيات الموقع (خط العرض والطول)"}

    # استدعاء API الطقس
    params = {
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ar"
    }

    if city:
        params["q"] = city
    if lat and lon:
        params["lat"] = lat
        params["lon"] = lon

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
        "city": city if city else "Unknown",
        "latitude": lat if lat else "Unknown",
        "longitude": lon if lon else "Unknown",
        "forecasts": forecast_list
    }
    
# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Weather API is live! Please use /weather endpoint."}
