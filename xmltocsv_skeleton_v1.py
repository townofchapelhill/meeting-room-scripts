## Run on Python 3.x ##

######################
# Import needed modules
import xml.etree.ElementTree as ET
import urllib.request
import csv
import datetime
import os

## This .py program contains code that enables a user to parse XML info from either a URL 
## or a saved file. The parsed info is then converted to a CSV file which is locally 
## saved to the computer. The program lastly created a .txt file to keep a log each time 
## the program is run. The actions are controlled through user input.

######################
# Function that creates files to write parsed, converted, and logged info to a local file

def create_files():
    
    # Get current date info to use in logging
    current_datetime = datetime.datetime.now()
    
    loop = False
    while loop == False:
        
        # User input to decide the filename, this will be based on data info
        # E.g. filename may be 'Nextbus' or 'FireIncidents' if the info regards buses/fire incidents/etc
        filename = str(input("Desired name for output file ('YOURINPUT'.xml): ")).title()
    
        # Create vars to hold the strings that will be the full filename
        # raw_file will hold the base xml data
        # final_file will hold error corrected raw_file data converted to CSV
        raw_file = 'Raw' + filename.title().replace(" ","") + 'Data.xml'
        final_file = 'Converted' + filename.title().replace(" ","") + 'Data.xml'
        csv_file = filename.title().replace(" ","") + 'Data.csv'
        log = filename.title().replace(" ", "") + "Log.txt"

    
        # Open files in write mode to begin use
        xml_data = open(raw_file, "wt")
        converted_data = open(final_file, "wt") 
        log_file = open(log, 'wt')
        log_file.write("Program run on " + str(current_datetime) + '.\n')
        log_file.write('The files ' +raw_file + ', ' +final_file +", and "+filename + 'Log.txt' + " were created.\n")
    
        # Ask user to get data from a saved file or from a url
        file_or_url = input("Parse saved file ('f') or url data ('u'). Type 'b' to go back: ")
        
        # If the user chooses to use a saved file
        if file_or_url == 'f' or file_or_url == 'F':
            # Try to find a file with the name entered
            try:
                saved_filename = input("Enter the file name ('xyx.xml'): ")
            # Handle exception if the file is not found 
            except:
                print("There is no file saved with that name.")
                log_file.write("Error: User attempted to open a file that did not exist.\n")
                
            # Call parse_file using the entered filename
            parse_file(xml_data, saved_filename)
            log_file.write('Saved file successfully parsed to local XML file at ' + raw_file +' .\n')
            # Remove xml errors
            remove_errors(raw_file, final_file)
            # Convert xml to csv
            convert_to_csv(final_file,csv_file)
            log_file.write("XML successfully converted to CSV at " + csv_file + '.\n')
            loop = True
            
        # If the user chooses to parse a URL
        elif file_or_url == 'u' or file_or_url == 'U':
            # Ask user input for the URL address
            url_address = input("Enter the URL: ")
            # Call parse_url with the URL entered
            parse_url(xml_data, url_address)
            log_file.write('URL XML info successfully parsed to local XML file at ' +raw_file +'.\n')
            # Remove xml errors
            remove_errors(raw_file,final_file)
            # Convert xml to csv
            convert_to_csv(final_file, csv_file)
            log_file.write("XML successfully converted to CSV at " + csv_file + '.\n')
            loop = True
            
        # If the user chooses to go back -- e.g. they spelled the output file name wrong
        elif file_or_url == 'b':
            # Remove the file that was created with the wrong spelling
            os.remove(raw_file)
            os.remove(final_file)
            log_file.write('Filename labeled incorrect by user. Removed files from the OS.\n')
            # Loop back if the user chooses 'b' so they can start over
            loop = False
            
        # If the user does not enter any of the correct commands loop back to start
        else:
            print("Error. Enter 'f' for saved file or 'u' for url data. Try again.")
            loop = False
            
    # Final success log
    log_file.write('All files successfully created.\n')


######################
# Function to parse xml from saved file and write to file

def parse_file(write_file, filename):
    
    # Get current date info to use in logging
    current_datetime = datetime.datetime.now()
    
    # Create standard doc type var 
    doc_type = '<?xml version="1.0" encoding="utf-8" ?>\n'
    
    # Go ahead and write the doc type to the top of the file
    write_file.write(doc_type)

    # Open file passed into funtion and read lines
    open_file = open(filename, 'r')
    lines = open_file.readlines()
    for line in lines:
        write_file.write(line)
        
    print('The provided xml file has been copied to the raw file :)')
    # LATER Add option to compile multiple files into one
    write_file.close()
    

######################
# Function to parse XML info from url and write to file

