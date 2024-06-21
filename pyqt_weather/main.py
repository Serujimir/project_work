from datetime import datetime


def default_weather(lat, lon, api_key, lang="ru", units="metric"):
    try:
        response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&lang={lang}&units={units}").json()
        print(response)
        if response["cod"] == 200:

            coord = response["coord"]
            lon = coord["lon"]
            lat = coord["lat"]

            weather = response["weather"][0]
            description = weather["description"]
            icon = weather["icon"]

            main = response["main"]
            temp = main["temp"]
            feels_like = main["feels_like"]
            temp_min = main["temp_min"]
            temp_max = main["temp_max"]
            pressure = main["pressure"]
            humidity = main["humidity"]

            wind = response["wind"]
            speed = wind["speed"]
            deg = wind["deg"]
            try:
                gust = wind["gust"]
            except KeyError:
                gust = 0

            clouds = response["clouds"]["all"]

            dt = datetime.fromtimestamp(response["dt"]).strftime("%Y-%m-%d %H:%M:%S")

            sys = response["sys"]
            country = sys["country"]
            sunrise = datetime.fromtimestamp(sys["sunrise"]).strftime("%Y-%m-%d %H:%M:%S")
            sunset = datetime.fromtimestamp(sys["sunset"]).strftime("%Y-%m-%d %H:%M:%S")

            name = response["name"]

            cloud_data = {"lon": lon, "lat": lat, "description": description, "icon": icon,
                          "temp": temp, "feels_like": feels_like, "temp_min": temp_min,
                          "temp_max": temp_max, "pressure": pressure, "humidity": humidity,
                          "speed": speed, "deg": deg, "gust": gust, "clouds": clouds,
                          "dt": dt, "country": country, "sunrise": sunrise,
                          "sunset": sunset, "name": name}
            print(cloud_data)
            return cloud_data

        else:
            return None
    except requests.ConnectionError:
        return None


import sqlite3
import sys

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication,
                             QWidget,
                             QHBoxLayout,
                             QVBoxLayout,
                             QListWidget,
                             QListWidgetItem,
                             QPushButton,
                             QLineEdit,
                             QLabel,
                             QDialog, QMessageBox)

API_KEY = "649e85619e0c093b2c96235769749579"
SEARCH_CITY_LIMIT = 5


def has_internet_connection():
    try:
        requests.head("http://yandex.ru/")
        return True
    except requests.ConnectionError:
        return False


