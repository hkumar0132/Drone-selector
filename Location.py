import requests
import geopy.geocoders
from geopy.geocoders import Nominatim
import sys

class location:

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        
    #This address will be replaced by the address
    #sent by the drone GPS
    
    def getLatLong(self, address = 'Raiwala'): 
        
        #Default timeout
        
        geopy.geocoders.options.default_timeout = 100
        geolocator = Nominatim(user_agent="Drone selector")      
        
        try:
            location = geolocator.geocode(address)                
        except:
            print("Internet problem, try switching on the internet")
            return (self.latitude, self.longitude)
            
        try:                    
            self.latitude = location.latitude
            self.longitude = location.longitude
        except:
            print("City not found")
            
        return (self.latitude, self.longitude)

    
    def getWeatherCond(self, address = 'Raiwala'):         #This city can be replaced by the 
                                                            #address sent by the drone GPS
        a = self.getLatLong(address)
        lat = str(int(a[0]))
        lon = str(int(a[1]))
    
        #Using api from openweathermap.org
        #to get weather condition
        #This needs access to internet
        #connection
        
        api_key = "" #removed for security purpose
        
        #get method of requests module 
        #using latitude and longitude
        #return response object 
        
        try :
            response = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lon + "&appid=" + api_key) 
        except:
            return "Connection error"
            
        x = response.json() 

        # city is not found 
        
        if x["cod"] != "404": 
            
            check = x['weather'][0]['main']  
            
            #If these conditions exist, 
            #drones can't fly
           
            if (check == 'shower rain' or 
                check == 'rain' or
                check == 'thunderstorm' or
                check == 'snow' or
                check == 'mist'):
                sys.exit('Mission abort, drones can\'t fly! Weather codition not appropriate')
            
            current_temperature = x['main']['temp']
            current_pressure = x['main']['pressure']

            weather_description = x['weather'][0]['description'] 
            
            wind_speed = x['wind']['speed']
            clouds = x['clouds']['all']            
            
        else: 
            return "City Not Found"
        
        #returning a list of paramters
        #that define weather condition
        
        return {
                "Temp" : current_temperature ,
                "Pressure" : current_pressure ,
                "Description" : weather_description ,
                "Wind_speed" : wind_speed ,
                "Clouds" : clouds,
                }

 
#For testing the functions 

"""      
l = location(0, 0)
print("getLatLong() : " + str(l.getLatLong()))
print("getWeatherCond() : " + str(l.getWeatherCond()))

"""
