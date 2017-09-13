# Import required libraries 
import requests
import json
import datetime
import os
# Import API secrets file
import secrets 

# Access specific flurry query, pass header authentication, store data in var
def get_flurry():
    
    # Create var to put data in flurry directory
    unpublished_file = '//CHFS/Shared Documents/OpenData/datasets/flurrydata/flurry.csv'

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
    
    # Open the file to write/append to 
    flurrycsv = open(unpublished_file, "a")
    
    # Write CSV headings if the file is empty
    if os.stat("flurry.csv").st_size == 0:
        flurrycsv.write("Company Name, Average Time Per Session, Active Devices, Language, Time Spent, Sessions, Date and Time, Average Time Per Device, App Name, New Devices"+"\n")
    
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
    
    # Transfer file contents to a new file in the unpub directory
    flurrydirect = "//CHFS/Shared Documents/OpenData/datasets/flurrydata/flurry.csv"
    unpubdirect = open(flurrydirect)
    with open(flurrycsv) as f:
        with open(unpubdirect, "w") as f1:
            for line in f:
                f1.write(line) 
                
    # Close files
    unpubdirect.close()
    flurrycsv.close()
    
# Main function
def main():
    get_flurry()
    

# Call mai
