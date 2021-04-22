% Global Variables
Sense_ChannelID = 1360392; 
Sense_readAPIKey = 'Z6OCAR6RU3J8HBM4'; 
Sense_writeApiKey = "87FWY64K19D0X58W";
SoilMoistureFieldID = 1;
TemperatureFieldID = 2; 
HumidityFieldID = 3; 
RainFieldID = 4;
MotorFieldID = 5;
FPFieldID = 6;
EDSFieldID = 7;
LFDFieldId = 8;
fertilzePeriod = 24 * 90;

% Get Sensor Data
SenseData = thingSpeakRead(1360392,'Fields',[1:8],'NumPoints',1,'ReadKey',Sense_readAPIKey);

% Error control
if isnan(SenseData(LFDFieldId))
    SenseData(LFDFieldId) = 0
end

% Determine Motor Status
if SenseData(SoilMoistureFieldID) == 0
    MotorPump = 1;
else
    MotorPump = 0;
end 

% Determine EDS Status
if SenseData(SoilMoistureFieldID) == 1 & SenseData(RainFieldID) == 1
    EDS = 1;
else
    EDS = 0;
end

% Determmine Fertilizer Pump Status
if SenseData(LFDFieldId) > fertilzePeriod & MotorPump == 1
    FertilizerPump = 1;
    LFD = 0;
else
    FertilizerPump = 0;
    LFD = SenseData(LFDFieldId)+1;
end

% Display the calculated value
out = [["MotorPump:",MotorPump];
        ["FertilizerPump:",FertilizerPump];
        ["EDS:",EDS];
        ["LFD:",LFD]];
disp(out);

% Update the calculated value to sense channel
flag = 1;
while flag
    try
        tStamp = datetime('now');
        thingSpeakWrite(Sense_ChannelID,'Fields',[5:8],'Values',[MotorPump,FertilizerPump,EDS,LFD],...
            'WriteKey',Sense_writeApiKey,'TimeStamp',tStamp);
        flag = 0;
    catch
        for i=1:100
        end
    end
end
    
