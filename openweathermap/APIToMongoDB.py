import requests
# from pprint import pprint
import json
import pymongo

def insertData(thisList):
    # print("sohail")
    count = 0 
    for One_loc in thisList:
        cityName = One_loc[0]
        latitude =  One_loc[1]
        langitude = One_loc[2]
        count = count+1
        url = "https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely,current&appid=5af4c2482556ed487ddf572a2f3088c8".format(latitude,langitude)
        res = requests.post(url)
        data = res.text
        parse_json = json.loads(data)

#         create collection of city name
#         db = client[cityName]    
        collection = db[cityName]

        
        for i in range(8):
                day = parse_json['daily'][i]['temp']['day']
                min = parse_json['daily'][i]['temp']['min']
                max = parse_json['daily'][i]['temp']['max']
                night = parse_json['daily'][i]['temp']['night']
                eve = parse_json['daily'][i]['temp']['eve']
                morn = parse_json['daily'][i]['temp']['morn']
                press = parse_json['daily'][i]['pressure']
                dew = parse_json['daily'][i]['dew_point']
                windSpeed = parse_json['daily'][i]['wind_speed']
                humidity = parse_json['daily'][i]['humidity']
                cloud = parse_json['daily'][i]['clouds']
                uvi = parse_json['daily'][i]['uvi']
                sky =  parse_json['daily'][i]['weather'][0]['main']
                skky =  parse_json['daily'][i]['weather'][0]['description']

                insertData = {"id" : i ,"day temperature" : day, "min temperature" : min , "max temperature"
                :max , "night temperature" : night , "evening temperature": eve ,
                 "morning temperature": morn, "pressure" : press ,"dew point" : dew 
                 ,"windSpeed" : windSpeed , "humidity" :humidity ,"cloud":cloud,
                  "uvi index":uvi , "weather" : sky ,"sky" : skky }
                
                collection.insert_one(insertData)
                insertData.clear()


    print("Fetch weather information of total cities {}".format(count))    

    # def updateData(thisList):

if _name_ == '_main_':

    client = pymongo.MongoClient("mongodb://localhost:27017")
    f = open("F:\\FYP\cities.txt", encoding='utf-8')
    print("file open successfully")
    thisList = []
    line = f.read().splitlines() 
    for x in line:
        linee = x.split(',')
        thisList.append(linee)
    
    db = client["weatherData"] 
    insertData(thisList)
    print("data enter successfully in database")