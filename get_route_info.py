import urllib.request
import zipfile
import csv
from datetime import datetime
from time import sleep
from display import *

def update_basic_info():
	url = 'http://rtcws.rtcsnv.com/g/google_transit.zip'
	urllib.request.urlretrieve(urz, '/home/pi/Documents/oled/oled.zip')
	with zipfile.ZipFile('/home/pi/Documents/oled/oled.zip', 'r') as zip_ref:
		zip_ref.extractall('/home/pi/Documents/oled/route_info')

def get_info(file):
	folder = '/home/pi/Documents/oled/route_info'
	file = f'{file}.txt'
	with open(f'{folder}/{file}') as f:
		reader = csv.reader(f, delimiter=',')
		info = []
		for row in reader:
			info.append(row)
	return(info)

def time_check(stop_times):
	date = datetime.strftime(datetime.now(), '%Y-%m-%d')
	for stop in range(len(stop_times)):
		for c in [1,2]:
			if int(stop_times[stop][c][:2]) > 23:
				stop_times[stop][c] = f'{int(stop_times[stop][c][:2]) - 24}{stop_times[stop][c][2:]}'
				#Add one day to date for times past 1
			stop_times[stop][c] = f'{date} {stop_times[stop][c]}'
	return(stop_times)

def next_stop_info(nearby_stop_times):
	trips_dict = {}
	for i in trips:
		trips_dict[i[2]] = i[3]
	for stop in nearby_stop_times:
		stop.append(trips_dict[stop[0]])
	routes = []
	for stop in nearby_stop_times:
		if stop[-1] not in routes:
			routes.append(stop[-1])
	next_stop = {}
	for route in routes:
		filtered_stops = [stop for stop in nearby_stop_times if stop[-1] == route and datetime.strptime(stop[1], date_format) > datetime.now()]
		if route not in next_stop.keys():
			next_stop[route] = filtered_stops[0]
		for stop in filtered_stops:
			if datetime.strptime(next_stop[route][1], date_format) > datetime.strptime(stop[1], date_format):
				next_stop[route] = stop
		return(next_stop)	

def format_stops(stop_info):
	for stop in stop_info.keys():
		print(f'{stop} - {stop_info[stop][1]}')

def get_updates():
	url = 'http://rtcws.rtcsnv.com/gtfrt/tripUpdates.pb'
	feed = gtfs.realtime_pb2.FeedMessage()
	response = urllib.requests.open(url)
	feed.ParseFromString(response.read())
	return(feed)

def check_updates():
	for entity in feed.entity:
                if entity.HasField('trip_update'):
                        pass

def display_text(stop):
	if stop[10] == '110 Eastern Northbound':
		rsb = ('110 Eastern - Northbound')
	elif stop[10] == '110 Eastern Southbound':
		rsb = ('110 Easten - Southbound')
	elif stop[10] == '203 Spring Mtn & Desert Inn Eastbound / Lamb Northbound':
		rsb = ('203 Desert Inn - Eastbound')
	elif stop[10] == '203 Lamb Southbound / Desert Inn & Spring Mtn Westbound':
		rsb = ('203 Desert Inn - Westbound')	
	
	return((rsb, stop[1], stop[2]))

if __name__ == '__main__':
	files = ['stop_times', 'stops', 'routes', 'agency', 'trips', 'calendar', 'calendar_dates', 'shapes']
	date_format = '%Y-%m-%d %H:%M:%S'
	for file in files:
		exec(f'{file} = get_info("{file}")')

	nearby_stops = ['775', '776', '838', '839']
	nearby_stop_times = time_check([i for i in stop_times if i[3] in nearby_stops])

	while True:
		next_stop = next_stop_info(nearby_stop_times)
		for stop in next_stop.keys():
			display(*display_text(next_stop[stop]))
			sleep(5)
