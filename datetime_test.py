import datetime
import time

# Create datetime objects for each time (a and b)
dateTimeA = datetime.datetime.now()
time.sleep(1)
dateTimeB = datetime.datetime.now()
# Get the difference between datetimes (as timedelta)
dateTimeDifference = dateTimeB - dateTimeA
# Divide difference in seconds by number of seconds in hour (3600)  
dateTimeDifferenceInHours = dateTimeDifference.total_seconds()
print(dateTimeDifference.total_seconds()*1000)
print(dateTimeDifferenceInHours)
