# Import libraries to request REST api
import requests
import json

# Access specific flurry query, pass header authentication, store data in var
def get_flurry():
    
    json_file = open("flurry.json", "w")
    
    # Static URL, needs to be made able to be modified on a weekly, monthly, x basis based on timestamps
    url = "https://api-metrics.flurry.com/public/v1/data/appUsage/week/company/app/language?metrics=sessions,activeDevices,newDevices,timeSpent,averageTimePerDevice,averageTimePerSession&dateTime=2017-07-03/2017-07-10"
    headers = {"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6ImZsdXJyeS56dXVsLnByb2Qua2V5c3RvcmUua2V5LjIifQ.eyJpc3MiOiJodHRwczovL3p1dWwuZmx1cnJ5LmNvbTo0NDMvdG9rZW4iLCJpYXQiOjE0OTg2NzI5MjAsImV4cCI6MzMwNTU1ODE3MjAsInN1YiI6IjM5Njk2MiIsImF1ZCI6IjQiLCJ0eXBlIjo0LCJqdGkiOiIxNjQwIn0.TEfZiAbxbODOqVbwdAHkrHlvvJaiEaZCEbH0hOkBKsY"}
    data = requests.get(url,headers=headers).json()
    data_list = data["rows"]
    
    # Testing purposes
    flurrycsv = open("flurry.csv", "w")
    i = 0
    flurrycsv.write("Company Name, Average Time Per Session, Active Devices, Language, Time Spent, Sessions, Date and Time, Average Time Per Device, App Name, New Devices"+"\n")
    while i < len(data_list):
        flurrycsv.write(data_list[i]['company|name'] + ", ")
        flurrycsv.write(str(data_list[i]['averageTimePerSession'])+ ", ")
        flurrycsv.write(str(data_list[i]['activeDevices'])+ ", ")
        flurrycsv.write(data_list[i]['language|name']+ ", ")
        flurrycsv.write(str(data_list[i]['timeSpent'])+ ", ")
        flurrycsv.write(str(data_list[i]['sessions'])+ ", ")
        flurrycsv.write(data_list[i]['dateTime']+ ", ")
        flurrycsv.write(str(data_list[i]['averageTimePerDevice'])+ ", ")
        flurrycsv.write(data_list[i]['app|name']+ ", ")
        flurrycsv.write(str(data_list[i]['newDevices']))
        flurrycsv.write("\n")
        i += 1    
   
# Update the file with new data on weekly, monthly, x basis
def update_file():
    pass

# Main function
def main():
    get_flurry()

# Call main   
main()
