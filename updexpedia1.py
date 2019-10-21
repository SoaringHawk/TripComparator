import argparse, os, sys, datetime, json, re, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time
import csv

csv_file = open('route_data', 'a')
route_writer = csv.writer(csv_file)
#route_writer.writerow(['Route', 'Sum'])

csv_file = open('flight_data', 'a')
flight_writer = csv.writer(csv_file)


#functions
def startBrowser(headless=False):
	global browser
	profile = webdriver.ChromeOptions()
	profile.add_argument('--no-sandbox')
	prefs = {"profile.managed_default_content_settings.images": 2}
	profile.add_experimental_option("prefs", prefs)
	if headless: profile.add_argument('--headless')
	browser = webdriver.Chrome(executable_path=chromedriver, options=profile)
	browser.set_page_load_timeout(100)
	
	browser.set_window_size(1224, 786)

def getRoute(dep, arr, dt):
	global browser, flight_writer, inpData
	dt = dt.strftime('%m/%d/%Y')
	route = {"from":dep,"to":arr,"date":dt,"cost":9999,"dep-time":None,"arr-time":None}

	while(True):
		
		with open('flight_data', 'r+') as f:
			flight_reader = csv.reader(f)
			counter = 0
			for ids,row in enumerate (flight_reader):
				if len(row) > 0:
					if ids == counter:
						#print('pass')
						row[0] = datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S')
						if row[1] == route["from"] and row[2] ==route["to"] and row[3] == route["date"] and datetime.datetime.now() - row[0] < datetime.timedelta(hours=24):
							#print('pass')
							route = {"from":row[1],"to":row[2],"date":row[3],"cost":(int)(row[4]),"dep-time":row[5],"arr-time":row[6]}
							if route not in inpData["routes"]:
								print('Route already calculated')
								return route
				counter+=1

		q = "https://www.expedia.com/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=children:0,adults:1,seniors:0,infantinlap:Y".format(dep,arr,dt)
		browser.get(q)	
				
		try:
			time.sleep(1)
			browser.find_element_by_xpath('//*[@id="departure-times"]/div/div[2]/div/label').click()
			time.sleep(1)
			results = browser.find_element_by_id("flightModuleList").find_elements_by_tag_name("li")
			result = results[0]
		except AttributeError: return None
		
		try:
			cost = (int)(result.find_element_by_xpath('//span[@data-test-id="listing-price-dollars"]').text.replace(",","").replace("$",""))
			if cost==9999:
				time.sleep(1)
				continue
			
			if cost < route["cost"]:
				route["cost"] = cost
				route["dep-time"] = result.find_element_by_xpath('//span[@data-test-id="departure-time"]').text
				route["arr-time"] = result.find_element_by_xpath('//span[@data-test-id="arrival-time"]').text
				flight_writer.writerow([datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), route["from"], route["to"], route["date"], route["cost"], route["dep-time"], route["arr-time"]])
			
			break
		except: time.sleep(1)

	return route
	
#def getRoute1(dep, arr, dt):
#	global browser
#	route = {"from":dep,"to":arr,"date":dt,"cost":9999,"dep-time":None,"arr-time":None}
	
#	while(True):
#		q = "https://www.expedia.com/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=children:0,adults:1,seniors:0,infantinlap:Y".format(dep,arr,dt)
#		browser.get(q)	
				
#		try:
#			time.sleep(1)
#			browser.find_element_by_xpath('//*[@id="departure-times"]/div/div[3]/div/label').click()
#			time.sleep(1)
#			results = browser.find_element_by_id("flightModuleList").find_elements_by_tag_name("li")
#			result = results[0]
#		except AttributeError: return None
		
#		try:
#			cost = (int)(result.find_element_by_xpath('//span[@data-test-id="listing-price-dollars"]').text.replace(",","").replace("$",""))
#			if cost==9999:
#				time.sleep(1)
#				continue
			
#			if cost < route["cost"]:
#				route["cost"] = cost
#				route["dep-time"] = result.find_element_by_xpath('//span[@data-test-id="departure-time"]').text
				
				
#				route["arr-time"] = result.find_element_by_xpath('//span[@data-test-id="arrival-time"]').text
				

#			break
#		except: time.sleep(1)

#	return route

