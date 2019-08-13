#############################################################################################################################
# Author: Naveen
# This script does the following:
# 1. Asks user to enter execution time in minutes and threshold values.
# 2. Then it copies the file at LOG_FILE_PATH and then parses it for different regular expressions
# 3. If any value is found to breach the defined threshold then it sends an alert email.
#############################################################################################################################
# To be implemented:
# 1. Refine code and add proper comments.
# 2. Throw error if user  inputs are invalid.
# 3. Capture logs via dclogs.sh and include the filename in the alert email or attach the logs to email.
#############################################################################################################################
import os
import re
import time
import  datetime

#LOG_FILE_PATH = '/usr/local/deviceconnect/Logs/MobileLabs.DeviceConnect.WatchDog.log'
LOG_FILE_PATH = '/Users/administrator/Desktop/Jira/NewFolder/Logs/MobileLabs.DeviceConnect.WatchDog.log'

#All regular expressions
strRegExCpuServices = r'(.*?)(localservices: Cpu usage)(.*)'
strRegExCpuWeb = r'(.*?)(localweb: Cpu usage)(.*)'
strRegExCpuWebViewer = r'(.*?)(localwebviewer: Cpu usage)(.*)'
strRegExMemServices = r'(.*?)(localservices: ResidentSize)(.*)'
strRegExMemWeb = r'(.*?)(localweb: ResidentSize)(.*)'
strRegExMemWebViewer = r'(.*?)(localwebviewer: ResidentSize)(.*)'
strRegExLsofServices = r'(.*?)(localservices: Lsof count)(.*)'
strRegExLsofWeb = r'(.*?)(localweb: Lsof count)(.*)'
strRegExLsofWebViewer = r'(.*?)(localwebviewer: Lsof count)(.*)'

