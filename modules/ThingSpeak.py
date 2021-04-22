import requests 
class ThingSpeak:
    def __init__(self,channelId,readApi,writeApi):
        self.channelId = channelId
        self.readApi = readApi
        self.writeApi = writeApi
    def queryDataList(self,FieldId,result=1):
        url = "https://api.thingspeak.com/channels/"+str(self.channelId)+"/fields/"+str(FieldId)+".json"
        ReadHeader = {
            "api_key":self.readApi,
            "results":result
        }
        try:
            req = requests.get(url, params=ReadHeader)
            return req.json()["feeds"]
        except:
            return None    
    def queryAllDataList(self,result=1):
        url = "https://api.thingspeak.com/channels/"+str(self.channelId)+"/feeds.json"
        ReadHeader = {
            "api_key":self.readApi,
            "results":result
        }
        try:
            req = requests.get(url, params=ReadHeader)
            return req.json()
        except:
            return None
    def queryLatest(self,FieldId):
        url = "https://api.thingspeak.com/channels/"+str(self.channelId)+"/fields/"+str(FieldId)+"/last.json"
        ReadHeader = {
            "api_key":self.readApi,
        }
        try:
            req = requests.get(url, params=ReadHeader)
            return int(float(req.json()["field"+str(FieldId)]))
        except:
            return -1
    def queryAllLatest(self):
        url = "https://api.thingspeak.com/channels/"+str(self.channelId)+"/feeds/last.json"
        ReadHeader = {
            "api_key":self.readApi,
        }
        try:
            req = requests.get(url, params=ReadHeader)
            return req.json()
        except:
            return None

"""
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

def UpdateMotorPump(WriteApi,MotorPump):
  WriteHeader = {
      "api_key":WriteApi,
      "field5":MotorPump
  }
  req = requests.get('https://api.thingspeak.com/update', params=WriteHeader)
  return req

def UpdateFertilizerPump(WriteApi,FertilizerPump):
  WriteHeader = {
      "api_key":WriteApi,
      "field6":FertilizerPump
  }
  req = requests.get('https://api.thingspeak.com/update', params=WriteHeader)
  return req

def UpdateEDS(WriteApi,EDS):
  WriteHeader = {
      "api_key":WriteApi,
      "field7":EDS
  }
  req = requests.get('https://api.thingspeak.com/update', params=WriteHeader)
  return req
"""
