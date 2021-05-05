readChannelID = 1363129;
humiFieldID= 2;  
tempFieldID = 1;
wFieldID=3; 
readAPIKey = 'TK750DEX4Y4E5TQB';  
 
% Get humidity, temperature data for the last N minutes from the SIS
humidity = thingSpeakRead(readChannelID,'Fields',humiFieldID,'NumMinutes', 1,'ReadKey',readAPIKey); 
humidity = rmmissing(humidity);
display(humidity)
[tempF,timeStamp] = thingSpeakRead(readChannelID,'Fields',tempFieldID,'NumMinutes', 1,'ReadKey',readAPIKey); 
%moistureData = thingSpeakRead(readChannelID,'NumMinutes',1,'Fields',wFieldID,'ReadKey',readAPIKey); 
 
% Calculate the average humidity

avgHumidity = mean(humidity);
display(avgHumidity,'Average Humidity'); 
% Calculate the maximum and minimum temperatures 
[maxTempF,maxTempIndex] = max(tempF);
[minTempF,minTempIndex] = min(tempF);
display(maxTempF,'Maximum Temperature over the observation span is');
display(minTempF,'Minimum Temperature over the observation span is'); 
%fprintf(['Note: To write data to another channel, assign the write channel ID \n',... 
%    'and API Key to ''writeChannelID'' and  ''writeAPIKey'' variables. Also \n',... 
%   'uncomment the line of code containing ''thingSpeakWrite'' \n',... 
%   '(remove ''%%'' sign at the beginning of the line.)']);      

% To store the calculated average humidity, max, min  temperatures write it to a SIS updates channel  
writeChannelID = 1371616;  
 % Enter the Write API Key between the '' below: 
writeAPIKey = 'ACZ3CLZE3NTCDN40';  
 
% Set the email subject. 
 
% Read the recent data.

% Write to the three fields in the SIS updates channel 
thingSpeakWrite(writeChannelID,'Fields',[1,2,3],'Values',{avgHumidity,maxTempF,minTempF},'WriteKey',writeAPIKey);% Catch errors so the MATLAB code does not disable a TimeControl if it fails



