import requests
from tkinter import ttk
import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbControl import Weather_data

engine = create_engine("sqlite:///weather.db")
Session = sessionmaker(bind=engine)
session = Session()


def weather(event):
    #orų API
    city = city_cb.get()

    url = "http://api.openweathermap.org/data/2.5/find?q={}&units=metric&lang=lt&appid=8fffae095fb4ca5e0e20135b03f3b477".format(city)
    notations = requests.get(url)
    output = notations.json()


    #kintamūjų gavimas is json failo
    temperature = output["list"][0]['main']['temp']
    humidity = output["list"][0]['main']['humidity']
    wind_speed=output["list"][0]['wind']['speed']
    feels_like=output["list"][0]['main']['feels_like']
    description=output["list"][0]['weather'][0]['description']

    #database

    weather_now = Weather_data(city, temperature, humidity, wind_speed, description)
    session.add(weather_now)
    session.commit()


    temperature_label.configure(text="Temperatūra: " + str(temperature) + "°C")
    humidity_label.configure(text="Dregmė: " + str(humidity) + "%")
    wind_speed_label.configure(text="Vėjo greitis:" + str(wind_speed) + "m/s")
    feels_like_label.configure(text="Pojūtis: " + str(feels_like) + "°C")
    description_label.configure(text=description.title())

    #nekuriam tabu be reikalo
    if city in used_names:
        pass
    else:
        global count
        new_tab.append(ttk.Frame(tabs))
        # new_tab[count]= ttk.Frame(tabs)
        tabs.add(new_tab[count], text=city)
        tabs.pack()
        main.geometry('900x500')
        used_names.append(city)


    #TreeW
    columns = ("temperature", "humidity", "wind_speed", "fix_time")
    tree = ttk.Treeview(new_tab[count], columns=columns, show="headings")

    tree.heading("temperature", text="Temperatūra °C")
    tree.heading("humidity", text="Dregmė %")
    tree.heading("wind_speed", text="Vėjo greitis m/s")
    tree.heading("fix_time", text="Data")
    tree.pack()

    #pasiimam duombaze
    data = []
    weather_db = session.query(Weather_data).filter_by(city=city).all()

    #pildom lentele
    for wt in weather_db:
        data.append(f"{wt.temperature} {wt.humidity}  {wt.wind_speed}  {wt.fix_date}")

    for line in data:
        tree.insert('', tk.END, values=line)

    count = count +1




#Tkinter nustatymai
count = 0
new_tab =[]
used_names = []
main = tk.Tk()
main.title("Orai")
main.geometry('900x200')
main.iconbitmap(r"Weather.ico")
main.resizable(False, False)
selection_label = tk.Label(text="Pasirinkite iš esamų, arba įrašykite savo miestą:")
selection_label.pack()
city_name_list = ["Vilnius", "Kaunas", "Klaipeda", "Šiauliai"]
selected_city = tk.StringVar()
city_cb = ttk.Combobox(main, textvariable=selected_city)
city_cb['values'] = city_name_list


city_cb.bind("<<ComboboxSelected>>", weather)
city_cb.bind("<Return>", weather)



city_cb.pack()

temperature_label = ttk.Label(main)
temperature_label.pack()

humidity_label = ttk.Label(main)
humidity_label.pack()

wind_speed_label = ttk.Label(main)
wind_speed_label.pack()

feels_like_label = ttk.Label(main)
feels_like_label.pack()

description_label = ttk.Label(main)
description_label.pack()

tabs = ttk.Notebook(main)




main.mainloop()