# AutomatedReminders
In this project, I will create a Python program that will send a text message reminder daily that displays the date, my classes for the day, a random inspirational quote, and any due dates within the next week, sorted by class. I will also use PythonAnywhere.com, a hosting service, to run my script daily.

I will be using the pandas, datetime, twilio, and io modules, amongst others, and utilizing skills such as nested FOR loops, dataframe manipulation, index matching, etc.

Files in the repository:
 - ResumeFetcher.py is the main Python file 
 - Dates.csv contains all of my Assignments with their Due Dates and Class
 - Quotes.csv contains some random quotes that I've copied from various websites 
 - .env contains sensitive information (which is converted to xxx for this repository) 
 - PythonAnywhere.png is a screenshot showing my automated task that launches my ResumeFetcher.py daily
 - TextOutput is an example of an SMS message I've recieved from this program

I created this project because I wanted an automated reminder system that I didn't have to consistently update, log into, flip through, etc. A system that I could set up once, 
let it run, and not have to worry about it for the rest of the semester. This is why I chose a pandas csv file data format, instead of using JSON files that I 
could delete, edit and insert on the fly. I also wanted to make locating my new classes a bit easier, as now I can just look at a text instead of having to navigate
through a web brower and my KU portal to find my class's location and time. Lastly, I wanted an inspirational quote to start my day on the right note.

