from flask import Flask, render_template, url_for
from modules.ThingSpeak import ThingSpeak as TS

UI_Channel = TS(channelId=1364680,
                  readApi="CYKWB6EPOIRWSA3W",
                  writeApi="1VOAYPNBCQM0B3V7")
Sense_Channel = TS(channelId=1360392,
                  readApi="Z6OCAR6RU3J8HBM4",
                  writeApi="87FWY64K19D0X58W")

app = Flask(__name__,static_folder='templates')

@app.route('/')
def default():
   AvData = UI_Channel.queryAllLatest()
   SenseData = Sense_Channel.queryAllLatest()
   Averages = {
      "Temperature":int(float([0 if AvData == None else AvData["field2"]][0])),
      "Humidity":int(float([0 if AvData == None else AvData["field3"]][0])),
      "Rainfall":int(float([0 if AvData == None else AvData["field4"]][0])),
      "Waterusage":int(float([0 if AvData == None else AvData["field1"]][0]))
   }
   print(SenseData)
   Accutators = {
      "MotorPump":["No Data" if SenseData==None else ["ON" if SenseData["field5"] == "1" else "OFF"][0]][0],
      "FertilizerPump":["No Data" if SenseData==None else ["ON" if SenseData["field6"] == "1" else "OFF"][0]][0],
      "EDS":["No Data" if SenseData==None else ["ON" if SenseData["field7"] == "1" else "OFF"][0]][0]
   }
   FSD = {
      "LFD":"20/06/2021",
      "Moisture":36
   }
   return render_template('index.html',Averages=Averages,Accutators=Accutators,FSD=FSD)

if __name__ == '__main__':
   app.run(debug=True)