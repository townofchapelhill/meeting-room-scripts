from xml.dom import minidom
from xml.dom.minidom import Document
import os
import urllib.request
import csv
import re
import sys

day = -143

class Reservation(object):
    def __init__(self, startDate=None, startTime=None, endDate=None, endTime=None, description=None, location=None, status=None):
        self.startDate = ''
        self.startTime = ''
        self.endDate = ''
        self.endTime = ''
        self.description = ''
        self.location = ''
        self.status = ''

# def clear_file(day):
#     try:
#         if os.stat('aggregate_reservations.csv').st_size != 0:
#             os.remove('aggregate_reservations.csv')
#     except:
#         pass
#     get_reservations(day)

def get_reservations(day):
    reservations = []
    
    if day == 1:
        sys.exit()

    url = "http://chapelhill.evanced.info/spaces/patron/spacesxml?dm=xml&do=" + str(day)
    decoded_url = urllib.request.urlopen(url).read().decode('utf-8')
    stripped_url_list = "<root>" + decoded_url[52:-14] + "</root>" + "\n"

    with open("reservations.xml", "w", encoding="utf-8") as dump_file:
        dump_file.write(stripped_url_list)

    parse_xml(day)

def parse_xml(day):
    obj_reservations = []
    xmldoc = minidom.parse("reservations.xml")
    res_list = xmldoc.getElementsByTagName('item')
    for item in res_list:
        new_res = Reservation()
        new_res.startDate = item.firstChild.firstChild.nodeValue

        startTime_list = item.getElementsByTagName('time')
        for time in startTime_list:
            new_res.startTime = time.firstChild.nodeValue
        
        endDate_list = item.getElementsByTagName('enddate')
        for endDate in endDate_list:
            new_res.endDate = endDate.firstChild.nodeValue
        
        endTime_list = item.getElementsByTagName('endtime')
        for endTime in endTime_list:
            new_res.endTime = endTime.firstChild.nodeValue

        description_list = item.getElementsByTagName('description')
        for description in description_list:
            new_res.description = description.firstChild.nodeValue

        location_list = item.getElementsByTagName('location')
        for location in location_list:
            new_res.location = location.firstChild.nodeValue

        status_list = item.getElementsByTagName('status')
        for status in status_list:
            new_res.status = status.firstChild.nodeValue
        
        obj_reservations.append(new_res.__dict__)
        try:
            os.remove('reservations.xml')
        except:
            pass
    
    write_csv(obj_reservations, day)

def write_csv(obj_reservations, day):
    for res in obj_reservations:
        scrubbed_value = re.sub('[^A-Za-z0-9_\-\.: ]', ' ', str(res['description']))
        res['description'] = scrubbed_value

    with open('aggregate_reservations.csv', 'a') as res_headers:
        try:
            fieldnames = obj_reservations[0].keys()
            csv_writer = csv.DictWriter(res_headers, fieldnames=fieldnames, extrasaction='ignore', delimiter=',')
        except:
            pass

        if os.stat('aggregate_reservations.csv').st_size == 0:
            csv_writer.writeheader()
        
        for entry in obj_reservations:
            csv_writer.writerow(entry)
    
    day += 1
    print(day)
    get_reservations(day)

# clear_file(day)
get_reservations(day)