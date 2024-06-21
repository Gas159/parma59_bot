# import time
# time_now= time.tzname
# print(time_now)
#
# import datetime
# tz_string = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
# print(tz_string)
#
# from time import gmtime, strftime
# print(strftime("%z", gmtime()))
#
# timezone = "Europe/Moscow"
# print(timezone)

from datetime import datetime, timedelta
from pytz import timezone


msk_tz_perm = timezone('Europe/Samara')
current_time = datetime.now(msk_tz_perm)
print(current_time)


msk_tz = timezone('Europe/Moscow')
# Get the current time in the desired timezone
current_time = datetime.now(msk_tz)
print(current_time)

# Define the timedelta for the offset of 2 hours
time_offset = timedelta(hours=2)

# Apply the timedelta to the current time in the given timezone
current_time_shifted = current_time + time_offset

print(current_time_shifted.strftime("%Y-%m-%d %H:%M:%S"))