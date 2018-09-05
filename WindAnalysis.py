import datetime as dt
import numpy as np
import math
import time
import xlwt
from os import path


class WindAnalysis():

    def __init__(self, inputFile, dateCol, timeCol, dirCol, speedCol):
        
        self.runAnalysis(inputFile, dateCol, timeCol, dirCol, speedCol)
        
        return
        
###################################################################
###################################################################

    def runAnalysis(self, inputFile, dateCol, timeCol, dirCol, speedCol):
        
        print("Running Analysis...")
        
        self.inputFile = inputFile
        self.inputFileArray = self.getFileArray(self.inputFile,",")
        
        ## Take out the first 2  unwanted rows
        self.trimmedInputFileArray = self.inputFileArray[2:]
        self.initialHeaderArray = []
        
        ## Indepedent arrays for times and values need to be created
        
        ## Create independent arrays for date and time
        self.dateTimeArray = []
        self.dateTimeArrayHeader = []
        self.dataGapStartdateTimeArray = []
        self.dataGapEnddateTimeArray = []
        
        ## Create independent arrays for values
        self.analysisArray = []
        self.valuesArray = []
        self.valuesArrayHeader = []
        
        ## Create an array to store the python datetime object
        self.dateObjectArray = []
        self.dateObjectHourlyArray = []
        self.dateObjectDailyArray = []
        
        ## Create arrays to store hourly and daily results
        self.U_10Min = []
        self.V_10Min = []
        self.Dir_10Min = []
        self.Speed_10Min = []
        self.hourlyAVGU = []
        self.hourlyAVGV = []
        self.hourlyAVGDir = []
        self.hourlyAVGSpeed = []
        self.dailyAVGU = []
        self.dailyAVGV = []
        self.dailyAVGDir = []
        self.dailyAVGSpeed = []
        
        ## Specify column header for direction and speed data
        self.dateCol = dateCol
        self.timeCol = timeCol
        self.dirCol = dirCol
        self.speedCol = speedCol
        
        self.dateColIndex = -9999
        self.timeColIndex = -9999
        self.dirColIndex = -9999
        self.speedColIndex = -9999

        ## Create boolean flag to pick up data gaps
        self.dataGap = False
        
        ## Loop through the trimmed array
        for i in range(0,len(self.trimmedInputFileArray)):
            
            lineArray =  self.trimmedInputFileArray[i]
            
            ## Create headers for the date-time and value arrays
            if i == 0:
                
                ## Trim possible quotation marks from the strings
                for m in range(0,len(self.trimmedInputFileArray[i])):
                    headerElement = self.trimmedInputFileArray[i][m].replace("\"","")
                    self.trimmedInputFileArray[i][m] = headerElement                    
                    self.initialHeaderArray.append(headerElement)
                    if headerElement == self.dateCol:
                        self.dateColIndex = m
                    if headerElement == self.timeCol:
                        self.timeColIndex = m
                    if headerElement == self.dirCol:
                        self.dirColIndex = m
                    if headerElement == self.speedCol:
                        self.speedColIndex = m
                
                self.dateTimeArrayHeader = [self.trimmedInputFileArray[i][0], 'Hour', 'Minute', 'Hourly Group Factor', 'Daily Group Factor']
                self.analysisArray.append(self.trimmedInputFileArray[i][self.dirColIndex].replace("\"",""))
                self.analysisArray.append(self.trimmedInputFileArray[i][self.speedColIndex].replace("\"",""))
                
                for z in range(0,len(self.analysisArray)):
                    self.valuesArrayHeader.append(self.analysisArray[z])
                self.valuesArrayHeader.append('xComp')    
                self.valuesArrayHeader.append('yComp')
                self.valuesArrayHeader.append('HourlyAVGxComp')
                self.valuesArrayHeader.append('HourlyAVGyComp')
                self.valuesArrayHeader.append('DailyAVGxComp')
                self.valuesArrayHeader.append('DailyAVGyComp')
                self.valuesArrayHeader.append('HourlyAVGDir')
                self.valuesArrayHeader.append('HourlyAVGSpeed')
                self.valuesArrayHeader.append('DailyAVGDir')
                self.valuesArrayHeader.append('DailyAVGSpeed')
                
            else:
                
                ## Store the data
                valuesLineArray = []
                valuesLineArray.append(self.trimmedInputFileArray[i][self.dirColIndex])
                valuesLineArray.append(self.trimmedInputFileArray[i][self.speedColIndex])
                valuesArray = []
                
                floatValue = -9999
                for j in range(0,len(valuesLineArray)):
                    if len(valuesLineArray[j]) > 0:
                        try:
                            floatValue = float(valuesLineArray[j])
                        except ValueError:
                            floatValue = float(valuesLineArray[j]+'.0')
                        valuesArray.append(floatValue)
                    else:
                        valuesArray.append('')
                        
                windDir10Min = valuesLineArray[0]
                windSpeed10Min = valuesLineArray[1]
                
                xComp, yComp = self.degreeToVector(windDir10Min, windSpeed10Min)
                    
                if math.isnan(xComp) or math.isnan(yComp):
                    valuesArray.append('')
                    valuesArray.append('')
                else:
                    valuesArray.append(xComp)
                    valuesArray.append(yComp)
                
                ## Store the dates and times into an array
                rowDate = lineArray[0].split('/')
                rowTime = lineArray[1].split(':')
                rowHour = rowTime[0]
                rowMinute = rowTime[1]
                
                # Create Group Factors for calculation of averages
                if rowMinute == '00':
                    lastHour = self.valuesArray[i-6:i]
                    lastHour.append(valuesArray)
                    
                    sumLastHourX = []
                    sumLastHourY = []

                    for a in range(0,len(lastHour)):
                        if isinstance(lastHour[a][2],np.float64) and isinstance(lastHour[a][3], np.float64):
                            sumLastHourX.append(lastHour[a][2])
                            sumLastHourY.append(lastHour[a][3])
                    if len(sumLastHourX) > 0 and len(sumLastHourY) > 0:
                        avgLastHourX = np.mean(sumLastHourX)
                        avgLastHourY = np.mean(sumLastHourY)
                    else:
                        avgLastHourX = ''
                        avgLastHourY = ''

                    valuesArray.append(avgLastHourX)
                    valuesArray.append(avgLastHourY)

                    if len(repr(int(rowHour)))==1:
                        rowHourGF = '0'+repr(int(rowHour)-1)
                    else:
                        rowHourGF = repr(int(rowHour)-1)
                else:
                    valuesArray.append('')
                    valuesArray.append('')
                    rowHourGF = rowHour
                rowHourlyGF = rowDate[2] + rowDate[1] + rowDate[0] + rowHourGF
                rowDailyGF = rowDate[2] + rowDate[1] + rowDate[0]
                
                dateTimeArray = [self.trimmedInputFileArray[i][0],rowHour,rowMinute,rowHourlyGF,rowDailyGF]
                self.dateTimeArray.append(dateTimeArray)

                # Calculate daily average
                if rowMinute == '00' and rowHour == '24':
                    
                    lastday = self.valuesArray[i-144:i]
                    lastday.append(valuesArray)

                    sumLastDayX = []
                    sumLastDayY = []
                    for b in range(0,len(lastday)):
                        if isinstance(lastday[b][4],np.float64) and isinstance(lastday[b][5],np.float64):
                            sumLastDayX.append(lastday[b][4])
                            sumLastDayY.append(lastday[b][5])

                    if len(sumLastDayX) > 0 and len(sumLastDayY) > 0:
                        avgLastDayX = np.mean(sumLastDayX)
                        avgLastDayY = np.mean(sumLastDayY)
                    else:
                        avgLastDayX = ''
                        avgLastDayY = ''
                    valuesArray.append(avgLastDayX)
                    valuesArray.append(avgLastDayY)
                    
                else:
                    valuesArray.append('')
                    valuesArray.append('')
                
                for k in range(0,len(lineArray)):

                    ## Swap out the '24:00' with '00:00'
                    if '24:00' in lineArray[1]:
                        self.trimmedInputFileArray[i][1] = self.trimmedInputFileArray[i][1].replace("24:00", "00:00")
                        
                        ## Then add one more day to the date part
                        dateObject = dt.datetime.strptime(self.trimmedInputFileArray[i][0],'%d/%m/%Y')
                        adjustedDateObject = dateObject + dt.timedelta(days=1)
                        adjustedDateString = adjustedDateObject.strftime('%d/%m/%Y')
                        self.trimmedInputFileArray[i][0] = adjustedDateString

                ## Store the adjusted times as python datetime objects
                dateTimeString = self.trimmedInputFileArray[i][0] + " " + self.trimmedInputFileArray[i][1]
                dateTimeObject = dt.datetime.strptime(dateTimeString,'%d/%m/%Y %H:%M')
                
                if i > 1:
                    ## Previous date objects for reporting dataGaps
                    prevDateTimeString = self.trimmedInputFileArray[i-1][0] + " " + self.trimmedInputFileArray[i-1][1]
                    prevDateTimeObject = dt.datetime.strptime(prevDateTimeString,'%d/%m/%Y %H:%M')

                # Append hourly and daily averages to result arrays
                if valuesArray[4] != '' and valuesArray[5] != '':
                    hourlyAVGDir, hourlyAVGSpeed = self.vectorToDegSpeed(valuesArray[4], valuesArray[5])
                    valuesArray.append(hourlyAVGDir)
                    valuesArray.append(hourlyAVGSpeed)
                    self.hourlyAVGDir.append(hourlyAVGDir)
                    self.hourlyAVGSpeed.append(hourlyAVGSpeed)
                    self.hourlyAVGU.append(avgLastHourX)
                    self.hourlyAVGV.append(avgLastHourY)
                    self.dateObjectHourlyArray.append(dateTimeObject - dt.timedelta(hours=1))
                else:
                    valuesArray.append('')
                    valuesArray.append('')

                if valuesArray[6] != '' and valuesArray[7] != '':
                    dailyAVGDir, dailyAVGSpeed = self.vectorToDegSpeed(valuesArray[6], valuesArray[7])
                    valuesArray.append(dailyAVGDir)
                    valuesArray.append(dailyAVGSpeed)
                    self.dailyAVGDir.append(dailyAVGDir)
                    self.dailyAVGSpeed.append(dailyAVGSpeed)
                    self.dailyAVGU.append(avgLastDayX)
                    self.dailyAVGV.append(avgLastDayY)
                    self.dateObjectDailyArray.append(dateTimeObject - dt.timedelta(days=1))
                else:
                    valuesArray.append('')
                    valuesArray.append('')
                      
                self.valuesArray.append(valuesArray)

                if isinstance(valuesArray[0],float) and isinstance(valuesArray[1],float):
                    self.dateObjectArray.append(dateTimeObject)
                    self.Dir_10Min.append(valuesArray[0])
                    self.Speed_10Min.append(valuesArray[1])
                    self.U_10Min.append(xComp)
                    self.V_10Min.append(yComp)
                    if (self.dataGap==True):
                        self.dataGapEnddateTimeArray.append(prevDateTimeObject)
                        self.dataGap=False
                elif(self.dataGap==True) and i == len(self.trimmedInputFileArray)-1:
                    self.dataGapEnddateTimeArray.append(dateTimeObject)
                elif(self.dataGap==False):
                    self.dataGapStartdateTimeArray.append(dateTimeObject)
                    self.dataGap = True
        
        return
    