def getRoute2(dep, arr, dt):
	global browser, flight_writer, inpData
	dt = dt.strftime('%m/%d/%Y')
	route = {"from":dep,"to":arr,"date":dt,"cost":9999,"dep-time":None,"arr-time":None}

	while(True):
		
		with open('flight_data', 'r+') as f:
			flight_reader = csv.reader(f)
			counter = 0
			for ids,row in enumerate (flight_reader):
				if len(row) > 0:
					if ids == counter:
						#print('pass')
						row[0] = datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S')
						if row[1] == route["from"] and row[2] ==route["to"] and row[3] == route["date"] and datetime.datetime.now() - row[0] < datetime.timedelta(hours=24):
							#print('pass')
							route = {"from":row[1],"to":row[2],"date":row[3],"cost":(int)(row[4]),"dep-time":row[5],"arr-time":row[6]}
							if route not in inpData["routes"]:
								print('Route already calculated')
								return route
				counter+=1

		q = "https://www.expedia.com/Flights-Search?flight-type=on&mode=search&trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=children:0,adults:1,seniors:0,infantinlap:Y".format(dep,arr,dt)
		browser.get(q)	
				
		try:
			time.sleep(1)
			browser.find_element_by_xpath('//*[@id="departure-times"]/div/div[4]/div/label').click()
			time.sleep(1)
			results = browser.find_element_by_id("flightModuleList").find_elements_by_tag_name("li")
			result = results[0]
		except AttributeError: return None
		
		try:
			cost = (int)(result.find_element_by_xpath('//span[@data-test-id="listing-price-dollars"]').text.replace(",","").replace("$",""))
			if cost==9999:
				time.sleep(1)
				continue
			
			if cost < route["cost"]:
				route["cost"] = cost
				route["dep-time"] = result.find_element_by_xpath('//span[@data-test-id="departure-time"]').text
				route["arr-time"] = result.find_element_by_xpath('//span[@data-test-id="arrival-time"]').text
				flight_writer.writerow([datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), route["from"], route["to"], route["date"], route["cost"], route["dep-time"], route["arr-time"]])
			
			break
		except: time.sleep(1)

	return route

def getFilteredFlights(date,dep,lastpoint):
	global FLIGHTS, VISITED, inpData
	results = []
	for flight in FLIGHTS:
		if (date-flight["date"]) <= (inpData["travelDates"][1]-inpData["travelDates"][0]) and (date-flight["dep-time"]) <= (inpData["travelDates"][1]-inpData["travelDates"][0]) and flight["from"]==dep and (flight["arr-time"]-flight["dep-time"])> datetime.timedelta(hours=1 ) and flight["to"]!=lastpoint and flight["to"] not in VISITED:
			results.append(flight)
			
	return results
			

def getFlight(endDate,dep,arr):
	global FLIGHTS
	
	for flight in FLIGHTS:
		if (endDate-flight["date"]) <= (inpData["travelDates"][1]-inpData["travelDates"][0]) and (endDate-flight["dep-time"]) <= (inpData["travelDates"][1]-inpData["travelDates"][0]) and flight["from"]==dep and flight["to"]==arr:
			return flight
	return None
	
def getRoutes(currentAirport,currentDate,lastpoint):
	global inpData, DATA, PATH, FLIGHTS, DATES, VISITED, min_staying_time 
	#print("\n\n"+currentAirport+" - "+currentDate)

	
	# check if is last date
	if len(PATH) > i: 
		flight = getFlight(currentDate,currentAirport,lastpoint)
		PATH.append(flight)
		DATA.append(PATH)
		
		#print("Finish")
		#print(flight)
		#print(PATH)
		#print(VISITED)
		
		PATH = PATH[:-1]
		VISITED = VISITED[:-1]
		return
		
	flights = getFilteredFlights(currentDate,currentAirport,lastpoint)
	#print(flights)
	for flight in flights:
		if len(PATH) > 0 and (flight["dep-time"]-PATH[-1]["arr-time"]) > datetime.timedelta(hours= min_staying_time):
			VISITED.append(flight["from"])
			#print(airports_list)
			PATH.append(flight)
			#print(PATH)
			getRoutes(flight["to"],DATES[(len)(PATH)],lastpoint)
			PATH = PATH[:-1]
			VISITED = VISITED[:-1]

		elif len(PATH) == 0:
			VISITED.append(flight["from"])
			#print(airports)
			PATH.append(flight)
			#print(PATH)
			getRoutes(flight["to"],DATES[(len)(PATH)],lastpoint)
			PATH = PATH[:-1]
			VISITED = VISITED[:-1]
	
	return


def bubbleSort(arr):
	n = len(arr)

	for i in range(n):
		for j in range(0, n-i-1):
			if arr[j]["sum"] > arr[j+1]["sum"]:
				arr[j], arr[j+1] = arr[j+1], arr[j]
				
	return arr

# init
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

