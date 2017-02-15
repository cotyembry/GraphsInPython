'''
       Author:  John Coty Embry
         Date:  02-13-2017
Last Modified:  02-14-2017


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
import matplotlib.pyplot as mtlBarGraph
import matplotlib.pyplot as mplDiscreteLine

#platform.system() == 'Windows' #this will help me to append a '/' or a '\' when making the absolute path for the file
import platform
from pathlib import Path


#CELLERRORVALUE is used throughout the code to make sure not to append and use in a calculation this -9999 data value since this means to the TMY3 files that data did not exist for that cell so this should be either 1. smoothed over 2. replaced with a 0 (which is what I chose to do)
CELLERRORVALUE = -9999

def drawBarGraph(left, height, width=0.8, bottom=None, hold=None, data=None):
    '''
    matplotlib.pyplot.bar()
    left:   sequence of scalars
            the x coordinates of the left sides of the bars
    height: sequence of scalars
            the heights of the bars
    area is the radius of the point to show how big the dot is drawn on the screen
    alphaValue is the transparency/opacity (alpha) of the paint
    '''
    # monthly min, max, and average





    mplLineGraph.figure(figureText)
    mplLineGraph.scatter(xValues, yValues, s=area, c=color, alpha=alphaValue)
    mplLineGraph.show()


def drawLineGraph(figureText, xValues, yValues, area=3, color='green', alphaValue=0.5):
    '''
    drawLineGraph lets me simplify the api call using matplotlib's methods and adds in some optional arguments that have default values
    area is the radius of the point to show how big the dot is drawn on the screen
    alphaValue is the transparency/opacity (alpha) of the paint
    '''
    mplLineGraph.figure(figureText)
    mplLineGraph.scatter(xValues, yValues, s=area, c=color, alpha=alphaValue)
    mplLineGraph.show()

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

    for i in range(0, 8760):
        cellList.append(sanitizedLinesList[i].split(','))
        #this will grab the cell row, then with [1] grab the cell (which has the time value in it) then do a string slice [:2] which makes it where it just keeps the hour and discards the minutes
        time.append(str(cellList[i][1])[:2])

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


        #time is being used as the xAxis labels
        drawLineGraph('Scatter Chart', time, yValues)

    elif graphSelection == 2:
        #I need to see what month I am currently looking at and also need to know what the prior month is
        #this will tell me when the months change.
        #another thing to think about is the first iteration
        
        #current and prior month will help me know when the month has changed while I'm iterating through these lists
        currentMonth = ''
        priorMonth = ''
        valueList = []  #valueList will help me get the min of the month
        for i in range(0, 8760):


            humidityValueForCurrentCell = float(cellList[i][37])
            # yValues.append(humidityValueForCurrentCell)






            #TODO: fix/restructure code
            
            #okay, so I messed up and acutally wrote the logic for the changing of the months in the wrong place, but im too tired to change it right now
            #I will take it out of this current location (below this text) and implement it later on after I have gotten the data for the humidity out just
            #like was done above for the temperature data




            #to properly get a minimum for the month I need to know what month I'm looking at so I will do that now
            currentMonth = cellList[i][0].split('/')[0] #this references the first row, first cell and grabs the month with the .split method
            

            #I need to get the MONTHLY min
            if i == 0 or currentMonth == priorMonth:
                #if here I know this is the first iteration
                #OR
                #if here then this will allow me to continue to build the valueList so that I can eventually get the minimum value for the month (once the month changes)
                if i == 0: priorMonth = currentMonth    #this only needs to be done during the first iteration
                if humidityValueForCurrentCell == CELLERRORVALUE:
                    yValues.append(0)
                else:                
                    valueList.append(humidityValueForCurrentCell)

            else:
                #if here then the month must have changed
                #I can now get the minimum value for the month
                minimumValueForMonth = min(valueList)
                minimumValueForMonthList.append(minimumValueForMonth)
                valueList = []  #I will empty the list and start the process of getting the minimum value for the next month by adding the first value for the newest month in the iteration
                valueList.append(humidityValueForCurrentCell)

            #I need to get the MONTHLY max
            

            #get MONTHLY average
            #so for each month 
                #get all of the data and average it out
                #make sure to watch out for -9999 values (since this is indicates that the value is missing)

            priorMonth = currentMonth   #this will help me know later when the month has changed during the iteration over the list




        print(minimumValueForMonthList)





            # drawLineGraph('Scatter Chart', time, yValues)
    elif graphSelection == 3:
        for i in range(0, 8760):
            globalHorizontalIrridiation = float(cellList[i][4])
            yValues.append(globalHorizontalIrridiation)

            drawLineGraph('Scatter Chart', time, yValues)
    else:
        #error (todo - make sure to write the error trapping code above when getting the input from the user)
        for i in range(0, 8760):
            yValues.append(0)

            drawLineGraph('Scatter Chart', time, yValues)




    '''



    date = []
    time = []
    GHI = []
    temperature = []
    humidity = []

    for h in range(0, 8760):

        date.append(str(list3[h][0]))
        time.append(str(list3[h][1]))

    month = []
    hour = []

    for h in range(0, 8760):
        month.append(int(str(date[h])[:2]))
        hour.append(int(str(time[h])[:2]))

    #SCATTER CHART
    if chartoption == 1:
        mplLineGraph.figure("Scatter Chart")
        x = hour

        if plotoption == 1:
            y = temperature
        elif plotoption ==2:
            y = humidity
        elif plotoption == 3:
            y = GHI

        area = 3  #point radius
        mplLineGraph.scatter(x, y, s=area, c='green', alpha=0.5)
        mplLineGraph.show()


    #DISCRETE VALUES
    if chartoption==2:
        mtlBarGraph.figure("Discrete Values")
        x = range(0,8760)

        if plotoption == 1:
            y = temperature
        elif plotoption ==2:
            y = humidity
        elif plotoption == 3:
            y = GHI

        area = 6  #point radius
        mtlBarGraph.scatter(x, y,  s = area,  c = 'red', alpha = 0.5)
        mtlBarGraph.plot(x, y)
        mtlBarGraph.show()


    #BAR MIN/AVE/MAX
    if chartoption == 3:

        monthlymin = []
        monthlymax = []
        monthlyave = []
        monthcount = 1
        monthitems = 0

        minvalue = 10**10
        maxvalue = -10**10
        sumvalue = 0

        for h in range(0, 8760):

            if plotoption == 1:
                if temperature[h] < minvalue:
                    minvalue = temperature[h]
                if temperature[h] > maxvalue:
                    maxvalue = temperature[h]
                sumvalue += temperature[h]
            elif plotoption == 2:
                if humidity[h] < minvalue:
                    minvalue = humidity[h]
                if humidity[h] > maxvalue:
                    maxvalue = humidity[h]
                sumvalue += humidity[h]
            elif plotoption == 3:
                if GHI[h] < minvalue:
                    minvalue = GHI[h]
                if GHI[h] > maxvalue:
                    maxvalue = GHI[h]
                sumvalue += GHI[h]

            monthitems += 1

            if h == 8759:

                monthlymin.append(minvalue)
                monthlymax.append(maxvalue)
                monthlyave.append(sumvalue / monthitems)
                monthcount += 1
                monthitems = 0

                minvalue = 10**10
                maxvalue = -10**10
                sumvalue = 0

            elif h < 8759:

                if monthcount != month[h + 1]:
                    monthlymin.append(minvalue)
                    monthlymax.append(maxvalue)
                    monthlyave.append(sumvalue / monthitems)
                    monthcount += 1
                    monthitems = 0

                    minvalue = 10**10
                    maxvalue = -10**10
                    sumvalue = 0


        mplDiscreteLine.figure("Min/Ave/Max Values")
        n_groups = 12
        index = np.arange(n_groups)
        bar_width = 0.35
        opacity = 1

        for m in range(0, 12):

            rects1 = mplDiscreteLine.bar(m, monthlymin[m], bar_width, alpha=opacity,color='blue', label='Min')
            rects2 = mplDiscreteLine.bar(m + bar_width, monthlyave[m], bar_width, alpha=opacity, color='green', label='Ave')
            rects3 = mplDiscreteLine.bar(m + bar_width + bar_width, monthlymax[m], bar_width, alpha=opacity, color='red', label='Max')

        mplDiscreteLine.xlabel('Month')
        if plotoption == 1:
            mplDiscreteLine.ylabel('Temp')
        elif plotoption == 2:
            mplDiscreteLine.ylabel('Humidity')
        elif plotoption == 3:
            mplDiscreteLine.ylabel('GHI')

        mplDiscreteLine.title('Monthly Min/Ave/Max')
        mplDiscreteLine.xticks(index + bar_width  / 2, ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
        mplDiscreteLine.show()

    '''

#a typical standard is to have a main function to start the program from
def main():

    Program()

main()  #to start the program