###################################################################
###################################################################

    def writeDataToOutput(self, outputFileName, uvCompOption):
        
        ## Convert arrays to strings for CSV output                    
        self.CSVHeaderString = ''
        for i in range(0,len(self.dateTimeArrayHeader)):
            if i == 3 or i ==4:
                continue
            elif i == 0:
                self.CSVHeaderString = self.dateTimeArrayHeader[i] + ","
            elif i < len(self.dateTimeArrayHeader)-1:
                self.CSVHeaderString = self.CSVHeaderString + self.dateTimeArrayHeader[i] + ","
            else:
                self.CSVHeaderString = self.CSVHeaderString + self.dateTimeArrayHeader[i]
                
        for i in range(0,len(self.valuesArrayHeader)):
            if i < len(self.valuesArrayHeader)-1:
                if uvCompOption:
                    self.CSVHeaderString = self.CSVHeaderString + self.valuesArrayHeader[i] + ","
                else:
                    if i < 2 or i > 7:
                        self.CSVHeaderString = self.CSVHeaderString + self.valuesArrayHeader[i] + ","
            else:
                self.CSVHeaderString = self.CSVHeaderString + self.valuesArrayHeader[i]
        
        self.CSVStringArray = []
        for i in range(0,len(self.valuesArray)):
            lineString = ''
            lineArray = self.valuesArray[i]
            dateTimeArrayLine = self.dateTimeArray[i]
            for k in range(0,3):
                lineString = lineString + dateTimeArrayLine[k] + ","
                
            for j in range(0,len(lineArray)):
                if j < len(lineArray)-1:
                    if uvCompOption:
                        lineString = lineString + repr(lineArray[j]) + ","
                    else:
                        if j < 2 or j > 7:
                            lineString = lineString + repr(lineArray[j]) + ","
                else:
                    lineString = lineString + repr(lineArray[j])
                    
            self.CSVStringArray.append(lineString)
            
        if '.xls' in outputFileName:
            return self.writeToXLS(self.CSVStringArray, outputFileName, self.CSVHeaderString)
        else:
            return self.writeToCSV(self.CSVStringArray, outputFileName, self.CSVHeaderString)
    