#argparser = argparse.ArgumentParser()
#argparser.add_argument('airports',help = 'Comma seperated airports, no spaces')
#argparser.add_argument('startdate',help = 'Start date for trip')
#argparser.add_argument('enddate',help = 'End ate for trip')
#argparser.add_argument('startpoint',help = 'Enter start point')
#args = argparser.parse_args()
startdate = input('Enter a startdate i.e: 2019-10-05 ')
enddate = input('Enter a enddate i.e: 2019-10-06 ')
airports = input('Enter airport separated by comma ')
startpoint = input('Enter a startpoint ')
min_staying_time = (int)(input('Enter the minimum staying time in hours i.e: 24 '))


try:
	inpData = {
		"startDate":datetime.datetime.strptime(startdate, '%Y-%m-%d'),
		"endDate":datetime.datetime.strptime(enddate, '%Y-%m-%d'),
		"tripDays":0,
		"destinations":airports.split(","),
		"startPoint":startpoint,
		"travelDates":[],
		"routes":[]
	}
	inpData["tripDays"] = ((inpData["endDate"] - inpData["startDate"]).total_seconds())/3600
except ValueError:
	print("Wrong date format")
	sys.exit(2)

if inpData["startDate"] > inpData["endDate"]:
	print("End Date must be before Start Date")
	sys.exit(1)

if inpData["tripDays"]/24 >= (len)(inpData["destinations"]):
	daysOnEachLocation = (int)((inpData["tripDays"]/24) / (len)(inpData["destinations"]))
	remains = (inpData["tripDays"]/24) % (len)(inpData["destinations"])
	currentDate = inpData["startDate"]
	inpData["travelDates"].append(currentDate)
	for location in inpData["destinations"]:
		currentDate = currentDate+datetime.timedelta(days=daysOnEachLocation)
		inpData["travelDates"].append(currentDate)
	inpData["travelDates"][-1] = inpData["travelDates"][-1]+datetime.timedelta(days=remains)

elif inpData["tripDays"]/24 < (len)(inpData["destinations"]):
	timeOnEachLocation = (int)((inpData["tripDays"]) / (len)(inpData["destinations"]))
	remains = (inpData["tripDays"]) % (len)(inpData["destinations"])
	currentDate = inpData["startDate"]
	inpData["travelDates"].append(currentDate)
	for location in inpData["destinations"]:
		currentDate = currentDate+datetime.timedelta(hours=timeOnEachLocation)
		inpData["travelDates"].append(currentDate)
	inpData["travelDates"][-1] = inpData["travelDates"][-1]+datetime.timedelta(hours=remains)



else:
	print("Destinations cannot be more than trip days")
	sys.exit(1)
	
	currentDate = inpData["startDate"]
	for day in range(inpData["tripDays"]):
		inpData["travelDates"].append(currentDate)
		currentDate = currentDate+datetime.timedelta(days=1)
	

