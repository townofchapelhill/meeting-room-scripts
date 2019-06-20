import xml.etree.ElementTree as ET
import urllib.request
import csv
import datetime
import calendar

# set the date with and without time to variables
now = datetime.datetime.now()
today = datetime.date.today()

# set xml files to variables
usage_file = '//CHFS/Shared Documents/OpenData/datasets/staging/reservationData.xml'
fixed_file = '//CHFS/Shared Documents/OpenData/datasets/staging/convertedReservationData.xml'

# throw an error if a "/logs" directory doesn't exist
try:
    log_file = open('logs/' + str(today) + '-meetingslog.txt', 'w')
except:
    error_file = open('error.txt', 'w')
    error_file.write('ERROR - "logs" directory not found\n')
    error_file.close()


# function checks if a string is an ASCII (english characters only)
def is_ascii(s):
	return all(ord(c) < 128 for c in s)
	
# function counts the amount of reservations this week (Sunday to today)
def reservations_by_week():
	
	# create a file that holds all xml data this week
	weekly_monthly_data = open(usage_file, 'w')
	log_file.write('Temporary XML file for weekly data created.\n')
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
		try:
			decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
			stripped_url_list = decoded_url[52:-14]
			weekly_monthly_data.write(stripped_url_list)
			log_file.write("Day URL successfully accessed and decoded.\n")
		except:
			log_file.write("ERROR - URL access or decoding error\n")
	    
	weekly_monthly_data.write(body)
	weekly_monthly_data.close()
	
	my_file = open(usage_file, 'r')
	my_file2 = open(fixed_file, 'w')
	
	lines_of_file = my_file.readlines()
	
	# change the week's xml data to take away invalid tokens 
	# and save to a different file
	
	log_file.write('\nRemoving invalid tokens from xml file.\n')
	
	for line in lines_of_file:
		if is_ascii(line):
			pass
		else:
			for char in line:
				if is_ascii(char):
					continue
				else:
					line = line.replace(char, '?')
		my_file2.writelines(line)
	
	log_file.write('Temporary converted XML file created.\n')
	my_file.close()
	my_file2.close()
	
	# parse the xml file
	tree = ET.parse(fixed_file)
	root = tree.getroot()
	
	count = 0
	
	# count each <item> tag in the xml file to get reservations this week
	for member in root.findall('item'):
		count += 1
	
	log_file.write('\nAmount of reservations this week have been calculated.\n\n')	
	return count
	
# function counts the amount of reservations this month (1st to today)
def reservations_by_month():
	
	# create a file that holds all xml data this week
	weekly_monthly_data = open(usage_file, 'w')
	log_file.write('Temporary XML file for monthly data created.\n')
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
		try:
		    # Read and decode the XML file found at each url
			decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
			stripped_url_list = decoded_url[52:-14]
			weekly_monthly_data.write(stripped_url_list)
			log_file.write("Day URL successfully accessed and decoded.\n")
		except:
			log_file.write("ERROR - URL access or decoding error\n")
	    
	weekly_monthly_data.write(body)
	weekly_monthly_data.close()
	
	my_file = open(usage_file, 'r')
	my_file2 = open(fixed_file, 'w')
	
	lines_of_file = my_file.readlines()
	
	log_file.write('\nRemoving invalid tokens from XML file.\n')
	# change invalid tokens and placed converted into a new file
	
	for line in lines_of_file:
		if is_ascii(line):
			pass
		else:
			for char in line:
				if is_ascii(char):
					continue
				else:
					line = line.replace(char, '?')
		my_file2.writelines(line)
	
	log_file.write('Temporary converted XML file created.\n')
	my_file.close()
	my_file2.close()
	
	# parse the xml file
	
	tree = ET.parse(fixed_file)
	root = tree.getroot()
	
	# initialize counters
	count = 0
	room_a = 0
	room_b = 0
	room_c = 0
	room_d = 0
	dml1 = 0
	dml2 = 0
	dmls = 0
	
	# count each <item> tag to get monthly usage data
	# count each instance of each room usage
	for items in root.findall('item'):
		count += 1
		for locations in items.findall('location'):
			if locations.text == 'Meeting Room A':
			    room_a += 1
			elif locations.text == 'Meeting Room B':
			    room_b += 1
			elif locations.text == 'Meeting Room C':
			    room_c += 1
			elif locations.text == 'Meeting Room D':
			    room_d += 1
			elif locations.text == 'Digital Media Lab Workstation 1':
			    dml1 += 1
			elif locations.text == 'Digital Media Lab Workstation 2':
			    dml2 += 1
			elif locations.text == 'Digital Media Lab Studio':
			    dmls += 1
	
	log_file.write('\nAmount of reservations this month have been calculated.\n\n')	
	return count,room_a,room_b,room_c,room_d,dml1,dml2,dmls

