from flask import Flask, render_template, url_for
from datetime import datetime, timedelta
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
   tempData = Sense_Channel.queryAllDataList(2)['feeds']
   SenseData={}
   for i in range(2):
      for j in range(1,9):
         if tempData[i]["field"+str(j)] !=None:
            SenseData["field"+str(j)] = tempData[i]["field"+str(j)]
   Averages = {
      "Temperature":int(float([0 if (AvData == None or AvData == -1) else AvData["field2"]][0])),
      "Humidity":int(float([0 if (AvData == None or AvData == -1) else AvData["field3"]][0])),
      "Rainfall":int(float([0 if (AvData == None or AvData == -1) else AvData["field4"]][0])),
      "Waterusage":int(float([0 if (AvData == None or AvData == -1) else AvData["field1"]][0]))
   }
   Accutators = {
      "MotorPump":["ON" if SenseData["field5"]=='1' else ["OFF" if SenseData["field5"] == '0' else "No Data"][0]][0],
      "FertilizerPump":["ON" if SenseData["field6"]=='1' else ["OFF" if SenseData["field6"] == "0" else "No Data"][0]][0],
      "EDS":["ON" if SenseData["field7"]=='1' else ["OFF" if SenseData["field7"] == '0' else "No Data"][0]][0]
   }
   FSD = {
      "LFD":(datetime.now() - timedelta(minutes=int(SenseData["field8"]))).strftime('%d/%m/%Y'),
      "Moisture":int(float([0 if (AvData == None or AvData == -1) else AvData["field5"]][0]))
   }
   return render_template('index.html',Averages=Averages,Accutators=Accutators,FSD=FSD)

if __name__ == '__main__':
   app.run(debug=True)