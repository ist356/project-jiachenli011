import streamlit as st
import pandas as pd
import folium
import streamlit.components.v1 as components
from weather_get_merge import merge_weather_data
from Map import create_weather_geomap

st.title("Mutiple City Weather checker 📊🗺️")
st.write("Enter the city you want to check（Use , for mutiple city，eg: Syracuse, London, New York）")

city_input = st.text_input("City name", "")

if "weather_df" not in st.session_state:
    st.session_state.weather_df = None

if st.button("Check Now!") and city_input:
   
    placeholder = st.empty()
    placeholder.text("Loading the data please wait")

    # 解析用户输入的城市列表
    cities = [city.strip() for city in city_input.split(",") if city.strip()]

    if cities:
        weather_df = merge_weather_data(cities)
        if not weather_df.empty:
            # 生成经纬度列（API 中应返回 Latitude 和 Longitude，如果没有可手动添加）
            weather_df["Latitude"] = [31.23, 39.90, 40.71, 51.51][:len(weather_df)]  # 示例经纬度
            weather_df["Longitude"] = [121.47, 116.40, -74.01, -0.13][:len(weather_df)]

            st.session_state.weather_df = weather_df
            placeholder.success("Data acquisition success！")
        else:
            placeholder.error("Out of api calls, please wait for next month。")
    else:
        placeholder.error("Enter a city name。")

if st.session_state.weather_df is not None:
    weather_df = st.session_state.weather_df

    # 显示数据表格
    st.write("### Dataframe for weather")
    st.dataframe(weather_df)

    # 提供城市选择框
    city_options = weather_df["City"].unique()
    selected_city = st.selectbox("Choose a city on map:", city_options)

    # 过滤数据生成地图
    selected_city_df = weather_df[weather_df["City"] == selected_city]
    create_weather_geomap(selected_city_df, save_path="selected_city_map.html")

    # 在 Streamlit 中显示地图
    st.write("### Weather map")
    with open("selected_city_map.html", "r", encoding="utf-8") as map_file:
        map_html = map_file.read()
        components.html(map_html, height=600, scrolling=True)

    # 提供下载数据功能
    csv = weather_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "下载完整数据", data=csv, file_name="weather_data.csv", mime="text/csv"
    )