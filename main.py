import time
import concurrent.futures
from googlesearch import search
import csv
from onlineOfflineDetection import *
import sys
import pandas as pd


def findLinks(query):
    try:
        with open('collegeName.csv', 'r') as collegeNames:
            next(collegeNames)
            links = {}
            total = len(pd.read_csv('collegeName.csv'))
            temp = 1
            for college in collegeNames:
                sys.stdout.write("\r")
                sys.stdout.write(f"Finding links : {temp}/{total}\r")
                college = college.rstrip()
                if not college:
                    continue
                Query = college + " " + query 
                link = list(search(Query, tld="co.in", num=1, stop=1, pause=2)) 
                links[college] = link
                temp += 1   
                sys.stdout.flush()  
            return links  
    except Exception as e:
        print(e)


def initializeGeneratedFile():
    try:
        with open('systemGenerated.csv', 'w') as generateFile:
            writer = csv.writer(generateFile)
            field = ["College","Internship Links","Check","Hackathon Links","Check","Events","Check"]
            writer.writerow(field)
    except Exception as e:
        print(e)         


def writeSystemGeneratedFile(college,internshipLink,status1,hackathonLink,status2,eventLink,status3):
    try:
        with open('systemGenerated.csv', 'a') as generateFile:
            writer = csv.writer(generateFile)          
            writer.writerow([college,internshipLink,status1,hackathonLink,status2,eventLink,status3])   
    except Exception as e:
        print(e) 
                          

def checkOnlineOffline(linkList):
    try:
        with open('collegeName.csv', 'r') as collegeNames:
            total = len(pd.read_csv('collegeName.csv'))
            temp = 1
            next(collegeNames)
            checked = {}
            for college in collegeNames:
                college = college.rstrip()
                if not college:
                    continue
                for i in linkList[college]:
                    tempChecked = determine(i)
                    sys.stdout.write("\r")
                    sys.stdout.write(f"Checking online or offline : {temp}/{total}\r")
                    checked[college] = tempChecked 
                    temp += 1    
                    sys.stdout.flush()         
            return checked         
    except Exception as e:
        print(e)


def main():
    try:    
        with concurrent.futures.ThreadPoolExecutor() as executer:

            findinternshipLinks = executer.submit(findLinks,"internship")
            findhackathonLinks = executer.submit(findLinks,"hackathon")
            findeventLinks = executer.submit(findLinks,"events")

            internshipLinks = findinternshipLinks.result()
            hackathonLinks = findhackathonLinks.result()
            eventLinks = findeventLinks.result()

            print("\nFound Links!")

            checkingIntern = executer.submit(checkOnlineOffline,internshipLinks)
            checkingHackathon = executer.submit(checkOnlineOffline,hackathonLinks)
            checkingEvent = executer.submit(checkOnlineOffline,eventLinks)

            checkedIntern = checkingIntern.result()
            checkedHackathon = checkingHackathon.result()
            checkedEvent = checkingEvent.result()

            print("\nChecked online/offline!")
        
        print("Creating CSV File....")  
        
        initializeGeneratedFile()

        with open('collegeName.csv', 'r') as collegeNames:
            next(collegeNames)  
            for college in collegeNames:
                college = college.rstrip()
                if not college:
                    continue
                writeSystemGeneratedFile(college,internshipLinks[college],checkedIntern[college],hackathonLinks[college],checkedHackathon[college],eventLinks[college],checkedEvent[college])
        
        print('File created with the name "systemGenerated.csv"') 

    except Exception as e:
        print(e)  


if __name__ == "__main__":

    start = time.time() 

    main()  

    finish = time.time()

    print(f"Time taken: {finish-start} sec.")  