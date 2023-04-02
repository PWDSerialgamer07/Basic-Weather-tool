import requests
import colorama
from colorama import Fore
from datetime import datetime
import streamlit as st

st.title("Météo")

output1 = "data"
key = "f5cb8f71c2bf75cb34a47e04052d44ab"

city_id = st.text_input('Entrez votre ville', '')
city = "http://api.openweathermap.org/geo/1.0/direct?q=" + city_id + "&appid=" + key

output1 = requests.get(city)

if output1.status_code == 200:
    data = output1.json()
    if data:
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric&lang=fr"
        weather_data = requests.get(weather_url).json()
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        desc = weather_data['weather'][0]['description']
        local_time = datetime.utcfromtimestamp(
            weather_data['dt'] + weather_data['timezone']).strftime('%Y-%m-%d %H:%M:%S')
        st.write("La température actuelle à " + city_id + " est de " + str(temp) + "°C et le temps est " + desc +
                 ".\nLa température ressentie est de " + str(feels_like) + "°C.\nL'heure locale est " + local_time + ".")
    else:
        st.write("[ERROR] " + "Ville introuvable. " +
                 "Avez vous entrées la bonne villes?")
else:
    st.write("[ERROR] " +
             "Une erreur s'est produite. Veuillez réessayez")

theme = st.sidebar.selectbox('Thème', ['Clair', 'Sombre'])

if theme == 'Clair':
    st.markdown(
        '<style>body {background: #F7F7F7;}</style>', unsafe_allow_html=True)
elif theme == 'Sombre':
    st.markdown(
        '<style>body {background: #2F2F2F;}</style>', unsafe_allow_html=True)

if st.sidebar.checkbox('Voir plus de détails'):
    pressure = weather_data['main']['pressure']
    humidity = weather_data['main']['humidity']
    wind_speed = weather_data['wind']['speed']
    st.write(
        f"**Pression atmosphérique:** {pressure} hPa\n**Humidité:** {humidity} %\n**Vitesse du vent:** {wind_speed} m/s")