###################################################################
###################################################################

    def writeToCSV(self, inputArray, fileName, header = ''):

        print("Writing to " + fileName + " ...")

        # Open File
        resultFile = open(fileName,'w')

        # Write header
        if len(header)>0:
            resultFile.write(header + "\n")

        # Write data to file
        for r in inputArray:
            resultFile.write(r + "\n")
        resultFile.close()

        return True
###################################################################
###################################################################

    def writeToXLS(self, inputArray, fileName, header = ''):

        print("Writing to " + fileName + " ...")

        workbook = xlwt.Workbook()
        head, tail = path.split(self.inputFile)
        inputFileName = tail.split('.')
        worksheet = workbook.add_sheet(inputFileName[0])
        headerArray = header.split(",")

        for col, cell in enumerate(headerArray):
            #print cell
            worksheet.write(0,col,label=cell)
        
        for row, line in enumerate(inputArray):
            lineArray = line.split(",")
            for col, cell in enumerate(lineArray):
                worksheet.write(row+1,col,label=cell)

        workbook.save(fileName)

        return True
###################################################################
###################################################################

    def getDataGapArrays(self):
        
        return self.dataGapStartdateTimeArray, self.dataGapEnddateTimeArray
    
###################################################################
###################################################################

    def getHeaderArray(self):
        
        return self.initialHeaderArray
        
