# Import libraries to request REST api
import requests
import json

# Access specific flurry query, pass header authentication, store data in var
def get_flurry():
    # Static URL, needs to be made able to be modified on a weekly, monthly, x basis based on timestamps
    url = "https://api-metrics.flurry.com/public/v1/data/appUsage/week/company/app/language?metrics=sessions,activeDevices,newDevices,timeSpent,averageTimePerDevice,averageTimePerSession&dateTime=2017-07-03/2017-07-10"
    headers = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6ImZsdXJyeS56dXVsLnByb2Qua2V5c3RvcmUua2V5LjIifQ.eyJpc3MiOiJodHRwczovL3p1dWwuZmx1cnJ5LmNvbTo0NDMvdG9rZW4iLCJpYXQiOjE0OTg2NzI5MjAsImV4cCI6MzMwNTU1ODE3MjAsInN1YiI6IjM5Njk2MiIsImF1ZCI6IjQiLCJ0eXBlIjo0LCJqdGkiOiIxNjQwIn0.TEfZiAbxbODOqVbwdAHkrHlvvJaiEaZCEbH0hOkBKsY"}
    data = requests.get(url,headers=headers).json()
    data_list = data["rows"]
    cutoff_point = "averageTimePerDevice"
    
    # Testing purposes
    i = 0
    while i < len(data_list):
        print("Company Name: " + data_list[i]['company|name'])
        print("Average Time Per Session: " + str(data_list[i]['averageTimePerSession']))
        print("Active Devices: " + str(data_list[i]['activeDevices']))
        print("Language: " + data_list[i]['language|name'])
        print("Time Spent: " + str(data_list[i]['timeSpent']))
        print("Sessions: " + str(data_list[i]['sessions']))
        print("Date and Time: " + str(data_list[i]['dateTime']))
        print("Average Time Per Device: " + str(data_list[i]['averageTimePerDevice']))
        print("App Name: " + data_list[i]['app|name'])
        print("New Devices: " + str(data_list[i]['newDevices']))
        print()
        i += 1      

# Create file to store data
def create_file():
    pass

# Update the file with new data on weekly, monthly, x basis
def update_file():
    pass

# Main function
def main():
    get_flurry()

# Call main   
main()
