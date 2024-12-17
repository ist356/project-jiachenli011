import folium
from folium.plugins import MarkerCluster
import pandas as pd

def create_weather_geomap(weather_df: pd.DataFrame, save_path="weather_map.html"):
    """
    根据天气数据创建交互式地图
    weather_df: 包含城市天气数据的 DataFrame
    save_path: 地图保存路径
    """
    column_mapping = {
        "lat": "latitude",
        "lon": "longitude",
        "name": "city",
        "temperature": "temperature_c",
        "weather_descriptions": "weather_description"
    }
    weather_df.rename(columns=column_mapping, inplace=True)

    # 转换列为数值类型
    weather_df["latitude"] = pd.to_numeric(weather_df["latitude"], errors="coerce")
    weather_df["longitude"] = pd.to_numeric(weather_df["longitude"], errors="coerce")

    # 检查必要的列
    required_columns = {"latitude", "longitude", "city"}
    if not required_columns.issubset(set(weather_df.columns)):
        raise ValueError(f"数据缺少必要的列，请检查: {required_columns - set(weather_df.columns)}")

    # 初始化地图
    center_lat = weather_df["latitude"].mean()
    center_lon = weather_df["longitude"].mean()
    weather_map = folium.Map(location=[center_lat, center_lon], zoom_start=3)

    # 使用 MarkerCluster 聚合点
    marker_cluster = MarkerCluster().add_to(weather_map)

    # 遍历数据并添加标记
    for _, row in weather_df.iterrows():
        popup_info = (
            f"<b>City:</b> {row['city']}<br>"
            f"<b>Temperature:</b> {row.get('temperature_c', 'N/A')}°C<br>"
            f"<b>Weather:</b> {row.get('weather_description', 'N/A')}<br>"
        )
        icon_color = "red" if row.get("temperature_c", 0) > 30 else "blue"  # 根据温度改变标记颜色
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=popup_info,
            icon=folium.Icon(color=icon_color, icon="cloud")
        ).add_to(marker_cluster)

    # 保存地图
    weather_map.save(save_path)