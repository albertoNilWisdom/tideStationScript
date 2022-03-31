import requests
import os
import json
import mysql.connector
import datetime

db = mysql.connector.connect(
        host='127.0.0.1',
        user='ted',
        passwd='',#
        db='JohnLeeWebHooker')
cursor = db.cursor(buffered=True)

stationURL = 'https://environment.data.gov.uk/flood-monitoring/id/stations/E8980'
stationData = requests.get(stationURL).json()

#print(stationData['items']['measures']['latestReading']['value'])
#print(stationData['items']['measures']['latestReading']['dateTime'])


latestReading = stationData['items']['measures']['latestReading']['value']
latestReadingDateTime = stationData['items']['measures']['latestReading']['dateTime']

##read  oldprices
with open('/root/webhooks/tideData/lastreading.txt', 'r') as F:
    oldReadingDateTime = F.read()

os.remove('/root/webhooks/tideData/lastreading.txt')

##write newPrices to lastprices.txt
with open('/root/webhooks/tideData/lastreading.txt', 'w') as F:
    # Use the json dumps method to write the list to disk
    F.write(latestReadingDateTime)

if oldReadingDateTime != latestReadingDateTime:
    ##PUSH TO MYSQL
	print('push to mysql')
	sql = "INSERT INTO tideData(mAOD,dateTime,callDateTime)VALUES("+str(latestReading)+",'"+str(latestReadingDateTime)+"',cast(now() as datetime))"
	print(sql)
	cursor.execute(sql)
	db.commit()
