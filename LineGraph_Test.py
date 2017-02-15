'''
Author:         John Coty Embry
  Date:         02-13-2017

Due: 17 FEB 17
Instructions:
• For this assignment you will be performing data analysis and
charting using the matplotlib library for Python.
• You will be processing Typical Meteorological Year 3 data
from the National Solar Radiation Database. This information
is available at the following website:
http://rredc.nrel.gov/solar/old_data/nsrdb/1991-2005/tmy3/
• There is data available for many sites around the US, your
Python program should be able to take any TMY3 file as input.
• On program start ask the user which TMY3 file they would like
to process from the current input directory.
• Give the user a selection among (at a minimum): dry bulb
temperature, humidity, and global horizontal irradiation.
• Ask the user if they would like to plot:
o scatter chart by hour of the day
o monthly minimum, maximum, and average
o discrete values for each hour of the year.
• You are free to choose the best charting type implementation
for each of the above, including chart type, colors, axes, etc.
'''

import os
import matplotlib.pyplot as plt1
import matplotlib.pyplot as plt2
import matplotlib.pyplot as plt3

def Program():

    print(os.listdir())	#to list the current files in the directory
    fileName = input('Which TMY3 file would you like to process: ')
    graphSelection=int(input('What would you like to graph? 1. temperature 2. humidity 3. glabal horizontal irridiation '))


	# o scatter chart by hour of the day
	# o monthly minimum, maximum, and average
	# o discrete values for each hour of the year.
    chartSelection=int(input('What type of graph would you like to see? 1. scatter chart by hour 2. monthly min, max, and average 3. discrete values for each hour of the year '))

    file = open(fileName,'r')
    fileString = file.read()		#convert the whole file into a string
    list1 = fileString.split('\n')    list2 = list1[2:8762]			#list split is from 2 (because the first two rows of data are headers and are not needed) to 8762 because two things: 1. the 8762 element in this list is the last blank line in the file 2. the split method splits downward one value


    list3=[]

    print(list1[8762])

#a typical standard is to have a main function to start the program from
def main():
    Program()

main()  #to start the program