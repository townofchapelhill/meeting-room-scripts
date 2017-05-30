# import the necessary tools to parse xml and create a csv file
import xml.etree.ElementTree as ET
import csv

# parse the xml file
tree = ET.parse("nextBus.xml")
root = tree.getroot()

# open a file for writing
bus_data = open('nextBus.csv', 'w')

# create the csv writer object
csvwriter = csv.writer(bus_data)
item_head = []

# use boolean to determine header in loop
header = True

# loop through the each route in the root (<body>)
for route in root.findall('route'):

	if header:
		item_head.append('Bus')
		item_head.append('Title')
		item_head.append('Schedule Class')
		item_head.append('Days')
		item_head.append('Direction')
		item_head.append('blockID')
		item_head.append('Stop Name')
		item_head.append('Stop Times')
		# write back to csvwriter
		csvwriter.writerow(item_head)
		header = False
	
	# save a list of id's to know if they are already added in
	id_list = []
	
	# loop through each <tr> in the routes
	for tr in route.findall('tr'):
		if tr.attrib['blockID'] not in id_list:
			# loop through each stop and add the header info into list
			for stop in tr.findall('stop'):
				bus_info = []
				bus = route.attrib['tag']
				bus_info.append(bus)
				title = route.attrib['title']
				bus_info.append(title)
				schedule = route.attrib['scheduleClass']
				bus_info.append(schedule)
				days = route.attrib['serviceClass']
				bus_info.append(days)
				direction = route.attrib['direction']
				bus_info.append(direction)
				blockID = tr.attrib['blockID']
				bus_info.append(blockID)
				id_list.append(blockID)
				stop_n = stop.attrib['tag']
				bus_info.append(stop_n)
				
				# loop allows for stop times to be in the correct order and row
				for second_tr in route.findall('tr'):
					if second_tr.attrib['blockID'] == tr.attrib['blockID']:
						for second_stop in second_tr.findall('stop'):
							if second_stop.attrib['tag'] == stop.attrib['tag']:
								bus_info.append(second_stop.text)
								
				# append the bus_info list onto the next row in csv file				
				csvwriter.writerow(bus_info)

# close the file
bus_data.close()