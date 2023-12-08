from WebRegAutomation import WebRegAutomation
import time
from configparser import ConfigParser
import os
from ClassAvailabilityMonitor import ClassAvailabilityMonitor

'''
info.txt file Formatting:
YEAR (EX: 2024)
CAMPUS (EX: NB)
CLASS INDEXES (00000,00001)
'''

lines = []

# Open the file
with open('info.txt', 'r') as file:
    for line in file:
        # Optionally, you can strip the newline character at the end of each line
        lines.append(line.strip())

year = lines[0]
campus = lines[1]

classes = [element.strip() for element in lines[2].split(',')]

monitor = ClassAvailabilityMonitor(year, campus)

wra = WebRegAutomation(False)

config = ConfigParser()
config.read('config.ini')
username = config.get('credentials', 'username')
password = config.get('credentials', 'password')

login_result = wra.login(username,password,"https://sims.rutgers.edu/webreg/chooseSemester.htm?login=cas")

if(login_result):
    wra.get_duo()
    wra.webreg_loading()

while(True):
    for i in range(len(classes)):
        WebRegAutomation.print_with_timestamp("Checking Availablility for index: " + classes[i])
        if(not monitor.check_class_availability(classes[i])):
            WebRegAutomation.print_with_timestamp("Class Not Available")
            wra.timeout_activity()
        else:
            WebRegAutomation.print_with_timestamp("Class Available")
            WebRegAutomation.print_with_timestamp("Trying To Register")

            if(login_result):
                registration_result = wra.class_registration('12024',classes[i])
                if(registration_result):
                    classes.remove(classes[i])
        WebRegAutomation.print_with_timestamp("Timeout")
        time.sleep(5)


    



