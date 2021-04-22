RainFactor = 1/5000;
WaterFactor = 1/500;

Sense_ChannelID = 1360392; 
Sense_readAPIKey = 'Z6OCAR6RU3J8HBM4'; 
Sense_writeApiKey = "87FWY64K19D0X58W";
SoilMoistureFieldID = 1;
TemperatureFieldID = 2; 
HumidityFieldID = 3; 
RainFieldID = 4;
MotorFieldID = 5;

UI_ChannelId = 1364680;
UI_writeApiKey = "1VOAYPNBCQM0B3V7";
UI_readAPIKey = 'CYKWB6EPOIRWSA3W'; 
AvgWaterFieldID = 1;
AvgTemperatureFieldID = 2; 
AvgHumidityFieldID = 3; 
AvgRainFieldID = 4; 

while 1
    % Read and calculate avg. Temperature
    tempF = thingSpeakRead(Sense_ChannelID,'Fields',TemperatureFieldID,'numDays',1, ...
        'ReadKey',Sense_readAPIKey); 
    avgTemp = round(mean(tempF,'omitnan'));

    % Read and calculate avg. Humidity
    hum = thingSpeakRead(Sense_ChannelID,'Fields',HumidityFieldID,'numDays',1, ...
        'ReadKey',Sense_readAPIKey); 
    avgHum = round(mean(hum,'omitnan'));

    % Read and calculate avg. rainfall
    soil = thingSpeakRead(Sense_ChannelID,'Fields',SoilMoistureFieldID,'numDays',30, ...
        'ReadKey',Sense_readAPIKey); 
    rain = thingSpeakRead(Sense_ChannelID,'Fields',RainFieldID,'numDays',30, ...
        'ReadKey',Sense_readAPIKey); 
    AreaRain = trapz(rmmissing(rain.*soil));
    AverageRainFall = AreaRain * RainFactor/30;

    % Read and calculate avg. water usage
    motor = thingSpeakRead(Sense_ChannelID,'Fields',MotorFieldID,'numDays',30, ...
        'ReadKey',Sense_readAPIKey); 
    AverageWaterUsage = trapz(rmmissing(motor))*WaterFactor/30;
    
    % Display the calculated value
    out = [["Avg. Temperature:",avgTemp];
            ["Avg. Humidity:",avgHum];
            ["Avg. RainFall:",AverageRainFall];
            ["Avg. WaterUsage:",AverageWaterUsage]];
    disp(out);
    
    % Update the calculated value to interface channel
    tStamp = datetime('now');
    thingSpeakWrite(UI_ChannelId,'Fields',[AvgTemperatureFieldID,AvgHumidityFieldID,AvgRainFieldID,AvgWaterFieldID], ...
        'Values',[avgTemp,avgHum,AverageRainFall,AverageWaterUsage],'WriteKey',UI_writeApiKey,'TimeStamp',tStamp);
    
    pause(300);
end