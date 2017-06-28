import xml.etree.ElementTree as ET
import urllib.request
import csv
import datetime

# set the date with and without time to variables
now = datetime.datetime.now()
today = datetime.date.today()

# set xml files to variables
usage_file = '//CHFS/Shared Documents/OpenData/datasets/unpublished/cumulreservationData.xml'
fixed_file = '//CHFS/Shared Documents/OpenData/datasets/unpublished/convertedcumulReservationData.xml'

# throw an error if a "/logs" directory doesn't exist
try:
    log_file = open('logs/' + str(today) + '-cumulativeMeetingsLog.txt', 'w')
except:
    error_file = open('error.txt', 'w')
    error_file.write('ERROR - "logs" directory not found\n')
    error_file.close()
	
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
		log_file.write("Today's URL successfully accessed and decoded")
	except:
		log_file.write("ERROR - URL access or decoding error\n")
		
	reservations.write(stripped_url_list + '\n')
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
	    if '&amp;' in line:
	        line = line.replace("&amp;", "and")
	    my_file2.writelines(line)
	
	log_file.write('Converted XML file created.\n')
	my_file.close()
	my_file2.close()
	
	# parse the xml file
	try:
		tree = ET.parse(fixed_file)
		root = tree.getroot()
	except:
		log_file.write('ERROR - XML parsing error')
		print('error - XML parsing error')
		log_file.close()
	
	# create a csv file for writing
	reservation_data = open('//CHFS/Shared Documents/OpenData/datasets/unpublished/cumulreservationsToday.csv', 'w')
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
		
	log_file.write("Amount of reservations today calculated.\n\n")
	
	reservation_data.close()
	
	log_file.write("Today's reservation data and usage data has been written to a CSV file.\n\n")
	
	# print out usage data
	print('Reservations today:', counter)
	
try:
	main()
	log_file.write(str(now))
	log_file.close()
except:
    log_file.write('\nERROR - source folder for xml and csv files not found.\n')
    print('error - no src')
    log_file.close()