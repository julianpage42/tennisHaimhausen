# Import Meteostat library and dependencies
import calendar
import datetime
import pandas as pd
import pytz
from meteostat import Hourly, Daily
from meteostat import Stations
from astral import LocationInfo

#input variables
posLat = 48.323
posLon = 11.557
# minimum considered sun is risen
startHour = 12
# maximum considered sun is still risen
stopHour = 21
# minimum temperature
tempLimit = 10
# maximum precipitation
prcpLimit = 0.0
# year to consider
year = 2022
months = [1, 2, 3, 11, 12]

# Get nearby weather stations
stations = Stations()
stations = stations.nearby(posLat, posLon)
station = stations.fetch(1)
#print(station)
location = LocationInfo('Haimhausen', 'Germany', 'Europe/Berlin', posLat, posLon)
#print (location)

totalHours = 0
days = 0
for m in months:
    monthSum = 0
    monthData = Daily(station, datetime.datetime(year, m, 1), datetime.datetime(year, m, calendar.monthrange(year, m)[1])).fetch()

    for dayOfMonth in range(1, calendar.monthrange(year, m)[1]+1):
        #print(dayOfMonth)
        # get sunrise / sunset
        from astral.sun import sun
        sun = sun(location.observer, date=datetime.datetime(year, m, dayOfMonth), tzinfo=location.timezone)

        start = datetime.datetime(year, m, dayOfMonth, hour=max(startHour, sun["sunrise"].hour+1))
        end = datetime.datetime(year, m, dayOfMonth, hour=min(stopHour, sun["sunset"].hour-1))
        #print(start)
        #print(end)

        # Get hourly data
        data = Hourly(station, start, end).fetch()
        #print(data)
        #print(len(data))

        filtered = data.query('temp > {0}'.format(tempLimit))["temp"]
        # Print DataFrame
        #print(filtered)
        #print(len(filtered))

        prcp = (monthData[monthData.axes[0] == datetime.datetime(year, m, dayOfMonth)]["prcp"])
        if prcp.size == 0:
            print("No precipitation data found on {0}-{1}-{2}".format(year, m, dayOfMonth))
        else:
            if prcp.iloc[0] <= prcpLimit:
                monthSum = monthSum + len(filtered)
                if len(filtered) > 0:
                    days = days + 1
            #else:
                #print("Too rainy on {0}-{1}-{2}".format(year, m, dayOfMonth))
    print('Sum for month {0}: {1} Hours'.format(m, monthSum))
    totalHours = totalHours + monthSum
print("-------------------------")
print('Total Sum: {0} Hours'.format(totalHours))
print('Total Sum: {0} Days'.format(days))
