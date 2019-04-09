import xml.etree.ElementTree as ET
import urllib.request
import csv
import datetime

# set the date with and without time to variables
now = datetime.datetime.now()
today = datetime.date.today()

# set xml files to variables
usage_file = '//CHFS/Shared Documents/OpenData/datasets/staging/cumulreservationData.xml'
fixed_file = '//CHFS/Shared Documents/OpenData/datasets/staging/convertedcumulReservationData.xml'

# throw an error if a "/logs" directory doesn't exist
try:
    log_file = open('logs/' + str(today) + '-cumulativeMeetingsLog.txt', 'w')
except:
    error_file = open('error.txt', 'w')
    error_file.write('ERROR - "logs" directory not found\n')
    error_file.close()

# function checks if string is an ascii
def is_ascii(s):
	return all(ord(c) < 128 for c in s)
	
# function to create XML file from URL containing today's data
def create_xml():
	
	# ~ 
	reservations = open(usage_file, "r")
	converted = open(fixed_file, "w")
	
	lines = reservations.readlines()
	
	for line in lines:
	    pass
	
	last = line

	for line in lines:
	    if line == last:
	        converted.write(last[:-15])
	    else:
	        converted.write(line)
	
	reservations.close()
	converted.close()
	        
	# Create the variable to hold the desired write file
	# reservations = open(usage_file, "w")
	
	# ~
	reservations = open(fixed_file, "a")
	
	# Create variables to hold the phrases we want to add to the beginning and end of new XML file
	# doc_type = '<?xml version="1.0" encoding="utf-8" ?>\n'
	# body_tag = '<reservation>\n'
	body = '</reservation>\n'
	# Write the necessary statements to beginning of XML doc
	# reservations.write(doc_type)
	# reservations.write(body_tag)
	try:
		url = ('http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&do=0')
		decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
		stripped_url_list = decoded_url[52:-14]
		log_file.write("Today's URL successfully accessed and decoded.\n")
	except:
		log_file.write("ERROR - URL access or decoding error\n")
		
	reservations.write(stripped_url_list + '\n')
	log_file.write("Today's reservation data has been appended to a cumulative XML file for conversion to CSV.\n")
    # Write the end statements desired and close the file
	reservations.write(body)
	reservations.close()  

# main function that prints desired data and creates a csv file
# that organizes today's reservation data
def main():
	
	log_file.write("Creating XML file for today's meetings.\n")
	try:
		create_xml()
	except:
	    log_file.write("ERROR - there was an error in the creating the XML file for today's reservations.\n")
	
	# ~
	my_file = open(fixed_file, 'r')
	my_file2 = open(usage_file, 'w')
	
	# my_file = open(usage_file, 'r')
	# my_file2 = open(fixed_file, 'w')
	
	lines_of_file = my_file.readlines()
	
	log_file.write('Removing invalid tokens from XML file.\n')
	# change invalid tokens
	for line in lines_of_file:
		if is_ascii(line):
			if '&' in line:
				line = line.replace('&', 'and')
		else:
			for char in line:
				if is_ascii(char):
					continue
				else:
					line = line.replace(char, '?')
		my_file2.writelines(line)
	
	log_file.write('Converted XML file created.\n')
	my_file.close()
	my_file2.close()
	
	# parse the xml file
	# try:
	tree = ET.parse(usage_file)
	root = tree.getroot()
# except:
	# 	log_file.write('ERROR - XML parsing error')
	# 	print('error - XML parsing error')
	# 	log_file.close()
	
	# create a csv file for writing
	reservation_data = open('//CHFS/Shared Documents/OpenData/datasets/staging/cumulreservationsToday.csv', 'w')
	log_file.write("\nCSV file for today's meetings created.\n")
	
	# create the csv writer object
	csvwriter = csv.writer(reservation_data)
	item_head = []
	
	header = True
	
	# loops through today's reservations and adds to the csv file
	for member in root.findall('item'):
		reservation_row = []

		# creates the header
		if header:
			# loops through each grandchild and assigns the tags as the header
			for grandchild in root[0]:
				item_head.append(grandchild.tag)
			csvwriter.writerow(item_head)
			log_file.write("CSV header created, adding XML data to CSV file now...\n")
			header = False
			# creates a counter to count the amount of reservations today
			counter = 0
		
		# goes through each grandchild based on the child and appends rows to csv
		for grandchild in root[counter]:
			reservation_row.append(grandchild.text)
			
		csvwriter.writerow(reservation_row)
		
		# increment counter
		counter += 1
		
	reservation_data.close()
	
	log_file.write("Today's reservation data has been appended to the cumulative CSV file.\n\n")

main()
log_file.write(str(datetime.datetime.now()))
log_file.close()