# function counts the amount of reservations this year
def reservations_by_year():
	
	# create a file that holds all xml data this week
	weekly_monthly_data = open(usage_file, 'w')
	log_file.write('Temporary XML file for monthly data created.\n')
	doc_type = '<?xml version="1.0" encoding="utf-8" ?>\n'
	body_tag = '<reservation>\n'
	body = '</reservation>\n'
	weekly_monthly_data.write(doc_type)
	weekly_monthly_data.write(body_tag)

	# loop through XML URLs from the first of the month to today
	for month in range(1, now.month):
		for day in range(1, calendar.monthrange(now.year,month)[1]):
			
			# the url uses ds= to take in a date in the format YYYY/MM/DD
			url = ('http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&ds='+ str(now.year) \
			+ '/' + str(month) + '/' + str(day))
			try:
			    # Read and decode the XML file found at each url
				decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
				stripped_url_list = decoded_url[52:-14]
				weekly_monthly_data.write(stripped_url_list)
				log_file.write("Day URL successfully accessed and decoded.\n")
			except:
				log_file.write("ERROR - URL access or decoding error\n")
	    
	weekly_monthly_data.write(body)
	weekly_monthly_data.close()
	
	my_file = open(usage_file, 'r')
	my_file2 = open(fixed_file, 'w')
	
	lines_of_file = my_file.readlines()
	
	log_file.write('\nRemoving invalid tokens from XML file.\n')
	# change invalid tokens and placed converted into a new file
	for line in lines_of_file:
		if is_ascii(line):
			pass
		else:
			for char in line:
				if is_ascii(char):
					continue
				else:
					line = line.replace(char, '?')
		my_file2.writelines(line)
	
	log_file.write('Temporary converted XML file created.\n')
	my_file.close()
	my_file2.close()
	
	# parse the xml file
	
	tree = ET.parse(fixed_file)
	root = tree.getroot()
	
	count = 0
	
	# count each <item> tag to get monthly usage data
	for member in root.findall('item'):
		count += 1
	
	log_file.write('\nAmount of reservations this year have been calculated.\n\n')	
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
	try:
		url = ('http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&do=0')
		decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
		stripped_url_list = decoded_url[52:-14]
		log_file.write("Today's URL successfully accessed and decoded\n")
	except:
		log_file.write("ERROR - URL access or decoding error\n")
		
	reservations.write(stripped_url_list + '\n')
    # Write the end statements desired and close the file
	reservations.write(body)
	reservations.close()  

# main function that prints desired data and creates a csv file
# that organizes today's reservation data
def main():
	# calculate weekly
	log_file.write('Calculating reservations this week...\n')
	try:
		week_data = reservations_by_week()
	except:
		log_file.write('ERROR - there was an error in calculating the amount of reservations this week.\n')	
	
	# calcuate monthly
	log_file.write('Calculating reservations this month...\n')
	try:
		month_data, a, b, c, d, dl1, dl2, dls = reservations_by_month()
	except:
		log_file.write('ERROR - there was an error in calculating the amount of reservations this month.\n')	
	
	# calculate yearly
	log_file.write('Calculating reservations this year...\n')
	try:
		year_data = reservations_by_year() + month_data
	except:
		log_file.write('ERROR - there was an error in calculating the amount of reservations this year.\n')	

	log_file.write("Creating XML file for today's meetings.\n")
	try:
		create_xml()
	except:
	    log_file.write("ERROR - there was an error in the creating the XML file for today's reservations.\n")
	
	my_file = open(usage_file, 'r')
	my_file2 = open(fixed_file, 'w')
	
	lines_of_file = my_file.readlines()
	
	log_file.write('Removing invalid tokens from XML file.\n')
	# change invalid tokens
	for line in lines_of_file:
		if is_ascii(line):
			pass
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
	tree = ET.parse(fixed_file)
	root = tree.getroot()
	
	# create a csv file for writing
	reservation_data = open('//CHFS/Shared Documents/OpenData/datasets/staging/reservationsToday.csv', 'w')
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
				if grandchild.tag == "library":
					continue
				item_head.append(grandchild.tag)
			csvwriter.writerow(item_head)
			log_file.write("CSV header created, adding XML data to CSV file now...\n")
			header = False
			# creates a counter to count the amount of reservations today
			counter = 0
		
		# goes through each grandchild based on the child and appends rows to csv
		for grandchild in root[counter]:
			if grandchild.tag == "library":
				continue
			reservation_row.append(grandchild.text)
			
		csvwriter.writerow(reservation_row)
		
		# increment counter
		counter += 1
		
	log_file.write("Amount of reservations today calculated.\n\n")
	
	stats = [counter, week_data, month_data, year_data]
	
	# adds usage data to the csv file
	for i in range(len(stats)):
		row = []
		if i == 0:
			row.append('Reservations today:')
		elif i == 1:
			row.append('Reservations this week:')
		elif i == 2:
			row.append('Reservations this month:')
		else:
			row.append('Reservations this year:')
		row.append(stats[i])
		csvwriter.writerow(row)
	
	# calculate monthly percentages and append to csv
	log_file.write("Calculating Room Utilization for this month...")
	row_a = ['Meeting Room A:', a]
	row_b = ['Meeting Room B:', b]
	row_c = ['Meeting Room C:', c]
	row_d = ['Meeting Room D:', d] 
	row_dl1 = ['Digital Media Lab Workstation 1:', dl1]
	row_dl2 = ['Digital Media Lab Workstation 2:', dl2]
	row_dls = ['Digital Media Lab Studio:', dls]
	
	csvwriter.writerow(row_a)
	csvwriter.writerow(row_b)
	csvwriter.writerow(row_c)
	csvwriter.writerow(row_d)
	csvwriter.writerow(row_dl1)
	csvwriter.writerow(row_dl2)
	csvwriter.writerow(row_dls)

	
	reservation_data.close()
	
	log_file.write("Today's reservation data and usage data has been written to a CSV file.\n\n")
	
main()
log_file.write(str(datetime.datetime.now()))
log_file.close()

