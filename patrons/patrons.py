#### This program collects all patron data up until 7/25/17. Only run if previous data is lost ####

# import required library for accessing Sierra with authorization
import requests
import secrets
import patronsv2

# loop through each URI starting at 7,000th index, incrementing by 2,000 until 99,000 is reached
for i in range(7000,99000,2000):
    
    # print(i) for testing purposes
    
    # set request variable equal to URI at i's index, showing fields: createdDate, names, barcodes, expirationDate and deleted is false
    request = requests.get("https://catalog.chapelhillpubliclibrary.org/iii/sierra-api/v3/patrons?offset=" + str(i) + "&limit=2000&fields=createdDate,names,barcodes,expirationDate&deleted=false", headers={
        "Authorization": "Bearer " + patronsv2.get_token()
    })

    # slice off the beginning and ends of json to allow for combining all data
    sliced_json = request.text[38:-2]

    # append data to patron json file and add a newline each iteration for better organization
    patrons = open('patrons.json', 'a')
    patrons.write(sliced_json + ",\n")

# delete ',' before this ']}' in json file
patrons.write(']}')