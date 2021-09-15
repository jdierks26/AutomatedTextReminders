import pandas as pd
from datetime import datetime, timedelta
import os
import io
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from dotenv import load_dotenv
import random

# In this project, I will be using Twilio, datetime, pandas, and other modules to program an application that
# will send me a text message at the beginning of my day. The message will display the date, my classes for the day,
# and any upcoming assignments for the next week, separated by class. The output will look like this:

# Thursday, August 26, 2021
# ------------------------------------
# GEOG 100 | 11:00am | LIN 412
# IST 325 | 1:00pm | CAPF 3015
# ------------------------------------
# IST 410
#  -> Assessment - Fri Aug 27
# ------------------------------------

# To get started, we will need a .env file for any sensitive information. In this case, I will need to hide my
# authentication token for my Twilio API, which is a messaging service that I'll be using to send myself these
# messages

load_dotenv()

# Establishing the Client
proxy_client = TwilioHttpClient(proxy={'http': os.getenv("http_proxy"), 'https': os.getenv("https_proxy")})

twilio_client = Client(http_client=proxy_client)

# Loading in our .csv file that contains all my Due Dates, their Assignment, and their Class
df = pd.read_csv(filepath_or_buffer='/home/jdierks26/Due_Date_Reminders/Dates.csv')

# Using the Datetime module to import the current date, and find next week's date using a timedelta so we can find
# our upcoming due dates
now = datetime.now()

time_now = now

time_week = (now + timedelta(days=7))

# Converting our Due Dates to datetime objects so that the program knows how to properly compare the Due Date with the
# current date
for i in df.index:
    df.loc[i,'datetime'] = datetime.strptime(df.loc[i, 'Due Date'], '%m/%d/%Y')

# Creating a list to store all the indexes of the upcoming assignments, so that we can access them later
upcoming_indexes = list()

# Since I would like to organize my due dates by class, I need a way to reference each class. A set will work perfectly,
# as it removes duplicate values
class_list = set()

# Evaluating our converted Due Date and appending the index to our list if it is within a week from the current date
for i in df.index:
    if time_now <= df.loc[i, 'datetime'] <= time_week:
        upcoming_indexes.append(i)

# Adding all the unique classes from our upcoming due dates list to a class_list. This way, if a class doesn't have
# any upcoming assignments, it won't be in the set
for i in upcoming_indexes:
    class_list.add(df.loc[i, 'Class'])

# I'll be using StringIO to capture all the print statements for our final text output. Since the 'body' variable, which
# is used to store our actual message, cannot take print statements, I will store the output of certain print statements
# and store it into a variable 'f'
f = io.StringIO()

# Printing out the current date for the beginning of our message
print(time_now.strftime('%A, %B %e, %Y'), file=f)
print("------------------------------------", file=f)

# Since I have two sets of classes depending on the weekday, I can use .weekday and an IF statement to find what day of
# the week the current date is, and print out the corresponding classes
# .weekday will return an integer 0-6 depending on the weekday, monday being 0
if now.weekday() == 0 or now.weekday() == 2 or now.weekday() == 4:
    print("IST 330 | 9:30am | CAPF 3031" + "\n" + "IST 320 | 1:00pm | CAPF 1120", file=f)
else:
    print("GEOG 100 | 11:00am | LIN 412" + "\n" + "IST 325 | 1:00pm | CAPF 3015", file=f)

print("------------------------------------", file=f)

# Converting our datetime to a format that I prefer to read
for i in df.index:
    df.loc[i,'formatdate'] = df.loc[i, 'datetime'].strftime('%a %b %e')

# This nested FOR loop will, for each unique class in our class_list, print out that class, and for every upcoming due
# date that is in that class, print out the assignment and its due date
for classes in class_list:
    print(classes, file=f)
    for i in upcoming_indexes:
        if df.loc[i, 'Class'] == classes:
            print(" -> " + str(df.loc[i, 'Assignment']) + " - " + str(df.loc[i, 'formatdate']), file=f)
    print("------------------------------------", file=f)

# Here I am creating another dataframe from our Quotes csv file
df2 = pd.read_csv('/home/jdierks26/Due_Date_Reminders/Quotes.csv')

# Generating a random index from our Quotes.csv index
r_int = random.choice(df2.index)

# Printing a random quote based off the random index number we generated
print(df2.loc[r_int,'Quote'], file=f)

# Storing our print statement outputs into a variable called 'output'
output = f.getvalue()
f.close()

# Our function for sending messages. For our body we will just call our 'output' variable. Sensitive information has been xxx'd out. 
def send_message():
    twilio_from = xxx
    to_phone_number = xxx
    twilio_client.messages.create(
        body=output,
        from_=f"{twilio_from}",
        to=f"{to_phone_number}")

send_message()

# I want this program to run everyday at a set time. I have a few options:
# 1. Use Windows to turn this into a background script on my personal computer
# 2. Host my own server
# 3. Use an online hosting service

# Since I don't want to have my computer running 24/7, and I don't want to invest any money into hosting a server, I
# will use Pythonanywhere.com to host my application for free. In order to do so, though, I will have to use a Bash
# console to create the proper virtual environment to run my program with all it's dependencies. Once that is finished
# I can create an automated task that will run our virtual environment and then execute this file daily at 8am.

# thanks for checking out my project!
