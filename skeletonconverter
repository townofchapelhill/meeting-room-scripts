# Import needed modules
import xml.etree.ElementTree as ET
# Possible import lxml
import urllib.request
import csv
import datetime

# Function that creates files to write to
def create_files():

    # Store datetime information for file naming
    current_day = datetime.date.today()

    # User input to decide the filename, this will be based on data info
    # E.g. filename may be 'Nextbus' or 'FireIncidents' if the info regards buses/fire incidents/etc
    # Stick to capital starting letter and camel case
    filename = str(input("Desired Output Filename ('InThisFormat'): "))

    # Create vars to hold the strings that will be the full filename
    # raw_file will hold the base xml data
    # final_file will hold error corrected raw_file data
    raw_file = str(current_day) + '_Raw' + filename + 'Data.xml'
    final_file = str(current_day) + '_Converted' + filename + 'Data.xml'

    # Open raw file in write mode to begin use
    xml_data = open(raw_file, "w")
    converted_data = open(final_file, "w")

    # Ask user to get data from a saved file or from a url
    file_or_url = input("Parse saved file (f) or url data (u): ")
    if file_or_url == 'f' or file_or_url == 'F':
        saved_filename = input("Enter the file name ('xyx.xml'): ")
        parse_file(xml_data, saved_filename, 'f')
    elif file_or_url == 'u' or file_or_url == 'U':
        url_address = input("Enter the URL: ")
        parse_file(xml_data, url_address, 'u')
    else:
        print("Error. Enter 'f' for saved file or 'u' for url data.")

# Function to parse xml and write to file
def parse_file(write_file, filename, x):

    current_datetime = datetime.datetime.now()

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

        write_file.write(ending)
        write_file.write(body)

    elif x == 'u':
        list_to_xml = []
        decoded_url = urllib.request.urlopen(filename).read().decode('utf-8')
        for line in decoded_url:
            list_to_xml.append(line)
        print(list_to_xml)

        write_file.write(str(list_to_xml))

# Main function
def main():
    create_files()

# Call main
main()