# Main
browser = None
startBrowser()
try:
	inpData["destinations"].append(inpData["startPoint"])
	for i, dep in enumerate(inpData["destinations"]):
		for j, arr in enumerate(inpData["destinations"]):
			if i!=j:
				for travelDate in inpData["travelDates"]:
					#print(travelDate.strftime('%m/%d/%Y')+" "+dep+" "+arr+" "+inpData["startPoint"]+" "+inpData["endDate"].strftime('%m/%d/%Y'))
					if travelDate == inpData["startDate"] and dep != inpData["startPoint"]: continue
					if travelDate == inpData["endDate"] and arr != inpData["startPoint"]: continue
					if dep==inpData["startPoint"] and travelDate != inpData["startDate"]: continue
					if arr==inpData["startPoint"] and travelDate != inpData["endDate"]: continue
					
					for innertravel in range(len(inpData["travelDates"])):
						if travelDate >= inpData["startDate"]:
							route = getRoute(dep,arr,travelDate)
							if route!=None and route["cost"]!=9999:
								try:
									route["dep-time"] = datetime.datetime.strptime(route["dep-time"], '%I:%M%p')
									zero = datetime.datetime.strptime('12:00am', '%I:%M%p')
									raw_time = route["dep-time"] - zero
									route["date"] = datetime.datetime.strptime(route["date"], '%m/%d/%Y')
									route["dep-time"] = route["date"] + raw_time
									
									route["arr-time"] = datetime.datetime.strptime(route["arr-time"], '%I:%M%p')
									raw_time = route["arr-time"] - zero
									if route["arr-time"] < datetime.datetime.strptime('16:00', '%H:%M') and route["dep-time"]+datetime.timedelta(hours=7) >route["date"]+datetime.timedelta(days=1):
										route["arr-time"] = (route["date"]+ datetime.timedelta(days= 1)) + raw_time
									else:
										route["arr-time"] = route["date"] + raw_time
									#route["date"] = route["date"].strftime('%m/%d/%Y')
								except: 
									pass
								if route not in inpData["routes"]:
									inpData["routes"].append(route)
									print("[{0}][Cost: {1}$] Route Found: [{2} {3}] -> [{4} {5}]".format(route["date"],route["cost"],route["from"],route["dep-time"],route["to"],route["arr-time"]))

							#route = getRoute1(dep,arr,travelDate)
							#if route!=None and route["cost"]!=9999:
							#	try:
							#		route["dep-time"] = datetime.datetime.strptime(route["dep-time"], '%I:%M%p')
							#		zero = datetime.datetime.strptime('12:00am', '%I:%M%p')
							#		raw_time = route["dep-time"] - zero
							#		route["date"] = datetime.datetime.strptime(route["date"], '%m/%d/%Y')
							#		route["dep-time"] = route["date"] + raw_time
									
							#		route["arr-time"] = datetime.datetime.strptime(route["arr-time"], '%I:%M%p')
							#		raw_time = route["arr-time"] - zero
							#		route["arr-time"] = route["date"] + raw_time
									#route["date"] = route["date"].strftime('%m/%d/%Y')
							#	except:
							#		pass

							#	inpData["routes"].append(route)
							#	print("[{0}][Cost: {1}$] Route Found: [{2} {3}] -> [{4} {5}]".format(route["date"],route["cost"],route["from"],route["dep-time"],route["to"],route["arr-time"]))

							############## uncomment this part for more flights#################
							#route = getRoute2(dep,arr,travelDate)
							#if route!=None and route["cost"]!=9999:
							#	try:
							#		route["dep-time"] = datetime.datetime.strptime(route["dep-time"], '%I:%M%p')
							#		zero = datetime.datetime.strptime('12:00am', '%I:%M%p')
							#		raw_time = route["dep-time"] - zero
							#		route["date"] = datetime.datetime.strptime(route["date"], '%m/%d/%Y')
							#####		route["dep-time"] = route["date"] + raw_time
							#		
							#		route["arr-time"] = datetime.datetime.strptime(route["arr-time"], '%I:%M%p')
							#####		raw_time = route["arr-time"] - zero
							#		if route["arr-time"] < datetime.datetime.strptime('16:00', '%H:%M') and route["dep-time"]+datetime.timedelta(hours=5) >route["date"]+datetime.timedelta(days=1):
							#			route["arr-time"] = (route["date"]+ datetime.timedelta(days= 1)) + raw_time
							#		else:
							####			route["arr-time"] = route["date"] + raw_time
									#route["date"] = route["date"].strftime('%m/%d/%Y')
							#	except:
							#		pass

							#	inpData["routes"].append(route)
							#	print("[{0}][Cost: {1}$] Route Found: [{2} {3}] -> [{4} {5}]".format(route["date"],route["cost"],route["from"],route["dep-time"],route["to"],route["arr-time"]))
								
								

						travelDate = travelDate + (inpData["travelDates"][0]-inpData["travelDates"][1])//(len(inpData["travelDates"]))


	browser.quit()
except KeyboardInterrupt:
	browser.quit()
	print("Terminated by the user")


#inpData["startDate"] = inpData["startDate"].strftime('%m/%d/%Y %H:%M')
#inpData["endDate"] = inpData["endDate"].strftime('%m/%d/%Y %H:%M')

#print(inpData)

# Calculate routes
DATA = []
PATH = []
FLIGHTS = inpData["routes"]
DATES = []
VISITED = []

for tmp in inpData["travelDates"]:
	DATES.append(tmp)

i = 0

while i < len(inpData["destinations"]):
	getRoutes(startpoint,inpData["startDate"],startpoint)
	i += 1


# Calculate cost(s)
final = []
for routes in DATA:
	tmp = {"sum":0,"routes":routes}
	for route in routes: tmp["sum"]+=route["cost"]
	final.append(tmp)
		
# Sort by Sums
final = bubbleSort(final)

# Print
print("\n#############\nResult(s)")
for record in final:
	tmp = ""
	for route in record["routes"]:
		tmp+="{0}->{1}({2})({3}$) ".format(route["from"],route["to"],route["dep-time"],route["cost"])
	tmp1 = "-> SUM: {0}$".format(record["sum"])
	route_writer.writerow([tmp, tmp1])
	print(tmp+"-> SUM: {0}$".format(record["sum"]))
if len(final) == 0:
	print('No result? \n You may adjust your parameter to obtaint more flights \n decrease your staying time or uncomment the getRoute2 function \n to get more flights ')
