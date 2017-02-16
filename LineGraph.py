'''
       Author:  John Coty Embry
         Date:  02-13-2017
Last Modified:  02-16-2017


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
import matplotlib.pyplot as mplLineGraph
import matplotlib.pyplot as mplBarGraph
import matplotlib.pyplot as mplDiscreteLine

#platform.system() == 'Windows' #this will help me to append a '/' or a '\' when making the absolute path for the file
import platform
from pathlib import Path


#CELLERRORVALUE is used throughout the code to make sure not to append and use in a calculation this -9999 data value since this means to the TMY3 files that data did not exist for that cell so this should be either 1. smoothed over 2. replaced with a 0 (which is what I chose to do)
CELLERRORVALUE = -9999

def drawBarGraph(figureText, avgMaxMinList, width=0.8, bottom=None, hold=None, data=None, alphaValue=0.5):
    '''
                                  avg     max     min
    avgMaxMinList takes the form [[0-11], [0-11], [0-11]] where 0-11 represents the indexes that exists for the three lists inside the outer

    matplotlib.pyplot.bar(left, height)
        left:   sequence of scalars
                the x coordinates of the left sides of the bars
        height: sequence of scalars
                the heights of the bars

    area is the radius of the point to show how big the dot is drawn on the screen
    alphaValue is the transparency/opacity (alpha) of the paint
    '''
    # time to get the monthly min, max, and average and then graph the values

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    xCoordinates1 = []          #the xCoordinates lists will be used specifically for each different bar graph
    xCoordinates2 = []
    xCoordinates3 = []
    xInc1 = 0                   #I start the Inc varialbes off on what their respective left x position should start off as
    xInc2 = 0.33
    xInc3 = 0.66
    barWidth = 0.33             #this bar width value works in conjunction with the xInc variables and the barSection variable
    barSection = barWidth * 3   #barSection will represent enough space for 3 bars

    #this for loop is what creates the x-axis spacing list data structures to use later when drawing the graph to specify the x position's left value that matplotlib's api expects
    for i in range(0, 12):        
        xCoordinates1.append(xInc1)
        xCoordinates2.append(xInc2)
        xCoordinates3.append(xInc3)
        xInc1 += barSection
        xInc2 += barSection
        xInc3 += barSection


    mplBarGraph.figure(figureText)  #set the title text that was passed in when the function was called


    #finally, draw the bar graphs
    mplBarGraph.bar(xCoordinates1, avgMaxMinList[1], barWidth, align='center', alpha=alphaValue,color='purple', label='Min') #max bars
    mplBarGraph.bar(xCoordinates2, avgMaxMinList[2], barWidth, align='center', alpha=alphaValue, color='green', label='Ave') #min bars
    mplBarGraph.bar(xCoordinates3, avgMaxMinList[0], barWidth, align='center', alpha=alphaValue, color='red', label='Max')   #avg bars

    #and lastly show the graph
    mplBarGraph.show()


def drawLineGraph(figureText, xValues, yValues, area=3, color='green', alphaValue=0.5):
    '''
    drawLineGraph lets me simplify the api call using matplotlib's methods and adds in some optional arguments that have default values
    area is the radius of the point to show how big the dot is drawn on the screen
    alphaValue is the transparency/opacity (alpha) of the paint
    '''
    mplLineGraph.figure(figureText)
    mplLineGraph.scatter(xValues, yValues, s=area, c=color, alpha=alphaValue)
    mplLineGraph.show()


def formatDataForMonthlyMinMaxAndAvg(yValues, monthList):   
    #I need to see what month I am currently looking at and also need to know what the prior month is
    #this will tell me when the months change.
    #another thing to think about is the first iteration

    #current and prior month will help me know when the month has changed while I'm iterating through these lists
    currentMonth = ''
    priorMonth = ''
    valueList = []                  #valueList will help me get the min of the month
    averageValueForMonthList = []
    maximumValueForMonthList = []
    minimumValueForMonthList = []

    #okay, so I messed up and acutally wrote the logic for the changing of the months in the wrong place, but im too tired to change it right now
    #I will take it out of this current location (below this text) and implement it later on after I have gotten the data for the humidity out just
    #like was done above for the temperature data

    # print(monthList)

    for i in range(0, 8760):
        humidityValueForCurrentCell = yValues[i]

        #to properly get a minimum for the month I need to know what month I'm looking at so I will do that now
        currentMonth = monthList[i] #this is the current month in the iteration
        
        # if i == 0:
        #     print('i = ', i, currentMonth)
        # if i == 8759:
        #     print('i = ', i, currentMonth)

        #I need to get the MONTHLY min
        if i == 0 or currentMonth == priorMonth:
            #if here I know this is the first iteration
            #OR
            #if here then this will allow me to continue to build the valueList so that I can eventually get the minimum value for the month (once the month changes)
            if i == 0: priorMonth = currentMonth    #this only needs to be done during the first iteration
            if humidityValueForCurrentCell == CELLERRORVALUE:
                valueList.append(0)     #I could add some logic here to smooth the data
            else:                
                valueList.append(humidityValueForCurrentCell)


            #also a thing to have to watch out for is if this is the last element in the list
            #if it is we are done here after adding the minimum value to the minimumValueForMonthList
            if i == 8759:
                #this is the last iteration in the loop
                #I will finish up by getting the last calculation for the final month's data before the loop ends
                averageValueForMonth = getAverageOfList(valueList)
                maximumValueForMonth = max(valueList)
                minimumValueForMonth = min(valueList)
                averageValueForMonthList.append(averageValueForMonth)
                maximumValueForMonthList.append(maximumValueForMonth)
                minimumValueForMonthList.append(minimumValueForMonth)
                valueList = []      #empty this value since it is no longer needed
        else:
            
            #if here then the month must have changed
            #I can now get the minimum value for the month
            averageValueForMonth = getAverageOfList(valueList)
            maximumValueForMonth = max(valueList)
            minimumValueForMonth = min(valueList)
            averageValueForMonthList.append(averageValueForMonth)
            maximumValueForMonthList.append(maximumValueForMonth)
            minimumValueForMonthList.append(minimumValueForMonth)
            valueList = []  #I will empty the list and start the process of getting the minimum value for the next month by adding the first value for the newest month in the iteration
            valueList.append(humidityValueForCurrentCell)

        priorMonth = currentMonth   #this will help me know later when the month has changed during the iteration over the list

    #now I will return my composed data to use later when graphing these values
    return [averageValueForMonthList, maximumValueForMonthList, minimumValueForMonthList] 

def getAverageOfList(rawListData):
    averageList = 0   #averageList will hold a scalar for the averaged data for the list

    averageList = sum(rawListData) / float(len(rawListData))

    return averageList

def getChartSelectionFromUser():
    '''
    scatter chart by hour of the day
    monthly minimum, maximum, and average
    discrete values for each hour of the year.
    '''
    chartSelection = None
    inputMessage = 'What type of graph would you like? 1. scatter chart by hour 2. monthly min, max, and average 3. discrete values for each hour of the year '
    # inputMessage = 'Which TMY3 file would you like to process: '
    while chartSelection is None:
        try:
            chartSelection = int(input(inputMessage))
            if chartSelection >= 1 and chartSelection <= 3:
                break   #if here then the user has entered a valid value
            else:
                print('Error: please enter a whole number that is between 1 and 3: ')
                chartSelection = None  
        except ValueError as error:
            print('Error: please enter a whole number for the type of graph that you want to draw: 1. scatter chart by hour 2. monthly min, max, and average 3. discrete values for each hour of the year ')

    return chartSelection

def getFileNameFromUser():
    '''
    getFileNameFromUser will get the file name from the user for the TMY3 .csv file to use to get data from to graph for the user and it includes error trapping to make sure this is a valid file.
    '''
    fileName = None
    while fileName is None:
        try:
            print(os.listdir()) #to list the current files in the directory
            inputMessage = 'Which TMY3 file would you like to process out of the above listed: '
            fileName = input(inputMessage)
            #I will write some logic to handle Windows path slashes or other slashes depeding on the OS being used
            filePath = ''
            if platform.system() == 'Windows':
                filePath = Path(str(os.getcwd()) + '\\' + fileName)    #this will construct an absolute path using the '\' character (I had to escape it so that its special meaning is not used)
            else:
                filePath = Path(str(os.getcwd()) + '\/' + fileName)    #this will construct an absolute path using the '/' character (I escaped this character just incase it has a special meaning)
            if filePath.is_file():
                # if here then the file exists so I will break out of the while loop
                break
            else:
                print('Error: that file does not exist in this directory... try again ^_^\n')
                fileName = None
        except ValueError as error:
            print('Error: that file does not exist in this directory... try again ^_^\n')
            print(os.listdir())
    return fileName

def getGraphSelectionFromUser():
    '''
    getGraphSelectionFromUser will ask and get, with error trapping code, the users selection for the type of data they want to graph
    '''
    #now I will get the graph selection for the type of data the user want to graph
    graphSelection = None
    inputMessage = 'What data would you like to graph? 1. temperature 2. humidity 3. global horizontal irridiation '
    while graphSelection is None:
        try:
            graphSelection = int(input(inputMessage))
            if graphSelection >= 1 and graphSelection <= 3:
                break   #if here then the user has entered a valid value
            else:
                print('Error: please enter a whole number that is between 1 and 3: ')
                graphSelection = None  
        except ValueError as error:
            print('Error: please enter a whole number for the data on the graph that you want to draw: 1. temperature 2. humidity 3. global horizontal irridiation ')
    return graphSelection

def Program():
    #first I will get the fileName from the user for the .csv file they want to graph. I add input error code to make sure the user is entering in a valid file name for a file that exists in the current working directory
    fileName = getFileNameFromUser()

    #next I need to get the graph selection from the user for the data they want graphed
    graphSelection = getGraphSelectionFromUser()

    #now I need to ask and get the type of graph the user wants to see
    chartSelection = getChartSelectionFromUser()

    file = open(fileName,'r')
    fileString = file.read()                        #convert the whole file into a string
    linesInFileList = fileString.split('\n')
    sanitizedLinesList = linesInFileList[2:8762]    #list split is from 2 (because the first two rows of data are headers and are not needed) to 8762 because two things: 1. the 8762 element in this list is the last blank line in the file 2. the split method splits downward one value
    cellList = []   #this will be used later to help get the individual data cells
    #now I will build the list (I keep wanting to say array lol) to hold the hour values that will be used when drawing the graph
    time = []
    monthList = []  #this will help me in the monthly min, max, and average section of the code

    for i in range(0, 8760):
        cellList.append(sanitizedLinesList[i].split(','))
        #this will grab the cell row, then with [1] grab the cell (which has the time value in it) then do a string slice [:2] which makes it where it just keeps the hour and discards the minutes
        time.append(str(cellList[i][1])[:2])
        monthList.append(cellList[i][0].split('/')[0])    #this grabs the month

    #cellList now contains for each element up to and including 8759 a list of the individual cells for that element index


    #now that the data is organized in a multidimensional list of lists, I can begin to format the data to what the scatter plot graph api is expecting
    #I can build a list of y values and that is what is needed for the y-axis so I will do that now

    yValues = []
    minimumValueForMonthList = []

    if graphSelection == 1:
        #for each cellList element (i.e. 0 - 8759 inclusive)
        for i in range(0, 8760):
            temperatureValueForCurrentCell = float(cellList[i][31])#index 31 is the temperature index (todo: check and make sure 31 is correct)
            if temperatureValueForCurrentCell == CELLERRORVALUE:
                yValues.append(0)
            else:
                yValues.append(temperatureValueForCurrentCell)

        # #now that I have the data to graph I will use the matplotlib api to draw a scatter chart on the screen
        # mplLineGraph.figure("Scatter Chart")

        # area = 3  #this is the radius of the point to show how big the dot is drawn on the screen
        # mplLineGraph.scatter(time, yValues, s=area, c='green', alpha=0.5)
        # mplLineGraph.show()


        # #time is being used as the xAxis labels
        # drawLineGraph('Scatter Chart', time, yValues)

    elif graphSelection == 2:
        for i in range(0, 8760):
            humidityValueForCurrentCell = float(cellList[i][37])
            if humidityValueForCurrentCell == CELLERRORVALUE:
                yValues.append(0)
            else:
                yValues.append(humidityValueForCurrentCell)
    elif graphSelection == 3:
        for i in range(0, 8760):
            globalHorizontalIrridiation = float(cellList[i][4])
            if globalHorizontalIrridiation == CELLERRORVALUE:
                yValues.append(0)
            else:
                yValues.append(globalHorizontalIrridiation)
    else:
        #my default case should never run because of the input error trapping that I have above, but I will keep this else statement here with code that will make the yValues default to all be 0's
        for i in range(0, 8760):
            yValues.append(0)


    composedDataList = []       #this will hold the returned list values from formatDataForMonthlyMinMaxAndAvg

    # chartSelection = None
    # inputMessage = 'What type of graph would you like? 1. scatter chart by hour 2. monthly min, max, and average 3. discrete values for each hour of the year'
    if chartSelection == 1:
        #for the scatter chart, no data manipulation is needed - the above format the yValues are in already works
        #time is being used as the xAxis labels
        drawLineGraph('Scatter Chart', time, yValues)

    elif chartSelection == 2:
        #graph monthly min, max, and average as a bar graph
        # yValues = formatDataForMonthlyMinMaxAndAvg(yValues, monthList)
        composedDataList = formatDataForMonthlyMinMaxAndAvg(yValues, monthList)
        # The data structure/format of composedDataList is of the form shown below
        #
        # averageValuesList = composedDataList[0]
        # maximumValuesList = composedDataList[1]
        # minimumValuesList = composedDataList[2]

        #now that I have the data to graph, its time to actually graph it
        drawBarGraph('Monthly Min, Max, and Average', composedDataList)

    elif chartSelection == 3:
        #todo
        blahblah = 0
    #because of the error trapping code, 1, 2, and 3 are the only values that chartSelection could be so I don't have to consider any other possible values to branch on

#a typical standard is to have a main function to start the program from
def main():

    Program()

main()  #to start the program
