## Pin Configuration
SoilSensorPin = 21
RainSensorPin = 18
DHTPin = 25
MotorPin = 23
FerilizerPin = 16
EDSPin = 19
TestLEDPin = 27

# Import required libraries
import time
import requests 
import sys
#import Adafruit_DHT
import RPi.GPIO as GPIO       

# Global Variable assignment
interval = 25
ChannelId = 1360392
WriteApi = "87FWY64K19D0X58W"
ReadApi = "Z6OCAR6RU3J8HBM4"
FieldIdMap = {
    "SoilMoisture" : 1,         
    "Temperature" : 2,          
    "Humidity" : 3,           
    "Rain" : 4,           
    "MotorPump" : 5,               
    "FertilizerPump" : 6,   
    "EDS" : 7          
}

# Function Definitions
def UpdateSensors(WriteApi,SoilMoisture,Temperature,Humidity,Rain):
   WriteHeader = {
      "api_key":WriteApi,
      "field1":SoilMoisture,
      "field2":Temperature,
      "field3":Humidity,
      "field4":Rain
   }
   req = requests.get('https://api.thingspeak.com/update', params=WriteHeader)
   return req

def getData():
   url = "https://api.thingspeak.com/channels/"+str(ChannelId)+"/feeds.json"
   ReadHeader = {
      "api_key":ReadApi,
      "results":2
   }
   try:
      req = requests.get(url, params=ReadHeader)
      data = req.json()["feeds"]
      f={}
      f["field5"] = [data[0]["field5"] if data[0]["field5"] !=None else data[1]["field5"]][0]
      f["field6"] = [data[0]["field6"] if data[0]["field6"] !=None else data[1]["field6"]][0]
      f["field7"] = [data[0]["field7"] if data[0]["field7"] !=None else data[1]["field7"]][0]
      return f
   except:
      return None
      
# Pin Configuration
GPIO.setmode(GPIO.BCM)      

GPIO.setup(SoilSensorPin, GPIO.IN)  
GPIO.setup(RainSensorPin, GPIO.IN)  
GPIO.setup(DHTPin, GPIO.IN)  
GPIO.setup(MotorPin, GPIO.OUT)      
GPIO.setup(FerilizerPin, GPIO.OUT)      
GPIO.setup(EDSPin, GPIO.OUT)    
GPIO.setup(TestLEDPin, GPIO.OUT)      


state = False
while True:   
  time.sleep(1)
  try:
    #Humidity, Temperature = Adafruit_DHT.read(Adafruit_DHT.DHT11, DHTPin)
    Humidity, Temperature = (28,50)
    SoilMoisture = GPIO.input(SoilSensorPin)
    Rain = GPIO.input(RainSensorPin)
    #SoilMoisture,Rain = 2*(state,)
    print(SoilMoisture,Temperature,Humidity,Rain)

    UpdateSensors(WriteApi,SoilMoisture,Temperature,Humidity,Rain)
    print("data uploaded.")
    print("Waiting for 30 seconds for analysis program to run.....")
    time.sleep(30)

    acc = getData()
    print(acc)

    if acc != None and acc["field5"] == "1" :
      GPIO.output(MotorPin,True)
      print("MP HIGH")
    else:
      GPIO.output(MotorPin,False)   
      print("MP LOW")

    if acc != None and acc["field6"] == "1" :
      GPIO.output(FerilizerPin,True)
      print("FP HIGH")
    else:
      GPIO.output(FerilizerPin,False)
      print("FP LOW")

    if acc != None and acc["field7"] == "1" :
      GPIO.output(EDSPin,True)
      print("EDS HIGH")
    else:
      GPIO.output(EDSPin,False)
      print("EDS LOW")
  except error:
    print(error)
  finally:
    state = not state
    GPIO.output(TestLEDPin,state)
    print("------------------------------------------------------")
    print("Waiting for 30 seconds to upload next cycle.....")
    time.sleep(30)   