def main():
    #Ask user for how many minutes the script should be run and waht max values are allowed
    mins = int(raw_input("Enter the minutes for which the WatchDog.log would be monitored: "))
    intMaxCpu = int(raw_input("Enter the max allowed CPU value for dc-services, valid range is 1-100: "))
    intMaxCpuWeb = int(raw_input("Enter the max allowed CPU value for dc-web, valid range is 1-100: "))
    intMaxCpuWebViewer = int(raw_input("Enter the max allowed CPU value for dc-webviewer, valid range is 1-100: "))
    intMaxMem = int(raw_input("Enter the max allowed Memory value for dc-services, valid range is 100-5000 (MB): "))
    intMaxMemWeb = int(raw_input("Enter the max allowed Memory value for dc-web, valid range is 100-5000 (MB): "))
    intMaxMemWebViewer = int(raw_input("Enter the max allowed Memory value for dc-webviewer, valid range is 100-5000 (MB): "))
    intMaxLsof = int(raw_input("Enter the max allowed lsof value, valid range is 100-2000: "))

    i=1
    startTime = datetime.datetime.now().replace(microsecond=0)
    #print startTime
    strAlertMessage = ''
    blnSendEmail = False
    blnFirstEmail = True

    while (i <= mins):

        #Get latest WatchDog.log every 30 seconds
        #tailLog = 'tail -F /usr/local/deviceconnect/Logs/MobileLabs.DeviceConnect.WatchDog.log > ./Test.log'
        tailLog = 'tail -n 25 ' + LOG_FILE_PATH + ' > ./Test.log'
        testLogPath = os.getcwd() + '/Test.log'

        os.system(tailLog)

        #Send an alert if an anomaly is found in WatchDog.log

        #CPU Usage - Services
        strCpuLine = str(parseAndGetLine(strRegExCpuServices, testLogPath)).strip()
        #print strCpuLine
        strCpuValue = strCpuLine.split('Cpu usage')[1].strip()
        #print strCpuValue
        intCpuValue =  int(round(float(strCpuValue)))
        #print intCpuValue

        #CPU Usage - Web
        strCpuLineWeb = str(parseAndGetLine(strRegExCpuWeb, testLogPath)).strip()
        #print strCpuLineWeb
        strCpuValueWeb = strCpuLineWeb.split('Cpu usage')[1].strip()
        #print strCpuValueWeb
        intCpuValueWeb =  int(round(float(strCpuValueWeb)))
        #print intCpuValueWeb

        #CPU Usage - WebViewer
        strCpuLineWebViewer = str(parseAndGetLine(strRegExCpuWebViewer, testLogPath)).strip()
        #print strCpuLineWebViewer
        strCpuValueWebViewer = strCpuLineWebViewer.split('Cpu usage')[1].strip()
        #print strCpuValueWebViewer
        intCpuValueWebViewer =  int(round(float(strCpuValueWebViewer)))
        #print intCpuValueWebViewer

        #Memory Usage - Services
        strMemLine = str(parseAndGetLine(strRegExMemServices, testLogPath)).strip()
        strMemLine = strMemLine.split('ResidentSize ')[1].strip()
        #print strMemLine
        strMemValue = strMemLine.split(' ')[0].strip()
        #print strMemValue
        intMemValue =  int(round((float(strMemValue))/1000000))
        #print intMemValue

        #Memory Usage - Web
        strMemLineWeb = str(parseAndGetLine(strRegExMemWeb, testLogPath)).strip()
        strMemLineWeb = strMemLineWeb.split('ResidentSize ')[1].strip()
        #print strMemLineWeb
        strMemValueWeb = strMemLineWeb.split(' ')[0].strip()
        #print strMemValueWeb
        intMemValueWeb =  int(round((float(strMemValueWeb))/1000000))
        #print intMemValueWeb

        #Memory Usage - WebViewer
        strMemLineWebViewer = str(parseAndGetLine(strRegExMemWebViewer, testLogPath)).strip()
        strMemLineWebViewer = strMemLineWebViewer.split('ResidentSize ')[1].strip()
        #print strMemLineWebViewer
        strMemValueWebViewer = strMemLineWebViewer.split(' ')[0].strip()
        #print strMemValueWebViewer
        intMemValueWebViewer =  int(round((float(strMemValueWebViewer))/1000000))
        #print intMemValueWebViewer

        #lsof count services
        strServicesLsofLine = str(parseAndGetLine(strRegExLsofServices, testLogPath)).strip()
        #print strServicesLsofLine
        strServicesLsofValue = strServicesLsofLine.split('Lsof count')[1].strip()
        #print strServicesLsofValue
        intServicesLsofValue =  int(strServicesLsofValue)
        #print intServicesLsofValue

        #lsof count web
        strWebLsofLine = str(parseAndGetLine(strRegExLsofWeb, testLogPath)).strip()
        #print strWebLsofLine
        strWebLsofValue = strWebLsofLine.split('Lsof count')[1].strip()
        #print strWebLsofValue
        intWebLsofValue =  int(strWebLsofValue)
        #print intWebLsofValue

        #lsof count webviewer
        strWebviewerLsofLine = str(parseAndGetLine(strRegExLsofWebViewer, testLogPath)).strip()
        #print strWebviewerLsofLine
        strWebviewerLsofValue = strWebviewerLsofLine.split('Lsof count')[1].strip()
        #print strWebviewerLsofValue
        intWebviewerLsofValue =  int(strWebviewerLsofValue)
        #print intWebviewerLsofValue

        #Total lsof
        intTotalLsof = int(intServicesLsofValue + intWebLsofValue + intWebviewerLsofValue)
        #print intTotalLsof

        #Create alert message
        if intCpuValue > intMaxCpu:
            if blnSendEmail == False:
                strPrefix =  ''
            else:
                strPrefix = '\n\n'
            strAlertMessage = strPrefix + 'dc-services: CPU usage is over: ' + str(intMaxCpu) + '\nWatchDog.log line: ' + strCpuLine
            blnSendEmail = True

        if intCpuValueWeb > intMaxCpuWeb:
            if blnSendEmail == False:
                strPrefix =  ''
            else:
                strPrefix = '\n\n'
            strAlertMessage = strAlertMessage + strPrefix + 'dc-web: CPU usage is over: ' + str(intMaxCpuWeb) + '\nWatchDog.log line: ' + strCpuLineWeb
            blnSendEmail = True

        if intCpuValueWebViewer > intMaxCpuWebViewer:
            if blnSendEmail == False:
                strPrefix =  ''
            else:
                strPrefix = '\n\n'
            strAlertMessage = strAlertMessage + strPrefix + 'dc-webviewer: CPU usage is over: ' + str(intMaxCpuWebViewer) + '\nWatchDog.log line: ' \
            + strCpuLineWebViewer
            blnSendEmail = True

        if intMemValue > intMaxMem:
            if blnSendEmail == False:
                strPrefix =  ''
            else:
                strPrefix = '\n\n'
            strAlertMessage = strAlertMessage + strPrefix + 'dc-services: Memory usage is over: ' + str(intMaxMem) + '\nWatchDog.log line: ' + strMemLine
            blnSendEmail = True

        if intMemValueWeb > intMaxMemWeb :
            if blnSendEmail == False:
                strPrefix =  ''
            else:
                strPrefix = '\n\n'
            strAlertMessage = strAlertMessage + strPrefix + 'dc-web: Memory usage is over: ' + str(intMaxMemWeb) + '\nWatchDog.log line: ' + strMemLineWeb
            blnSendEmail = True

        if intMemValueWebViewer > intMaxMemWebViewer :
            if blnSendEmail == False:
                strPrefix =  ''
            else:
                strPrefix = '\n\n'
            strAlertMessage = strAlertMessage + strPrefix + 'dc-webviewer: Memory usage is over: ' + str(intMaxMemWebViewer) + '\nWatchDog.log line: ' \
            + strMemLineWebViewer
            blnSendEmail = True

        if intTotalLsof > intMaxLsof:
            strLogLines = strServicesLsofLine + '\n' + strWebLsofLine + '\n' + strWebviewerLsofLine
            strAlertMessage = strAlertMessage + '\n' + '\nlsof is over: ' + str(intMaxLsof) + '\nWatchDog.log lines:\n' + strLogLines
            blnSendEmail = True

        #Send email if threshold was breached and no email was sent in the past 15 minutes
        if blnSendEmail:
            if blnFirstEmail:
                #print 'Send 1st email'
                sendEmail(strAlertMessage)
                blnFirstEmail = False
                startTime = datetime.datetime.now().replace(microsecond=0)

            endTime = datetime.datetime.now().replace(microsecond=0)
            #print endTime
            timeDiff = str(endTime - startTime)
            #print timeDiff
            timeMinutes = int(timeDiff.split(':')[1].strip())
            #print timeMinutes

            if timeMinutes > 15:
                #print 'Send 2nd email'
                sendEmail(strAlertMessage)
                blnSendEmail = False
                startTime = datetime.datetime.now().replace(microsecond=0)

        #print  strAlertMessage

        if (i == mins):
            break
        time.sleep(55)
        i = i+1

#Parse /usr/local/deviceconnect/Logs/MobileLabs.DeviceConnect.WatchDog.log for the passed in regex and return the complete log line
def parseAndGetLine(strRegEx, strLogFilePath):
    read_line = True

    with open(strLogFilePath, "r") as file:
        match_list = []
        if read_line == True:
            for line in file:
                for match in re.finditer(strRegEx, line, re.S):
                    match_text = match.group()
                    match_list.append(match_text)
                    return match_text
        else:
            data = f.read()
            for match in re.finditer(strRegEx, data, re.S):
                match_text = match.group()
                match_list.append(match_text)
                return match_text
    file.close()

#Send Email
def sendEmail(strMessage):
    #print strMessage
    strMessage = "\"" + strMessage + "\""
    #print strMessage
    os.system("python " + os.getcwd() + "/SendEmailAlert.py " + str(strMessage).strip())

#Call main()
main()
