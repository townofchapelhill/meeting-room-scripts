import xml.etree.ElementTree as ET
import urllib.request
import csv
import datetime

# set the date with and without time to variables
now = datetime.datetime.now()
today = datetime.date.today()

# set xml files to variables
usage_file = str(today) + '-reservationData.xml'
fixed_file = str(today) + '-convertedReservationData.xml'

# function counts the amount of reservations this week (Sunday to today)
def reservations_by_week():
	
	# create a file that holds all xml data this week
	weekly_monthly_data = open(usage_file, 'w')
	doc_type = '<?xml version="1.0" encoding="utf-8" ?>\n'
	body_tag = '<reservation>\n'
	body = '</reservation>\n'
	weekly_monthly_data.write(doc_type)
	weekly_monthly_data.write(body_tag)
	
	# set sunday to correct offset based on the current day of the week
	if now.weekday() == 0:
		sunday = -1
	elif now.weekday() == 1:
		sunday = -2
	elif now.weekday() == 2:
		sunday = -3
	elif now.weekday() == 3:
		sunday = -4
	elif now.weekday() == 4:
		sunday = -5
	elif now.weekday() == 5:
		sunday = -6
	elif now.weekday() == 6:
		sunday = 0

	# loop through the reservation XML URLs for each day this week so far
	for day in range(sunday, 1):
		
		# the url uses do= to take in a date offset value
	    url = ('http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&do='+ str(day))
	    # Read and decode the XML file found at each url
	    decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
	    stripped_url_list = decoded_url[52:-14]
	    weekly_monthly_data.write(stripped_url_list)
	    
	weekly_monthly_data.write(body)
	weekly_monthly_data.close()
	
	my_file = open(usage_file, 'r')
	my_file2 = open(fixed_file, 'w')
	
	lines_of_file = my_file.readlines()
	
	# change the week's xml data to take away invalid tokens (& to and) 
	# and save to a different file
	for line in lines_of_file:
	    if '&amp;' in line:
	        line = line.replace("&amp;", "and")
	    my_file2.writelines(line)
	
	my_file.close()
	my_file2.close()
	
	# parse the xml file
	tree = ET.parse(fixed_file)
	root = tree.getroot()
	
	count = 0
	
	# count each <item> tag in the xml file to get reservations this week
	for member in root.findall('item'):
		count += 1
		
	return count
	
# function counts the amount of reservations this week (1st to today)
def reservations_by_month():
	
	# create a file that holds all xml data this week
	weekly_monthly_data = open(usage_file, 'w')
	doc_type = '<?xml version="1.0" encoding="utf-8" ?>\n'
	body_tag = '<reservation>\n'
	body = '</reservation>\n'
	weekly_monthly_data.write(doc_type)
	weekly_monthly_data.write(body_tag)

	# loop through XML URLs from the first of the month to today
	for day in range(1, now.day + 1):
		
		# the url uses ds= to take in a date in the format YYYY/MM/DD
	    url = ('http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&ds='+ str(now.year) \
	    + '/' + str(now.month) + '/' + str(day))
	    # Read and decode the XML file found at each url
	    decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
	    stripped_url_list = decoded_url[52:-14]
	    weekly_monthly_data.write(stripped_url_list)
	    
	weekly_monthly_data.write(body)
	weekly_monthly_data.close()
	
	my_file = open(usage_file, 'r')
	my_file2 = open(fixed_file, 'w')
	
	lines_of_file = my_file.readlines()
	
	# change invalid tokens and placed converted into a new file
	for line in lines_of_file:
	    if '&amp;' in line:
	        line = line.replace("&amp;", "and")
	    my_file2.writelines(line)
	
	my_file.close()
	my_file2.close()
	
	# parse the xml file
	
	tree = ET.parse(fixed_file)
	root = tree.getroot()
	
	count = 0
	
	# count each <item> tag to get monthly usage data
	for member in root.findall('item'):
		count += 1
		
	return count

