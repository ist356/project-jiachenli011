import requests
import pandas as pd

weather_api = "2ab8e147c79821aac1dce406053f3f40" 

def get_current_weather(city):
    """
    Get real-time weather data for a specified city from the Weatherstack API
    """
    access_key = weather_api
    url = "http://api.weatherstack.com/current"
    
    params = {
        "access_key": access_key,
        "query": city
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "error" in data:
            print(f"Something Wrong: {data['error']['info']}")
            return None
        
        return data  
    
    except Exception as i:
        print(f"Fail to request: {i}")

        return None
    
def weather_data_to_dataframe(weather_data: dict):
    """
    Convert the returned weather data to a Pandas DataFrame
    weather_data: JSON data returned by get_current_weather
    return -> Pandas DataFrame
    """
    
    extracted_data = {
            "City": weather_data["location"]["name"],
            "Country": weather_data["location"]["country"],
            "Local Time": weather_data["location"]["localtime"],
            "Temperature (C)": weather_data["current"]["temperature"],
            "Weather Description": weather_data["current"]["weather_descriptions"][0],
            "Wind Speed (km/h)": weather_data["current"]["wind_speed"],
            "Humidity (%)": weather_data["current"]["humidity"],
            "Pressure (mb)": weather_data["current"]["pressure"]
    }

    df = pd.DataFrame([extracted_data])
    return df

# def get_historical_weather(city: str, date: str,  hourly: int , units: str = "m") -> dict:
    """
    从 Weatherstack API 获取指定城市和日期的历史天气数据
    :param city: 城市名称，例如 'Shanghai'
    :param date: 历史日期，例如 '2024-12-01'，格式为 'YYYY-MM-DD'
    :param access_key: 你的 API 访问密钥
    :param hourly: 是否获取每小时数据，1 为开启，0 为关闭 (可选，默认开启)
    :param units: 单位系统，"m" 为公制，"s" 为科学制，"f" 为英制 (可选，默认 "m")
    :return: 包含历史天气数据的字典
    """
    url = "http://api.weatherstack.com/historical"
    params = {
        "access_key": weather_api,
        "query": city,
        "historical_date": date,
        "hourly": hourly,
        "units": units
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            print(f"API 错误: {data['error']['info']}")
            return None
        return data
    except Exception as e:
        print(f"数据提取失败: {e}")
        return None

# def historical_weather_to_dataframe(weather_data: dict) -> pd.DataFrame:
    """
    将历史天气数据转换为 Pandas DataFrame
    :param weather_data: get_historical_weather 返回的 JSON 数据
    :return: Pandas DataFrame
    """
    # 提取日期和天气数据
    date = list(weather_data["historical"].keys())[0]
    weather_info = weather_data["historical"][date]["hourly"]
    
    # 转换为 DataFrame
    df = pd.DataFrame(weather_info)
    df["date"] = date  # 添加日期列
    return df


def merge_weather_data(cities: list) -> pd.DataFrame:
    """
    Merge the current weather data of multiple cities into one DataFrame
    cities: list of cities,
    return -> DataFrame containing the current weather data of all cities
    """
    all_data = []  

    for city in cities:
        weather_data = get_current_weather(city)

        if weather_data:
            extracted_data = weather_data["location"].copy()  
            extracted_data.update(weather_data["current"])   
            extracted_data["City"] = weather_data["location"]["name"]  
            all_data.append(extracted_data)
        else:
            print(f"Not able to get {city} data, try another one。")

    
    return pd.DataFrame(all_data)


if __name__ == "__main__":
    weather_data = get_current_weather("New York")
    print(weather_data)
   # print(get_historical_weather("New York","2023-12-01",1))