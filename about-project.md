# About My Project

Student Name:  Jiachen Li
Student Email:  jli114@syr.edu

### What it does
This project I designed is a multi-city weather checker that allows users to obtain, and visualize real-time weather data for multiple cities. I used the Weatherstack API to retrieve current weather details, including temperature, humidity, wind speed, and weather description, as well as location-specific information such as city, country, and local time. Then I used Streamlit as the user interface, Pandas for data processing, and Folium for interactive map visualization.

Users are able to enter one or more city names through the Streamlit web interface. The application processes this input, obtains weather data for the selected city, and displays it in a tabular format. In addition, users can select a specific city from a drop-down menu to view its location and weather details on an interactive map, where the marker color changes dynamically based on temperature conditions, for example, red for higher temperatures and blue for lower temperatures. Finally, a CSV download function is also included, allowing users to export weather data for further analysis.

### How you run my project
data_show.py -> is the main body of project, just need to run this file with streamlit.
weather_get_merge.py -> is the file that I use to get weather data from Weatherstack API and merge it with the location data.
Map.py -> is the file that I use to create the interactive map.

### Other things you need to know
My initial plan was to use the weather API to obtain current and past data, and to show weather changes on a map by letting users select a time period. However, since the free access is for current data, and past data requires a paid upgrade, I kept the function of trying to obtain past data when writing the function. The second reason is that the free API can be used 100 times per month, and I had used it more than 50 times when testing the current API, which may result in no usage after submission, so I had to give up this plan.

Test maynot pass due to the date. Temperature always changes, need to set the new temperature in test file.