###################################################################
###################################################################

    def get10MinValues(self):
        
        return self.dateObjectArray, self.Dir_10Min, self.Speed_10Min, self.U_10Min, self.V_10Min
        
###################################################################
###################################################################

    def getHourlyAVG(self):
        
        return self.dateObjectHourlyArray, self.hourlyAVGDir, self.hourlyAVGSpeed, self.hourlyAVGU, self.hourlyAVGV

###################################################################
###################################################################

    def getDailyAVG(self):
        
        return self.dateObjectDailyArray, self.dailyAVGDir, self.dailyAVGSpeed, self.dailyAVGU, self.dailyAVGV
    
###################################################################
###################################################################

    def vectorToDegSpeed(self, x, y):
        
        deg = ''
        speed = ''
        
        if x != '' and y != '':
            if x > 0 and y > 0:
                deg = 90.0 - math.atan(y/x)*180.0/math.pi
                speed = math.pow(math.pow(x,2) + math.pow(y,2), 0.5)
            if x > 0 and y < 0:
                deg = math.atan(-y/x)*180.0/math.pi + 90.0
                speed = math.pow(math.pow(x,2) + math.pow(y,2), 0.5)
            if x < 0 and y < 0:
                deg = 270.0 - math.atan(y/x)*180.0/math.pi
                speed = math.pow(math.pow(x,2) + math.pow(y,2), 0.5)
            if x < 0 and y > 0:
                deg = math.atan(-y/x)*180.0/math.pi + 270.0
                speed = math.pow(math.pow(x,2) + math.pow(y,2), 0.5)
        
        return deg, speed
            
