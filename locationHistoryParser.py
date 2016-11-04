#!/bin/python

# Google Maps JSON parser
# Author:	D. Scott Boggs
#	 		scott@tams.tech
#
#	Looks in its directory for the Google Maps JSON file for your 
#	location history and parses it as a CSV

#	Please note this outputs the CSV directly to STDOUT, following the standard
#	used by csvkit for GNU/Linux, but it does not accept the JSON file to stdin,
#	the way in2csv does.

import sys

try:
	mapsFile = open('LocationHistory.json') #the file to be parsed
except IOError:
	print("Please place LocationHistory.json in the same folder as this script before running it")
	exit(1)
rowDivider = "  }, {"		#copypasted from the JSON file
column_titles = ["timestampMs","latitudeE7","longitudeE7","accuracy","ACTtimestampMs", "onFoot", "inVehicle", "onBicycle", "still", "walking", "running", "exitingVehicle", "tilting", "unknown"]
lastEntry = ""			#initialize the string that will hold the end file
arrayLevel=0
currentLine = [",",",",",",",",",",",",",",",",",",",",",",",",",",","]	#Initialize the currentLine array with blank csv cells, AKA one comma each
currentItem = ""
previousItem = ""
DEBUG=0			#value to print extra data for debugging
for s in column_titles:		#for each of the titles of the columns of the csv,
	sys.stdout.write(s+",")		#add the title and a comma,
sys.stdout.write("\n")			#then a newline to begin adding data
for line in mapsFile:				# iterate through the file line by line. Each line of the file is either zero or one cell in the final sheet
	previousItem = currentItem		# first, save the previous line for reference (when dealing with the "Activitys" sub-arrays)
	currentItem=line				# then, save the current line
	if arrayLevel==1:				# All following conditions depend on being within the "Location" or first-level array
		if rowDivider in currentItem:		#watches for the rowDivider string that was set @line 7, which indicates a new timestamp entry
			for s in currentLine:	# !!	this is important, it iterates through the "currentLine" array, which contains one csv cell per array cell
				sys.stdout.write(s) #		and writes each string directly to stdout. Originally, I saved the whole sheet to a string and printed it,
									#		but printing directly to stdout will take a lot less memory, which is important as your final .csv will be
									#		tens, if not hundreds of MB.
			sys.stdout.write("\n")	#	Adds a newline after the whole array is printed
			currentLine = [",",",",",",",",",",",",",",",",",",",",",",",",",",","]		#and resets the array to be blank.
		elif column_titles[0] in currentItem and arrayLevel==1:	# check for the first column title in the current line
			currentLine[0]=currentItem.split(":")[1][1:-1]		# splits the current line at the : selects everything after that, 
		elif column_titles[1] in currentItem:					# then drops the first and last characters (which is a space and
			currentLine[1]=currentItem.split(":")[1][1:-1]		# newline symbol, respectively, for every entry)
		elif column_titles[2] in currentItem:
			currentLine[2]=currentItem.split(":")[1][1:-1]		# and each of these other elif statements do the same thing for each of the other column titles
		elif column_titles[3] in currentItem:					# up to "Accuracy", covering everything in the first level of the array
			currentLine[3]=currentItem.split(":")[1][1:-1]
	elif arrayLevel==2:								# !!	This code deals with the sub-array "Activitys" and their values.
		if column_titles[0] in currentItem:			# if there's a timestamp, we're dealing with a new activitys entry.
			for s in currentLine:					# print it,
				sys.stdout.write(s)
			sys.stdout.write("\n")					# and start a new line.
			currentLine=[",",",",",",",",currentItem.split(":")[1][1:-1],",",",",",",",",",",",",",",",",","]	#then reinitialize the line with the timestamp value under the 'ACTtimestamp' header
					
						# note that this ^^ was a stylistic choice. If you don't like the layout of the .csv file, feel free to rearrange this code to stylize it how you would like
	elif arrayLevel==3:
		if column_titles[5] in previousItem and "confidence" in currentItem:		#check each item to see if the column 6-14 headers are present in the
			currentLine[5]=currentItem.split(":")[1][1:-1] + ","					#	PREVIOUS item, and if the word "confidence" is present in the CURRENT item.
		elif column_titles[6] in previousItem and "confidence" in currentItem:
			currentLine[6]=currentItem.split(":")[1][1:-1] + ","					# then adds the confidence value to the proper cell, and a comma.
		elif column_titles[7] in previousItem and "confidence" in currentItem:
			currentLine[7]=currentItem.split(":")[1][1:-1] + ","					# a couple of notes:
		elif column_titles[8] in previousItem and "confidence" in currentItem:		#		1 - this means that the values in the cells for each of the "Activities"
			currentLine[8]=currentItem.split(":")[1][1:-1] + ","					#			(note the use of ie and y to differentiate in the JSON) is actually the
		elif column_titles[9] in previousItem and "confidence" in currentItem:		#			confidence level for that Activitie
			currentLine[9]=currentItem.split(":")[1][1:-1] + ","
		elif column_titles[10] in previousItem and "confidence" in currentItem:		#		2 -	the Activities are listed in order of confidence: that's the entire reason
			currentLine[10]=currentItem.split(":")[1][1:-1] + ","					#			for storing each .csv line in an array, rather than printing each value
		elif column_titles[11] in previousItem and "confidence" in currentItem:		#			as its' line iteration occurs. This means that column_titles entries 6-14
			currentLine[11]=currentItem.split(":")[1][1:-1] + ","					#			can be rearranged as you see fit, as long as column 1-4 titles remain the 
		elif column_titles[12] in previousItem and "confidence" in currentItem:		#			same, and column 5 remains in the same place (although the string value
			currentLine[12]=currentItem.split(":")[1][1:-1] + ","					#			can technically be changed to anything)
		elif column_titles[13] in previousItem and "confidence" in currentItem:
			currentLine[13]=currentItem.split(":")[1][1:-1] + ","
	if "[ {" in currentItem:	#watch for array initialization character
		arrayLevel+=1			#and adjust the array level accordingly
		if DEBUG: print(arrayLevel)
	if "} ]" in currentItem:
		arrayLevel-=1			# ^^ likewise ^^
		if DEBUG: print(arrayLevel)
