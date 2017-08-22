
# Import required library for accessing Sierra with authorization
import requests
import datetime
import secrets
import json

# Open file to write to and file to append to in future
patrons = open('patrons.json', 'w')
patrons_append = open('updatedpatrons.json', 'a')
patrons.write('{ "entries": [')

# Create date range to use in api call for active users
now = str(datetime.date.today())
present_date_string = now + str("T00:00:00Z")
one_year_ago = str(datetime.date.today() - datetime.timedelta(days=365))
old_date_string = one_year_ago + str("T00:00:00Z")
date_range = "[" + str(old_date_string) + "," + str(present_date_string) + "]"

# copy Steven
url = "https://catalog.chapelhillpubliclibrary.org/iii/sierra-api/v3/token"
header = {"Authorization": "Basic " + str(secrets.active_patrons_static_key), "Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(url, headers=header)
json_response = json.loads(response.text)
active_patrons_token = json_response["access_token"]

# Save header in var, change api key as needed (for now)
header_text = {"Authorization": "Bearer " + active_patrons_token}

# Set looping vars
i = 0
loop=True

# Loop goes through records up to i
while loop == True:
    
    # Request the api data at url
    request = requests.get("https://catalog.chapelhillpubliclibrary.org/iii/sierra-api/v4/patrons/?limit=2000&offset=" + str(i) + "&fields=updatedDate&updatedDate=" + str(date_range), headers=header_text)
    
    # Testing
    print(i)
    
    # Stop looping when the requests sends an error code/doesn't connect
    if request.status_code != 200:
        break
    
    # Counter to find slice start point 
    # copy Steven for this bit of code
    counter = 1
    for letter in request.text:
        if letter == '[':
            break
        counter += 1

    # Slice off the beginning and ends of json to allow for combining all data
    sliced_json = request.text[counter:-2]

    # Write data to patron json file 
    patrons.write(sliced_json + ",\n")
    
    # Increment i 
    i = i + 2000
    
# Write to end of file 
patrons.write(']}')
