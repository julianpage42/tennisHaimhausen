# Import Meteostat library and dependencies
import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily, Hourly

posLat = 48.323
posLon = 11.557
year = 2023

# Set time period
start = datetime.datetime(year, 1, 1)
end = datetime.datetime(year, 12, 31)

# Create Point for Vancouver, BC
location = Point(posLat, posLon, 70)

data = Daily(location, start, end)
data = data.fetch()

# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'tmin', 'tmax','prcp'])
plt.show()