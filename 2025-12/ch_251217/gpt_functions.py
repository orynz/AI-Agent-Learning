# gpt_functions.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_weather(city) -> str:
    # print(city.replace(" ", ""))
    # city = city.replace(" ", "")
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "OPENWEATHER_API_KEY가 .env에 없습니다."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "kr",
    }

    try:
        r = requests.get(url, params=params, timeout=10)

        # 핵심: 실패 원인을 그대로 보여주기
        if r.status_code != 200:
            return f"OpenWeather API 오류: {r.status_code} / {r.text}"

        data = r.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels = data["main"]["feels_like"]
        hum = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        return f"{r.status_code}의 현재 날씨: {desc}, 기온 {temp:.1f}°C(체감 {feels:.1f}°C), 습도 {hum}%, 풍속 {wind:.1f}m/s"

    except Exception as e:
        return f"날씨 조회 예외: {type(e).__name__}: {e}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "사용자의 요청을 확인해서 도시를 변수로 넣어주면 해당 도시의 날씨 데이터를 반환한다.",
            "parameters": {
                "type": "object", 
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City and country e.g. Seoul, KR"
                    },
                }
            },
            "required": ["city"]
        },
    }
]