###################################################################
###################################################################

    def degreeToVector(self, directionStr, speedStr):
        
        if len(directionStr) < 1 and len(speedStr) < 1:
            return np.NaN, np.NaN
        
        direction = float(directionStr+".0")
        try:
            speed = float(speedStr)
        except ValueError:
            speed = float(speedStr+".0")
            
        if (direction == 0.0 or direction == 360.0):
            return speed*0.0, speed*1.0
        
        elif (direction == 90.0):
            return speed*1.0, speed*0.0
        
        elif (direction == 180.0):
            return speed*0.0, speed*-1.0
        
        elif (direction == 270.0):
            return speed*-1.0, speed*0.0
        
        elif (direction > 0.0 and direction < 90.0):
            return speed*np.cos((90.0-direction)*np.pi/180), speed*np.sin((90.0-direction)*np.pi/180)
        
        elif (direction > 90.0 and direction < 180.0):
            return speed*np.cos((direction-90.0)*np.pi/180), speed*-1*np.sin((direction-90.0)*np.pi/180)
        
        elif (direction > 180.0 and direction < 270.0):
            return speed*-1*np.cos((270.0-direction)*np.pi/180), speed*-1*np.sin((270.0-direction)*np.pi/180)
        
        elif (direction > 270.0 and direction < 360.0):
            return speed*-1*np.cos((direction-270.0)*np.pi/180), speed*np.sin((direction-270.0)*np.pi/180)
        
        else:
            return np.NaN, np.NaN

###################################################################
###################################################################
    
    def getFileArray(self, inputFile, delimiter):
    # Converts contents of input file in formats similar to CSVs into a string array

        # Open input file
        processFile = open(inputFile, 'r')

        # Read all the lines in the file
        lines = processFile.readlines()

        # Initialize output array
        contentArray = []

        # Loop through the lines
        for i in range(0,len(lines)):

            # Strip the regex line dividers from each single line
            line = repr(lines[i].rstrip('\r\n'))

            # Split the single line with the input delimited into an array
            arrayLine = line.split(delimiter)

            # Loop though each value of the line array and remove unnecessary strings
            for i in range(0,len(arrayLine)):
                arrayLine[i] = arrayLine[i].replace("'", "")
                arrayLine[i] = arrayLine[i].replace("[", "")
                arrayLine[i] = arrayLine[i].replace("]", "")

            # Append to output array
            contentArray.append(arrayLine)

        processFile.close()

        return contentArray
    
if __name__ == "__main__":
    
    startTime = time.time()
    '''
    input = '/media/jasontam/Data/WindAnalysis/xCSV_File_1502403685.csv'
    dateColumn = "Date"
    timeColumn = "Time"
    dirColumn = r'AC Pakuranga WDR_RAW 10min average \xb0'
    speedColumn = "AC Pakuranga WSP_RAW 10min average m/s"
    '''
    WindAnalysis(input, dateColumn, timeColumn, dirColumn, speedColumn)
    
    endTime = time.time()
    
    print("Time elapsed: " + repr(endTime-startTime))