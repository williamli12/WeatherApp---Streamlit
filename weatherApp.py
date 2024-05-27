import streamlit as st
import requests
from weatherAPI import key as aKey

#the weather api
# template url = https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}


#welcome headings and info
def welcome():
    st.title("Welcome to the Weather App!") #1st NEW
    st.write("Want to know the weather of a certain place?")
    st.write("---")

welcome()


# turning location to latitude and longitude coordinates
def generateLatLong():
    cName = st.text_input("City Name: ", value=None)
    choiceLimit = 5
    
    if cName != None:
        
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={cName}&limit={choiceLimit}&appid=" + aKey
        r = requests.get(url)
        dataList = r.json()

        cityCountry = []
        latLong = []

    
        for dicts in dataList:
            
            city = dicts["name"]
            lat = dicts["lat"]
            long = dicts["lon"]
            country = dicts["country"]

            if 'state' in dicts:
                state = dicts["state"]
                info = f"{city}, {state}, {country}"   
            else:
                info = f"{city}, {country}"

            cityCountry.append(info)
            latLong.append((lat, long))

        select = st.radio("Which city are you looking for?", cityCountry)
       # the radio returns the option selected
    
        which_lat_long = latLong[cityCountry.index(select)]
        return which_lat_long
        #go = st.button("Go")
        #if go:
    # lat_long = ()
    # for i in latLong:
    #     if i[0] == select:
    #         lat_long += (i[1], i[2])
    # st.write(f"{lat_long}")



#userInput + generating weather info
def userInput():
    answer = ["Input my own latitude and longitude please!", "Show me some selection!", "Input my own city please!"]
    question = st.radio("Do you want to input your own coordinates or choose a random city or input your own city?", answer, index=None)

    if question == answer[0]:
        lat = st.number_input("Enter the location's latitude")  #2nd NEW
        long = st.number_input("Enter the location's longitude")

    elif question == answer[1]:
        randomCities = ["Atlanta", "Los Angeles", "Nashville", "Seattle", "London", "Dubai", "Beijing", "Tokyo", "Rio de Janeiro"]
        randomSelection = st.radio("Here are a few cities if you do not know the exact latitude longitude.", randomCities) #NEW

        if randomSelection == randomCities[0]:
            lat = 33.75
            long = -84.39
        elif randomSelection == randomCities[1]:
            lat = 34.05
            long = -118.24
        elif randomSelection == randomCities[2]:
            lat = 36.17
            long = -86.76
        elif randomSelection == randomCities[3]:
            lat = 47.61
            long = -122.33
        elif randomSelection == randomCities[4]:
            lat = 51.509
            long = -0.118
        elif randomSelection == randomCities[5]:
            lat = 25.204
            long = 55.296
        elif randomSelection == randomCities[6]:
            lat = 39.916
            long = 116.383
        elif randomSelection == randomCities[7]:
            lat = 35.69
            long = 139.69
        elif randomSelection == randomCities[8]:
            lat = -22.90
            long = -43.20
    elif question == answer[2]:
        atup = generateLatLong()
        
    
    st.write("---")

    tempFormat = ["Fahrenheit", "Celsius"]
    desiredTemp = st.selectbox("Which temperature format do you prefer?", tempFormat) #3rd NEW
    enterButton = st.button("Enter") #4th NEW

    if enterButton:
        if question == answer[2]:
            lat = atup[0]
            long = atup[1]
        weatherURL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid=" + aKey
        r = requests.get(weatherURL)
        data_dict = r.json()

        st.write("---")

        #weather variables
        weatherID = str(data_dict["weather"][0]["id"])
        if weatherID[0] == "2":
            weatherID = "thunderstorm"
        elif weatherID[0] == "3":
            weatherID = "drizzle"
        elif weatherID[0] == "5":
            weatherID = "rain"
        elif weatherID[0] == "6":
            weatherID = "snow"
        elif weatherID[0] == "7":
            weatherID = "atmosphere"
        elif weatherID == "800":
            weatherID = "clear"
        elif weatherID[0] == "8":
            weatherID = "clouds"

        weatherTitle = data_dict["weather"][0]["main"]
        description = data_dict["weather"][0]["description"]
        city = data_dict["name"]

        country = ""
        if "country" in data_dict["sys"].keys():
            country = data_dict["sys"]["country"]

        tempKelvin = data_dict["main"]["temp"]
        if desiredTemp == tempFormat[0]:
            tempKelvin = (tempKelvin - 273.15) * 1.8 + 32
        elif desiredTemp == tempFormat[1]:
            tempKelvin = tempKelvin - 273.15

        humidity = data_dict["main"]["humidity"] #percentage
        visibility = (data_dict["visibility"]) * 3.28084 #in feet with max at 3280.84 feet

        windSpeed = (data_dict["wind"]["speed"]) * 2.23694 #mph
        clouds = data_dict["clouds"]["all"] #cloudiness percentage

        rain = 0 #inches for the last hour
        if "rain" in data_dict.keys():
            if "1h" in data_dict["rain"].keys():
                rain = round((data_dict["rain"]["1h"]) * 0.0393701, 2)

        snow = 0 #inches for the last hour
        if "snow" in data_dict.keys():
            if "1h" in data_dict["snow"].keys():
                snow = round((data_dict["snow"]["1h"]) * 0.0393701, 2)

        sunrise = data_dict["sys"]["sunrise"] #these two are in UNIX time so I probably wont add these
        sunset = data_dict["sys"]["sunset"]


        #Formatting the data

        st.subheader("Here is your data! Click through the different tabs!")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Location", "Description", "Temp/Humidity", "Wind/Clouds", "Rain/Snow"])

        with tab1:
            expander = st.expander(f"Location")
            if city == "Atlanta":
                expander.image("images/atlanta.jpg")
            elif city == "Los Angeles":
                expander.image("images/losangeles.jpg")
            elif city == "Beijing":
                expander.image("images/beijing.jpg")
            elif city == "Tokyo":
                expander.image("images/tokyo.jpg")
            elif city == "Seattle":
                expander.image("images/seattle.jpg")
            elif city == "Dubai":
                expander.image("images/dubai.jpg")
            elif city == "London":
                expander.image("images/london.jpg")
            elif city == "Rio de Janeiro":
                expander.image("images/rio.jpg")

            if city == "":
                expander.header("Don't know the location but...")
            else:
                expander.header(city)
            if country != "":
                expander.subheader("**Country:** " + country)
            expander.write("---")

        with tab2:
            expander = st.expander(f"What's happening?")
            expander.image(f"images/{weatherID}.jpg")
            expander.write(f"**{weatherTitle}**: {description}")
            expander.write("**Visibility:** " + str(round(visibility, 2)) + " Feet")
            expander.write("---")

        with tab3:
            expander = st.expander(f"Temperature and Humidity")
            expander.write("**Temperature:** " + str(round(tempKelvin, 2)) + " Degrees " + desiredTemp)
            expander.write("**Humidity:** " + str(humidity) + " %")
            st.progress(humidity)
            expander.write("---")

        with tab4:
            expander = st.expander(f"Wind Speed and Cloudiness")
            expander.write("**Wind Speed:** " + str(round(windSpeed, 2)) + " mph")
            expander.write("**Cloudiness:** " + str(clouds) + " %")
            st.progress(clouds)
            expander.write("---")
            

        with tab5:
            expander = st.expander(f"Is it raining? Snowing?")
            expander.write("**Rain in the last hour:** " + str(rain) + " in")
            expander.write("**Snow in the last hour:** " + str(snow) + " in")
            expander.write("---")

userInput()