# function counts reservations since a certain amount of days
def reservations_since(days_ago):
	
	weekly_monthly_data = open(usage_file, 'w')
	doc_type = '<?xml version="1.0" encoding="utf-8" ?>\n'
	body_tag = '<reservation>\n'
	body = '</reservation>\n'
	weekly_monthly_data.write(doc_type)
	weekly_monthly_data.write(body_tag)

	for i in range(days_ago,1):
		
	    url = ('http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&do='+ str(i))
	    # Read and decode the XML file found at each url
	    decoded_url= urllib.request.urlopen(url).read().decode('utf-8')
	    # Add each line of the XML file to the empty list
	
	    stripped_url_list = decoded_url[52:-14]
	    weekly_monthly_data.write(stripped_url_list)
	    
	weekly_monthly_data.write(body)
	weekly_monthly_data.close()
	
	my_file = open(usage_file, 'r')
	my_file2 = open(fixed_file, 'w')
	
	lines_of_file = my_file.readlines()
	
	for line in lines_of_file:
	    if '&amp;' in line:
	        line = line.replace("&amp;", "and")
	    my_file2.writelines(line)
	
	my_file.close()
	my_file2.close()
	
	# parse the xml file
	
	tree = ET.parse(fixed_file)
	root = tree.getroot()
	
	count = 0
	
	for member in root.findall('item'):
		count += 1
		
	return count

# function to create XML file from URL containing today's data
def create_xml():
    # Create the variable to hold the desired write file
    reservations = open(usage_file, "w")
    # Create variables to hold the phrases we want to add to the beginning and end of new XML file
    doc_type = '<?xml version="1.0" encoding="utf-8" ?>\n'
    body_tag = '<reservation>\n'
    body = '</reservation>\n'
    # Write the necessary statements to beginning of XML doc
    reservations.write(doc_type)
    reservations.write(body_tag)
    url = ('http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&do=0')
    decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
    stripped_url_list = decoded_url[52:-14]
    reservations.write(stripped_url_list)
    # Write the end statements desired and close the file
    reservations.write(body)
    reservations.close()  

# main function that prints desired data and creates a csv file
# that organizes today's reservation data
def main():
	create_xml()
	my_file = open(usage_file, 'r')
	my_file2 = open(fixed_file, 'w')
	
	lines_of_file = my_file.readlines()
	
	# change invalid tokens
	for line in lines_of_file:
	    if '&amp;' in line:
	        line = line.replace("&amp;", "and")
	    my_file2.writelines(line)
	
	my_file.close()
	my_file2.close()
	
	# parse the xml file
	tree = ET.parse(fixed_file)
	root = tree.getroot()
	
	# create a csv file for writing
	resident_data = open(str(today) + '-reservationsToday.csv', 'w')
	
	# create the csv writer object
	csvwriter = csv.writer(resident_data)
	item_head = []
	
	header = True
	
	# loops through today's reservations and adds to the csv file
	for member in root.findall('item'):
		resident = []
		address_list = []
		
		# creates the header
		if header:
			date = member.find('date').tag
			item_head.append(date)
			time = member.find('time').tag
			item_head.append(time)
			description = member.find('description').tag
			item_head.append(description)
			location = member.find('location').tag
			item_head.append(location)
			csvwriter.writerow(item_head)
			header = False
			# creates a counter to count the amount of reservations today
			counter = 0
	
		date = member.find('date').text
		resident.append(date)
		time = member.find('time').text
		resident.append(time)
		description = member.find('description').text
		resident.append(description)
		location = member.find('location').text
		resident.append(location)
		csvwriter.writerow(resident)
		# increment counter
		counter += 1
		
	resident_data.close()
	
	# print out usage data
	print('Reservations today:', counter)
	# print('Reservations since last week:', reservations_since(-7))
	# print('Reservations since last month:', reservations_since(-30))
	# print()
	print('Reservations this week:', reservations_by_week())
	print('Reservations this month:', reservations_by_month())
	
main()