def parse_url(write_file, filename):

    # Create main validation loop
    main_loop = True
    
    # While loop is true
    while main_loop == True:
        
        # Allow user to add another URL
        howmanyurls = input("Parse just this URL or add another? ('X' for just this URL 'Y' to add more): ")
        
        # If user chooses x
        if howmanyurls == 'X' or howmanyurls == 'x':
            # End main loop
            main_loop = False
        
            # Create a blank list to hold the initial data 
            blank_list = []
            
            # Try to decode the url based on different UTFs
            try: 
                decoded_url = urllib.request.urlopen(filename).read().decode('utf-8')
            except UnicodeDecodeError: 
                decoded_url = urllib.request.urlopen(filename).read().decode('utf-16')
            except: 
                decoded_url = urllib.request.urlopen(filename).read().decode('utf-32')
    
            # Iterate through the decoded url 'file', split \n characters, add \n characters to beginnings and ends of <>
            for line in decoded_url:
                line.split('\n')
                if line == ">":
                    line = (line+'\n')
                # elif line == '<': -s
                #     line = ('\n'+line)
                # Append each line to the blank list 
                blank_list.append(line)
    
            # Create a new list to hold the previous list 
            whole_list = blank_list # [0:-1] -s
            
            # Set the char to search for 
            utf = '>\n'
            # Prime the loop
            x = 1
            loop = False
            # Iterate through the list to find the utf char
            while loop == False and x < len(whole_list):
                location = whole_list[x]
                # If the utf char is found, created a stripped list that removes everything up until that point (This will be the utf line)
                # This removal allows for stacking of mutliple URLs
                # The doctype will be added to the written file 
                if location == utf:
                    end = x+1
                    stripped_list = whole_list[end:] # changed from -1 to none -s
                    # End the loop once the char is found 
                    loop = True
                # If the char is not found, continue iterating until it is found
                x = x+1
            # Write the stripped list to the file
            write_file.write("".join(stripped_list))   
            # Print for user 
            print("The URL has been decoded and written as a URL file.")
            # Close the written file 
            write_file.close()
        
        # If user chooses Y  -s
        elif howmanyurls ==  'Y' or howmanyurls == 'y':
            main_loop = False
            loop = True
            while loop == True:
                urls = input("Add next URL (Hit enter to stop): ")
                
                if urls == "":
                    loop = False
         
        # If user does not enter X or Y           
        else: 
            print("You must enter 'X' for one URL or 'Y' to add more. Try again.")
            main_loop = True


######################
# Function to clean up errors in the XML to remove before converting to CSV -s

def remove_errors(raw_file, final_file):
    raw = open(raw_file, 'r')
    converted = open(final_file, 'w')
    
    lines_of_file = raw.readlines()
    
    # change the xml data to take away invalid tokens (& to and) 
    # and save to a different file
    for line in lines_of_file:
        if '&' or '@' in line:
            line = line.replace("&", "and")
            line = line.replace("@", "at")
        converted.writelines(line)
    
    raw.close()
    converted.close()


######################
# Function that converts to CSV
# Pass in the file that was created
# Open that file and read to write to CSV file

def convert_to_csv(file, csv_file):
    # Allow user to enter tag names -s
    # Parse the XML file createdin pass_file and combine_routes
    tree = ET.parse(file)
    root = tree.getroot()

    # Create a CSV file in the open data unpublished folder for writing
    data = open(csv_file, 'w')
    # log_file.write('CSV file created.\n')

    # Create the csv writer object
    csvwriter = csv.writer(data)
    
    # Create empty list
    item_head = []

    # use boolean to determine header in loop
    header = True
    
    # check if the xml file contains attributes with important info
    if not list(root[0].attrib):
        has_attr = False
    else:
        has_attr = True
    
    # if there are no attributes, use tag names as headers and column names
    if not has_attr:
        # Create loop to convert file to csv -s
        for children in root.findall(root[0].tag):
            row = []
            # create header for csv file
            if header:
                # loops through each grandchild and assigns the tags as the header
                for grandchild in root[0]:
                    item_head.append(grandchild.tag)
                
                csvwriter.writerow(item_head)
                header = False
                    # creates a counter to count the amount of reservations today
                counter = 0
                # try:
                #     log_file.write("CSV header created, adding XML data to CSV file now...\n")
                # except:
                #     print('ERROR - missing "logs" directory')        
                
            # goes through each grandchild based on the child and appends rows to csv
            for grandchild in root[counter]:
                row.append(grandchild.text)
                
            csvwriter.writerow(row)
	   
            # increment counter
            counter += 1
        data.close()
            
    # if there are attributes, use the attributes within the tags for info
    # else:

    #         # save a list of id's to know if they are already added in
    #         id_list = []
    #         # loop through each <tr> in the routes
    #         for tr in route.findall('tr'):
    #             if tr.attrib['blockID'] not in id_list:
    #                 # loop through each stop and add the header info to list
    #                 for stop in tr.findall('stop'):
    #                     bus_info = []
    #                     bus = route.attrib['tag']
    #                     bus_info.append(bus)
    #                     title = route.attrib['title']
    #                     bus_info.append(title)
    #                     schedule = route.attrib['scheduleClass']
    #                     bus_info.append(schedule)
    #                     days = route.attrib['serviceClass']
    #                     bus_info.append(days)
    #                     direction = route.attrib['direction']
    #                     bus_info.append(direction)
    #                     blockID = tr.attrib['blockID']
    #                     bus_info.append(blockID)
    #                     id_list.append(blockID)
    #                     stop_n = stop.attrib['tag']
    #                     bus_info.append(stop_n)
                        
    #                     # loop allows for stop times to be in the correct order and row
    #                     for second_tr in route.findall('tr'):
    #                         if second_tr.attrib['blockID'] == tr.attrib['blockID']:
    #                             for second_stop in second_tr.findall('stop'):
    #                                 if second_stop.attrib['tag'] == stop.attrib['tag']:
    #                                     bus_info.append(second_stop.text)
                        
    #                     # add '--' for every blank space in csv
    #                     for i in range(30):
    #                         bus_info.append('--')
                            
    #                     # append the bus_info list onto the next row in csv file
    #                     csvwriter.writerow(bus_info)
                
    # # Close file once written to
    # data.close()


######################
# Main function

def main():
    # Call create_files
    create_files()

######################
# Call main to run program

main()
