# Import needed modules
import xml.etree.ElementTree as ET
# Possible import lxml
import urllib.request
import csv
import datetime
import os

# Function that creates files to write to
def create_files():
    
    # Get current date info to use in logging
    current_datetime = datetime.datetime.now()
    
    loop = False
    while loop == False:
        # Store datetime information for file naming
        current_day = datetime.date.today()

        # User input to decide the filename, this will be based on data info
        # E.g. filename may be 'Nextbus' or 'FireIncidents' if the info regards buses/fire incidents/etc
        # Stick to capital starting letter and camel case
        filename = str(input("Desired name for output file: ")).title()
    
        # Create vars to hold the strings that will be the full filename
        # raw_file will hold the base xml data
        # final_file will hold error corrected raw_file data
        raw_file = 'Raw' + filename.title().replace(" ","") + 'Data.xml'
        final_file = 'Converted' + filename.title().replace(" ","") + 'Data.xml'
    
        # Open raw file in write mode to begin use
        xml_data = open(raw_file, "w")
        converted_data = open(final_file, "w")
        log_file = open("LOG: "+filename, 'w')
    
        # Ask user to get data from a saved file or from a url
        file_or_url = input("Parse saved file ('f') or url data ('u'). Type 'b' to go back: ")
        
        # If the user chooses to use a saved file
        if file_or_url == 'f' or file_or_url == 'F':
            # Try to find a file with the name entered
            # EXCEPTION HANDLING NOT FUNCTIONAL?
            try:
                saved_filename = input("Enter the file name ('xyx.xml'): ")
            # Handle exception if the file is not found 
            except:
                print("There is no file saved with that name.")
                log_file.write("Error: User attempted to open a file that did not exist.")
            # Call parse_file using the entered filename, pass parameters to connect files and saved file vs url info
            parse_file(xml_data, saved_filename, 'f')
            loop = True
        # If the user chooses to parse a URL
        elif file_or_url == 'u' or file_or_url == 'U':
            # Ask user input for the URL address
            url_address = input("Enter the URL: ")
            # Call parse_file with the URL entered
            parse_file(xml_data, url_address, 'u')
            loop = True
        # If the user chooses to go back -- e.g. they spelled the output file name wrong
        elif file_or_url == 'b':
            # Remove the file that was created with the wrong spelling
            os.remove(raw_file)
            os.remove(final_file)
            # Loop back if the user chooses 'b' so they can start over
            loop = False
        # If the user does not enter any of the correct commands loop back to start
        else:
            print("Error. Enter 'f' for saved file or 'u' for url data. Try again.")
            loop = False

# Function to parse xml and write to file
def parse_file(write_file, filename, x):
    
    # Get current date info to use in logging
    current_datetime = datetime.datetime.now()

    # If the user entered f to use a saved file 
    if x == 'f':
        # Parse the xml file
        tree = ET.parse(filename)
        root = tree.getroot()

        for child in root:
            header_tag = str(child.tag)

        # Create doc type and body tag vars
        doc_type = '<?xml version="1.0" encoding="utf-8" ?>\n'
        body_tag = '<body copyright = "All data copyright Chapel Hill Transit 2017.">\n'
        body = '</body>'
        # Create outermost heading tag
        heading_tag = '<'+header_tag+'>\n'
        ending = '\n</'+header_tag+'>\n'

        # Write initial doc_type, body_tag, and heading_tag
        write_file.write(doc_type)
        write_file.write(body_tag)
        write_file.write(heading_tag)

        # Iterate and write the child attributes
        for child in root:
            write_file.write(str(child.attrib))

        # Write the ending tags
        write_file.write(ending)
        write_file.write(body)

    # If user chooses to enter a URL
    elif x == 'u':
        
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
            elif line == '<':
                line = ('\n'+line)
            # Append each line to the blank list 
            blank_list.append(line)

        # Create a new list to hold the previous list 
        whole_list = blank_list[0:-1]
        
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
                stripped_list = whole_list[end:-1]
                # End the loop once the char is found 
                loop = True
            # If the char is not found, continue iterating until it is found
            x = x+1
        # Write the stripped list to the file
        write_file.write("".join(stripped_list))    
    # Close the written file 
    write_file.close()
    

# Main function
def main():
    # Call create_files
    create_files()

# Call main
main()