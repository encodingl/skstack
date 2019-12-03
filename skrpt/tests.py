from django.test import TestCase

# Create your tests here.
import time
import datetime


# weekoffset = datetime.datetime.now().weekday()
# weekoffset = datetime.datetime.now().weekday() + 7
# weekoffset = datetime.datetime.now().weekday() + 14
# weekoffset = datetime.datetime.now().weekday() + 21


# threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = weekoffset))
# print(threeDayAgo)
weekoffset = datetime.datetime.now().weekday()
datelist = []
for i in range(5):
    weekstartday = (datetime.datetime.now() - datetime.timedelta(days=6))
    datelist.append(weekstartday.strftime("%Y%m%d"))
    weekoffset = weekoffset + 7
datelist.reverse()
print(datelist)



# dict1 = {'pord':[1,2,3,4,5]}
# # print(dict1['pord'])
# print(datetime.date(2020,1,1).isocalendar())
# at = datetime.date(2020,1,1).isocalendar()
# print(at[0],at[1])
# if len(str(at[1]))<2:
#     weeknum  = '0' + str(at[1])
# datelist = str(at[0]) + weeknum
# print(datelist)
# print(time.strftime('%W'))
# datetime.datetime