class MainWindow(QWidget):
    stylesheet = (
        "QPushButton {background-color: #ED6A5A; border: 1px solid #000000; border-radius: 5px; padding: 10px 20px; font-family: Arial; font-size: 18px;}"
        "QPushButton:hover {background-color: #f4f1bb;}"
        "QListWidget {background-color: #E6EBE0; border: 1px solid #000000; border-radius: 5px; font-family: Arial; font-size: 18px}"
        "QListWidget::item {background-color: #ffa600; padding: 5px; margin: 5px;}"
        "QListWidget::item:selected {background-color: #ffa600; padding: 3px; margin: 2px; color: #FFFFFF; outline: 0;}"
        "QLineEdit {background-color: #ffd380; border: 1px solid #000000; border-radius: 5px; padding: 10px; font-family: Arial; font-size: 18px}"
        "QLineEdit:hover {background-color: #FFFFFF;}"
        "QLabel {font-family: Arial; font-size: 18px;}"
        "QLabel#image_icon {background-color: #ffa600; text-align: center; margin: auto; border: 1px solid #000000; border-radius: 25px;}"
        "QLabel#weatherParameter {border: 1px solid #000000; border-radius: 5px; padding: 10px; background-color: #299328; color: #FFFFFF}"
        "QWidget#weatherParameters {border: 1px solid #000000; border-radius: 5px; background-color: #d6e6ff;}"
    )

    def __init__(self):
        super().__init__()
        _id = QFontDatabase.addApplicationFont("Salwey.ttf")

        self.con = self.set_up_database()
        self.set_up_ui()
        self.currentCityData = None

    def set_up_ui(self):

        self.setWindowTitle("Погода СеИва")
        self.setWindowIcon(QIcon(QPixmap("icons/icon.png")))
        self.resize(self.screen().geometry().width() - 200, self.screen().geometry().height() - 200)

        self.mainLayout = QHBoxLayout(self)

        # self.setStyleSheet(self.stylesheet)

        self.citiesListWidget = QWidget()
        self.citiesListWidget.setMaximumWidth(self.width() // 3)
        self.citiesListWidget.setMinimumWidth(self.width() // 6)
        self.citiesListWidgetLayout = QVBoxLayout(self.citiesListWidget)
        # self.citiesText = QLabel("Мои места:")
        # self.citiesText.setAlignment(Qt.AlignCenter)

        self.citiesList = QListWidget()
        self.citiesSearchText = QLabel("Поиск:")
        self.citiesSearch = QLineEdit()

        self.citiesBtnAdd = QPushButton("Добавить")
        self.citiesBtnDel = QPushButton("Удалить")
        self.citiesBtnSavedWeather = QPushButton("Сохранённые прогнозы")

        # self.citiesListWidgetLayout.addWidget(self.citiesText)
        self.citiesListWidgetLayout.addWidget(self.citiesList)
        self.citiesListWidgetLayout.addWidget(self.citiesSearchText)
        self.citiesListWidgetLayout.addWidget(self.citiesSearch)
        self.citiesListWidgetLayout.addWidget(self.citiesBtnAdd)
        self.citiesListWidgetLayout.addWidget(self.citiesBtnDel)
        self.citiesListWidgetLayout.addWidget(self.citiesBtnSavedWeather)

        self.mainView = QVBoxLayout()
        self.mainView.setAlignment(Qt.AlignTop)

        self.weatherParametersWidget = QWidget()
        self.weatherParametersWidget.setObjectName("weatherParameters")

        self.weatherParametersWidgetLayout = QHBoxLayout(self.weatherParametersWidget)
        self.weatherParametersWidgetLayout.setAlignment(Qt.AlignTop)

        self.weatherIcon = QLabel()
        self.weatherIcon.setAlignment(Qt.AlignCenter)
        self.weatherIcon.setObjectName("image_icon")
        image = QPixmap("icons/01d.png").scaled(256, 256, Qt.KeepAspectRatio)
        self.weatherIcon.setPixmap(image)

        self.weatherParameters = QVBoxLayout()

        self.weatherActual = QLabel("Актуально на: ")
        self.weatherActual.setObjectName("weatherParameter")

        self.weatherCity = QLabel("Город: ")
        self.weatherCity.setObjectName("weatherParameter")

        self.weatherPlace = QLabel("Место: ")
        self.weatherPlace.setObjectName("weatherParameter")

        self.weatherCountry = QLabel("Страна: ")
        self.weatherCountry.setObjectName("weatherParameter")

        self.weatherTemp = QLabel("Температура: ")
        self.weatherTemp.setObjectName("weatherParameter")

        self.weatherDescription = QLabel("Описание погоды: ")
        self.weatherDescription.setObjectName("weatherParameter")

        self.weatherPressure = QLabel("Давление: ")
        self.weatherPressure.setObjectName("weatherParameter")

        self.weatherHumidity = QLabel("Влажность: ")
        self.weatherHumidity.setObjectName("weatherParameter")

        self.weatherSpeed = QLabel("Скорость ветра: ")
        self.weatherSpeed.setObjectName("weatherParameter")

        self.weatherClouds = QLabel("Облачность в %: ")
        self.weatherClouds.setObjectName("weatherParameter")

        self.weatherSunrise = QLabel("Восход: ")
        self.weatherSunrise.setObjectName("weatherParameter")

        self.weatherSunset = QLabel("Закат: ")
        self.weatherSunset.setObjectName("weatherParameter")

        self.weatherLat = QLabel("Широта: ")
        self.weatherLat.setObjectName("weatherParameter")

        self.weatherLon = QLabel("Долгота: ")
        self.weatherLon.setObjectName("weatherParameter")

        self.weatherSaveBtn = QPushButton("Сохранить прогноз")
        self.weatherSaveBtn.setObjectName("weatherParameterBtn")

        self.weatherParameters.addWidget(self.weatherActual)
        self.weatherParameters.addWidget(self.weatherCity)
        self.weatherParameters.addWidget(self.weatherPlace)
        self.weatherParameters.addWidget(self.weatherCountry)
        self.weatherParameters.addWidget(self.weatherTemp)
        self.weatherParameters.addWidget(self.weatherDescription)
        self.weatherParameters.addWidget(self.weatherPressure)
        self.weatherParameters.addWidget(self.weatherHumidity)
        self.weatherParameters.addWidget(self.weatherSpeed)
        self.weatherParameters.addWidget(self.weatherClouds)
        self.weatherParameters.addWidget(self.weatherSunrise)
        self.weatherParameters.addWidget(self.weatherSunset)
        self.weatherParameters.addWidget(self.weatherLat)
        self.weatherParameters.addWidget(self.weatherLon)
        self.weatherParameters.addWidget(self.weatherSaveBtn)

        self.weatherParametersWidgetLayout.addWidget(self.weatherIcon)
        self.weatherParametersWidgetLayout.addLayout(self.weatherParameters)

        self.mainView.addWidget(self.weatherParametersWidget)

        self.mainLayout.addWidget(self.citiesListWidget)
        self.mainLayout.addLayout(self.mainView)

        self.is_first_selection = True

        self.load_my_cities()
        self.get_first_city()

        self.citiesBtnAdd.clicked.connect(self.add_city_dialog)
        self.citiesList.itemDoubleClicked.connect(self.setCity)
        self.citiesBtnDel.clicked.connect(self.btnDelTrigger)
        self.citiesSearch.textChanged.connect(self.searchCity)
        self.citiesBtnSavedWeather.clicked.connect(self.show_saved_weather)
        self.weatherSaveBtn.clicked.connect(self.saveWeather)

    def delete_saved_weather(self, city_name, country, dt):
        try:
            cur = self.con.cursor()
            cur.execute(
                f"DELETE FROM saved_weather WHERE (name=\"{city_name}\" OR city=\"{city_name}\") AND country=\"{country}\" AND dt=\"{dt}\"")
            self.con.commit()
            return True
        except Exception as e:
            self.show_saved_weather(f"Произошла неизвестная ошибка:\n{e}")
            return False

    def show_saved_weather(self):
        try:
            self.is_first_selection = True
            savedCities = QDialog(self)
            savedCities.resize(500, 600)
            savedCities.setWindowFlag(Qt.WindowStaysOnTopHint)
            savedCities.setWindowTitle("Сохранённые прогнозы")
            savedCities.setWindowIcon(QIcon(QPixmap("icons/icon.png")))
            layout = QVBoxLayout()

            def load_saved_weather():
                savedCitiesList.clear()
                cur = self.con.cursor()
                data = cur.execute("SELECT * FROM saved_weather").fetchall()
                for i in data:
                    city = i[-1]
                    actual = i[12]
                    country = i[13]
                    item = QListWidgetItem(f"{city} | {country} | Актуально на {actual}")
                    savedCitiesList.addItem(item)

            def prepareForLoad(item: QListWidgetItem):
                text = item.text()
                parse = text.split(" | ")
                city_name = parse[0]
                country = parse[1]
                dt = text.split("Актуально на ")[-1]
                self.load_city_weather(0, 0, "", True, city_name, dt, country)
                savedCities.close()

            def item_tyk():
                self.is_first_selection = False

            def prepareForDelete():
                if not self.is_first_selection:
                    try:
                        text = savedCitiesList.currentItem().text()
                        parse = text.split(" | ")
                        city_name = parse[0]
                        country = parse[1]
                        dt = text.split("Актуально на ")[-1]
                        if self.delete_saved_weather(city_name, country, dt):
                            load_saved_weather()
                    except AttributeError:
                        self.show_error_dialog("Выберите прогноз для удаления!")
                    except Exception as e:
                        self.show_error_dialog(f"Неизвестная ошибка:\n{e}")
                else:
                    self.show_error_dialog("Выберите прогноз для удаления!")

            savedCitiesList = QListWidget()
            savedCitiesBtnDel = QPushButton("Удалить сохранённый прогноз")
            layout.addWidget(savedCitiesList)
            layout.addWidget(savedCitiesBtnDel)
            savedCities.setLayout(layout)

            load_saved_weather()
            savedCitiesList.itemDoubleClicked.connect(prepareForLoad)
            savedCitiesBtnDel.clicked.connect(prepareForDelete)
            savedCitiesList.itemClicked.connect(item_tyk)

            savedCities.show()
        except Exception as e:
            print(e)

    def saveWeather(self):

        def is_duplicate(city_name, dt, country):
            cur = self.con.cursor()
            count = cur.execute(
                f"SELECT COUNT() FROM saved_weather WHERE city=\"{city_name}\" AND dt=\"{dt}\" AND country=\"{country}\"").fetchone()[
                0]
            if count == 0:
                return False
            elif count >= 1:
                return True

        city_name = self.weatherCity.text().split(": ")[-1]
        if len(city_name) >= 2:
            if self.currentCityData is not None:
                try:
                    data = self.currentCityData
                    if not is_duplicate(city_name, data["dt"], data["country"]):
                        cur = self.con.cursor()
                        query_add_weatherData = '''
                        INSERT OR IGNORE INTO saved_weather(lon, lat, description, icon, temp, feels_like, pressure, humidity,
                         speed, gust, clouds, dt, country, sunrise, sunset, name, city) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                         ?)
                        '''
                        cur.execute(query_add_weatherData, [data["lon"], data["lat"], data["description"],
                                                            data["icon"], data["temp"], data["feels_like"],
                                                            data["pressure"], data["humidity"], data["speed"],
                                                            data["gust"],
                                                            data["clouds"], data["dt"], data["country"],
                                                            data["sunrise"],
                                                            data["sunset"], data["name"], city_name])
                        self.con.commit()
                        self.show_error_dialog("Успешно сохранено!")
                        return
                    else:
                        self.show_error_dialog("Такой прогноз уже сохранён!")
                        return
                except Exception as e:
                    self.show_error_dialog("Ошибка при сохранении прогноза погоды")
                    return

    def searchCity(self):
        if len(self.citiesSearch.text()) >= 1:
            self.load_my_cities(self.citiesSearch.text())
        else:
            self.load_my_cities()

    def load_my_cities(self, text=""):
        self.citiesList.clear()
        cur = self.con.cursor()

        data = cur.execute(
            f"SELECT name, country, ru_name, state FROM cities WHERE LOWER(name) LIKE LOWER(\"{text}%\") or LOWER(ru_name) LIKE LOWER(\"{text}%\")").fetchall()

        for i in data:
            ru = i[2]
            if len(ru) >= 1:
                item = QListWidgetItem(f"{ru} | {i[1]} | {i[3]}")
            else:
                item = QListWidgetItem(f"{i[0]} | {i[1]} | {i[3]}")
            self.citiesList.addItem(item)

        print(data)

    def get_first_city(self):
        if has_internet_connection():
            print("Есть")
            cur = self.con.cursor()
            data = cur.execute("SELECT lat, lon, name, ru_name FROM cities LIMIT 1").fetchone()
            if data is not None and len(data) >= 1:
                if len(data[3]) >= 1:
                    name = data[3]
                else:
                    name = data[2]
                self.load_city_weather(data[0], data[1], name)

    def getCityInfoFromDB(self, name, country):
        cur = self.con
        if has_internet_connection():
            try:
                data = cur.execute(
                    f"SELECT lat, lon, name, ru_name FROM cities WHERE (name=\"{name}\" OR ru_name=\"{name}\") AND country=\"{country}\"").fetchone()
                print(data)
                if len(data[3]) >= 1:
                    name = data[3]
                else:
                    name = data[2]
                self.load_city_weather(data[0], data[1], name)
            except Exception as e:
                self.show_error_dialog(f"Неизвестная ошибка:\n{e}")
        else:
            self.show_error_dialog("Нет подключения к сети!")

    def setCity(self):
        try:
            index = self.citiesList.currentRow()
            parse = self.citiesList.item(index).text().split(" | ")
            city = parse[0]
            country = parse[1]
            self.getCityInfoFromDB(city, country)
        except Exception as e:
            self.show_error_dialog(f"Неизвестная ошибка:\n{e}")

    def load_city_weather(self, lat, lon, name, saved=False, saved_city="", saved_dt="", saved_country=""):

        self.weatherActual.setText("Актуально на: ")
        self.weatherCity.setText("Город: ")
        self.weatherPlace.setText("Место: ")
        self.weatherCountry.setText("Страна: ")
        self.weatherTemp.setText("Температура: ")
        self.weatherDescription.setText("Описание погоды: ")
        self.weatherPressure.setText("Давление: ")
        self.weatherHumidity.setText("Влажность: ")
        self.weatherSpeed.setText("Скорость ветра: ")
        self.weatherClouds.setText("Облачность: ")
        self.weatherSunrise.setText("Восход: ")
        self.weatherSunset.setText("Закат: ")
        self.weatherLat.setText("Широта: ")
        self.weatherLon.setText("Долгота: ")

        def set_icon(icon):
            pixmap = QPixmap("icons/01d.png")

            if icon == "01d":
                pixmap = QPixmap("icons/01d.png")
            elif icon == "02d":
                pixmap = QPixmap("icons/02d.png")
            elif icon == "03d":
                pixmap = QPixmap("icons/03d.png")
            elif icon == "04d":
                pixmap = QPixmap("icons/04d.png")
            elif icon == "09d":
                pixmap = QPixmap("icons/09d.png")
            elif icon == "10d":
                pixmap = QPixmap("icons/10d.png")
            elif icon == "11d":
                pixmap = QPixmap("icons/11d.png")
            elif icon == "13d":
                pixmap = QPixmap("icons/13d.png")
            elif icon == "50d":
                pixmap = QPixmap("icons/50d.png")

            self.weatherIcon.setPixmap(pixmap)

        if saved:
            try:
                cur = self.con.cursor()
                data = cur.execute(
                    f"SELECT * FROM saved_weather WHERE city=\"{saved_city}\" AND dt=\"{saved_dt}\" AND country=\"{saved_country}\" LIMIT 1").fetchone()

                if len(data) >= 1:
                    self.weatherActual.setText(f"Актуально на: {data[12]}")
                    self.weatherCity.setText(f"Город: {data[-1]}")
                    self.weatherPlace.setText(f"Место: {data[16]}")
                    self.weatherCountry.setText(f"Страна: {data[13]}")
                    self.weatherTemp.setText(f"Температура: {data[5]} ({data[6]})")
                    self.weatherDescription.setText(f"Описание погоды: {data[3]}")
                    self.weatherPressure.setText(f"Давление: {data[7]}")
                    self.weatherHumidity.setText(f"Влажность: {data[8]}%")
                    self.weatherSpeed.setText(f"Скорость ветра: {data[9]} (до {data[10]})")
                    self.weatherClouds.setText(f"Облачность: {data[11]}%")
                    self.weatherSunrise.setText(f"Восход: {data[16]}")
                    self.weatherSunset.setText(f"Закат: {data[17]}")
                    self.weatherLat.setText(f"Широта: {data[2]}")
                    self.weatherLon.setText(f"Долгота: {data[1]}")
                    icon = data[4]
                    set_icon(icon)
            except Exception as e:
                print(e)

            return
        self.currentCityData = None
        try:
            data = default_weather(lat, lon, API_KEY)
            self.currentCityData = data

            if data is not None:
                self.weatherActual.setText(f"Актуально на: {data["dt"]}")
                self.weatherCity.setText(f"Город: {name}")
                self.weatherPlace.setText(f"Место: {data["name"]}")
                self.weatherCountry.setText(f"Страна: {data["country"]}")
                self.weatherTemp.setText(f"Температура: {data["temp"]} ({data["feels_like"]})")
                self.weatherDescription.setText(f"Описание погоды: {data["description"]}")
                self.weatherPressure.setText(f"Давление: {data["pressure"]}")
                self.weatherHumidity.setText(f"Влажность: {data["humidity"]}%")
                self.weatherSpeed.setText(f"Скорость ветра: {data["speed"]} (до {data["gust"]})")
                self.weatherClouds.setText(f"Облачность: {data["clouds"]}%")
                self.weatherSunrise.setText(f"Восход: {data["sunrise"]}")
                self.weatherSunset.setText(f"Закат: {data["sunset"]}")
                self.weatherLat.setText(f"Широта: {data["lat"]}")
                self.weatherLon.setText(f"Долгота: {data["lon"]}")

                icon = data["icon"]
                set_icon(icon)




            else:
                self.show_error_dialog("Не удалось получить данные о городе!")

        except Exception as e:
            self.show_error_dialog(f"Неизвестная ошибка:\n{e}")

    def set_up_database(self):
        try:
            con = sqlite3.connect("cities.db")
            cur = con.cursor()

            query_cities = '''
            CREATE TABLE IF NOT EXISTS cities(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                lat REAL NOT NULL,
                lon REAL NOT NULL,
                country TEXT NOT NULL,
                ru_name TEXT,
                state TEXT
            )'''

            query_saved_weather = '''
            CREATE TABLE IF NOT EXISTS saved_weather(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lon REAL NOT NULL,
                lat REAL NOT NULL,
                description TEXT,
                icon TEXT NOT NULL,
                temp REAL NOT NULL,
                feels_like REAL,
                pressure INTEGER,
                humidity INTEGER,
                speed REAL,
                gust REAL,
                clouds INTEGER,
                dt TEXT NOT NULL,
                country TEXT,
                sunrise TEXT,
                sunset TEXT,
                name TEXT,
                city TEXT NOT NULL
            )'''

            cur.execute(query_cities)
            cur.execute(query_saved_weather)
            con.commit()

            return con
        except Exception as e:
            print(f"Ошибка во время инициализации базы данных:\n{e}")

    # Don't release
    def update_city_info(self, id, new_name):
        try:
            cur = self.con.cursor()
            cur.execute(f"UPDATE cities SET ru_name=\"{new_name}\" WHERE id={id}")
        except Exception as e:
            self.show_error_dialog(f"Произошла ошибка:\n{e}")
        self.con.commit()

    def search_city_by_name(self, name):
        if has_internet_connection():
            try:
                response = requests.get(
                    f"http://api.openweathermap.org/geo/1.0/direct?q={name}&limit={SEARCH_CITY_LIMIT}&appid={API_KEY}").json()

                data = []

                for i in response:
                    name = i["name"]
                    lat = i["lat"]
                    lon = i["lon"]
                    country = i["country"]
                    try:
                        ru_name = i["local_names"]["ru"]
                        state = i["state"]
                    except Exception:
                        ru_name = ""
                        state = ""

                    city = (name, lat, lon, country, ru_name, state)
                    data.append(city)
                return data
            except:
                return None
        else:
            self.show_error_dialog("Нет подключения к сети!")

    def add_city_dialog(self):
        if has_internet_connection():
            self.dialog = QDialog()
            self.dialog.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.dialog.setFixedSize(400, 250)
            self.dialog.setWindowTitle("Добавление города")
            self.dialog.setWindowIcon(QIcon(QPixmap("icons/icon.png")))

            self.dialogLayout = QVBoxLayout()

            self.searchLayout = QHBoxLayout()
            self.searchCityName = QLineEdit()
            self.searchCityBtn = QPushButton("Искать")
            self.searchLayout.addWidget(self.searchCityName)
            self.searchLayout.addWidget(self.searchCityBtn)

            self.searchCityList = QListWidget()

            self.dialogLayout.addLayout(self.searchLayout)
            self.dialogLayout.addWidget(self.searchCityList)

            self.dialog.setLayout(self.dialogLayout)

            data = []
        else:
            self.show_error_dialog("Нет подключения к сети!")
            return

        def load_list():
            global data
            self.searchCityList.clear()
            if len(self.searchCityName.text()) >= 1:
                if has_internet_connection():
                    data = self.search_city_by_name(self.searchCityName.text())

                    if len(data) >= 1:
                        for i in data:
                            print(i)
                            ru_name = i[4]
                            state = i[5]
                            if len(ru_name) >= 1 and len(state) >= 1:
                                item = QListWidgetItem(f"{ru_name} | {i[3]} | {state}")
                            else:
                                item = QListWidgetItem(f"{i[0]} | {i[3]}")
                            self.searchCityList.addItem(item)

                        self.searchCityList.itemDoubleClicked.connect(saveCityDialog)
                    else:
                        self.show_error_dialog("Город не найден!")
                        return
                else:
                    self.show_error_dialog("Нет подключения к сети!")
                    return
            else:
                self.show_error_dialog("Название города должно состоять как минимум из 1 символа!")
                return

        def saveCityDialog():
            global data

            index = self.searchCityList.currentRow()
            name = data[index][0]
            ru_name = data[index][4]
            if len(ru_name) >= 1:
                is_ru = True
            else:
                is_ru = False

            confirm = QMessageBox(self)
            confirm.setWindowFlag(Qt.WindowStaysOnTopHint)
            confirm.setWindowTitle("Сохранение города")
            confirm.setWindowIcon(QIcon(QPixmap("icons/icon.png")))
            confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            if is_ru:
                confirm.setText(f"Вы точно хотите сохранить: {ru_name}?")
            else:
                confirm.setText(f"Вы точно хотите сохранить: {name}?")

            def click(button):
                button = confirm.standardButton(button)
                if button == QMessageBox.Yes:
                    if self.save_city_to_database(data[index]):
                        self.dialog.close()
                    confirm.close()
                    return
                elif button == QMessageBox.No:
                    confirm.close()
                    return

            confirm.buttonClicked.connect(click)

            confirm.show()

        self.searchCityBtn.clicked.connect(load_list)

        self.dialog.show()

    def show_error_dialog(self, desc):
        try:
            dialog = QMessageBox(self)
            dialog.setWindowFlag(Qt.WindowStaysOnTopHint)
            dialog.setWindowTitle("Внимание!")
            dialog.setWindowIcon(QIcon(QPixmap("icons/icon.png")))
            dialog.setText(str(desc))
            dialog.show()
        except Exception as e:
            print(e)

    def save_city_to_database(self, data: tuple):
        cur = self.con.cursor()

        def is_duplicate(name, ru_name, country):
            try:
                cur = self.con.cursor()
                count = cur.execute(
                    f"SELECT COUNT() FROM cities WHERE (name=\"{name}\" OR ru_name=\"{ru_name}\") AND country=\"{country}\"").fetchone()[
                    0]
                if count == 0:
                    return False
                elif count >= 1:
                    return True
            except Exception as e:
                self.show_error_dialog(f"Ошибка при проверке дубликата в базе данных:{e}")
                return

        if not is_duplicate(data[0], data[4], data[3]):

            try:
                query_add_city = '''
                INSERT INTO cities(name, lat, lon, country, ru_name, state) VALUES(?, ?, ?, ?, ?, ?)
                '''
                cur.execute(query_add_city, [data[0], data[1], data[2], data[3], data[4], data[5]])
            except sqlite3.DatabaseError as e:
                print("1")
                self.show_error_dialog("Город с таким названием и страной уже есть!")
                return False
            except Exception as e:
                self.show_error_dialog(f"Неизвестная ошибка:\n{e}")
                return False
            self.con.commit()
            self.load_my_cities()
            return True
        else:
            print("2")
            self.show_error_dialog("Город с таким названием и страной уже есть!")
            return False

    def btnDelTrigger(self):
        if self.citiesList.currentItem() is not None:
            parse = self.citiesList.currentItem().text().split(" | ")
            city = parse[0]
            country = parse[1]
            confirm = QMessageBox.question(self, "Внимание!", f"Вы действительно хотите удалить {city}",
                                           QMessageBox.Yes, QMessageBox.No)

            if confirm == QMessageBox.Yes:
                self.delete_city_from_database(city, country)
            elif confirm == QMessageBox.No:
                print("No")

        else:
            self.alert = QMessageBox()
            self.alert.setWindowTitle("Внимание!")
            self.alert.setText("Выберите город для удаления!")
            self.alert.show()

    def delete_city_from_database(self, city_name, country):
        cur = self.con.cursor()

        try:
            cur.execute(
                f"DELETE FROM cities WHERE name=\"{city_name}\" OR ru_name=\"{city_name}\" AND country=\"{country}\"")
        except Exception as e:
            print(e)
            return False

        self.con.commit()
        self.load_my_cities()
        return True


if __name__ == '__main__':

    # Handle high resolution displays:
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyleSheet(MainWindow.stylesheet)

    main = MainWindow()
    main.show()

    sys.exit(app.exec())
