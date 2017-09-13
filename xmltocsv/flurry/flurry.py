# Import required libraries 
import requests
import json
import datetime
import os
import traceback
# Import API secrets file
import secrets 

print("imported all libraries")

# Access specific flurry query, pass header authentication, store data in var
def get_flurry():
    
    # Find date and create vars to hold the span of one day 
    now = str(datetime.date.today())
    one_day_ago = str(datetime.date.today() - datetime.timedelta(days=1))
    date_string = one_day_ago + "/" + now
    
    # Flurry API call, date string is updated to cover daily stats
    url = "https://api-metrics.flurry.com/public/v1/data/appUsage/day/company/app/language?metrics=sessions,activeDevices,newDevices,timeSpent,averageTimePerDevice,averageTimePerSession&dateTime=" + date_string
    # Take API token from separate file
    headers = {"Authorization":"Bearer " + str(secrets.flurry_api_token)}
    data = requests.get(url,headers=headers).json()
    data_list = data["rows"]
    
    print("data fetched")
    
    # Open the file to write/append to 
    flurrycsv = open('//CHFS/Shared Documents/OpenData/datasets/flurrydata/flurry.csv', "a")
    print("flurry opened")
    
    # Write CSV headings if the file is empty
    if os.stat("//CHFS/Shared Documents/OpenData/datasets/flurrydata/flurry.csv").st_size == 0:
        flurrycsv.write("Company Name, Average Time Per Session, Active Devices, Language, Time Spent, Sessions, Date and Time, Average Time Per Device, App Name, New Devices"+"\n")
    print("added headings")
    
    # Set counter
    i = 0

    # Write/append the data to the file once the headings have been added
    # Write in CSV format for ease of use (since I'm not very familiar with json format)
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
    flurrycsv.close()
    
    # Copy file to unpub direct
    f = open('//CHFS/Shared Documents/OpenData/datasets/flurrydata/flurry.csv')
    f1 = open("//CHFS/Shared Documents/OpenData/datasets/unpublished/flurry.csv", "w")
    for line in f:
        f1.write(line)
        
   
# Main function
def main():
    
    errors = open("log_flurryerror.txt", "w")
    try:
        get_flurry()
    except Exception as exc:
        now = str(datetime.date.today())
        errors.write(traceback.format_exc())
        errors.write(now)

# Call main
main()
