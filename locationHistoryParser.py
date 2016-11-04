#!/bin/python

# Google Maps JSON parser
# Author:	D. Scott Boggs
#	 		scott@tams.tech
#
#	The Google Maps JSON file for your location history and parses it as a CSV
#	Please note this outputs the CSV directly to STDOUT, following the standard
#	used by csvtools for GNU/Linux

import sys
import re

mapsFile = open('LocationHistory.json') #the file to be parsed
rowDivider = "  }, {"		#copypasted from the JSON file
column_titles = ["timestampMs","latitudeE7","longitudeE7","accuracy","ACTtimestampMs", "onFoot", "inVehicle", "onBicycle", "still", "walking", "running", "exitingVehicle", "tilting", "unknown"]
lastEntry = ""			#initialize the string that will hold the end file
arrayLevel=0
currentLine = [",",",",",",",",",",",",",",",",",",",",",",",",",",","]
currentItem = ""
previousItem = ""
DEBUG=0
def numberOfCommas(s):
	return len(re.findall(',',s))

for s in column_titles:		#for each of the titles of the columns of the csv,
	sys.stdout.write(s+",")		#add the title and a comma,
sys.stdout.write("\n")			#then a newline to begin adding data
for line in mapsFile:		# iterate through the file line by line
	previousItem = currentItem
	currentItem=line		# save the current line as a string
	if arrayLevel==1:		# All following conditions depend on being within the "Location" or first-level array
		if rowDivider in currentItem:		#reference rowDivider set in line 7
			for s in currentLine:
				sys.stdout.write(s)
			sys.stdout.write("\n")
			currentLine = [",",",",",",",",",",",",",",",",",",",",",",",",",",","]
		elif column_titles[0] in currentItem and arrayLevel==1:	# check for the first column title in the current line
			currentLine[0]=currentItem.split(":")[1][1:-1]	# splits the current line at the : selects everything after that, 
		elif column_titles[1] in currentItem:					# then drops the first and last characters (which is a space and
			currentLine[1]=currentItem.split(":")[1][1:-1]	# newline symbol, respectively, for every entry)
		elif column_titles[2] in currentItem:
			currentLine[2]=currentItem.split(":")[1][1:-1]	# and each of these other elif statements do the same thing for each of the other column titles
		elif column_titles[3] in currentItem:
			currentLine[3]=currentItem.split(":")[1][1:-1]
	elif arrayLevel==2:
		if column_titles[0] in currentItem:
			for s in currentLine:
				sys.stdout.write(s)
			sys.stdout.write("\n")
			currentLine=[",",",",",",",",currentItem.split(":")[1][1:-1],",",",",",",",",",",",",",",",",","]
	elif arrayLevel==3:
		if column_titles[5] in previousItem and "confidence" in currentItem:
			#while numberOfCommas(currentLine)<5:
				#currentLine+=","
			currentLine[5]=currentItem.split(":")[1][1:-1] + ","
		elif column_titles[6] in previousItem and "confidence" in currentItem:
			#while numberOfCommas(currentLine)<6:
			#	currentLine+=","
			currentLine[6]=currentItem.split(":")[1][1:-1] + ","
		elif column_titles[7] in previousItem and "confidence" in currentItem:
			#while numberOfCommas(currentLine)<7:
			#	currentLine+=","
			currentLine[7]=currentItem.split(":")[1][1:-1] + ","
		elif column_titles[8] in previousItem and "confidence" in currentItem:
			#while numberOfCommas(currentLine)<8:
			#	currentLine+=","
			currentLine[8]=currentItem.split(":")[1][1:-1] + ","
		elif column_titles[9] in previousItem and "confidence" in currentItem:
			#while numberOfCommas(currentLine)<9:
			#	currentLine+=","
			currentLine[9]=currentItem.split(":")[1][1:-1] + ","
		elif column_titles[10] in previousItem and "confidence" in currentItem:
			#while numberOfCommas(currentLine)<10:
			#	currentLine+=","
			currentLine[10]=currentItem.split(":")[1][1:-1] + ","
		elif column_titles[11] in previousItem and "confidence" in currentItem:
			#while numberOfCommas(currentLine)<11:
			#	currentLine+=","
			currentLine[11]=currentItem.split(":")[1][1:-1] + ","
		elif column_titles[12] in previousItem and "confidence" in currentItem:
			#while numberOfCommas(currentLine)<12:
			#	currentLine+=","
			currentLine[12]=currentItem.split(":")[1][1:-1] + ","
		elif column_titles[13] in previousItem and "confidence" in currentItem:
			#while numberOfCommas(currentLine)<13:
			#	currentLine+=","
			currentLine[13]=currentItem.split(":")[1][1:-1] + ","
	if "[ {" in currentItem:	#watch for array initialization character
		arrayLevel+=1			#and adjust the array level accordingly
		if DEBUG: print(arrayLevel)
	if "} ]" in currentItem:
		arrayLevel-=1			# ^^ likewise ^^
		if DEBUG: print(arrayLevel)
