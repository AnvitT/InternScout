import time
import concurrent.futures
from googlesearch import search
import csv

def findLinks(query):
    try:
        with open('collegeName.csv', 'r') as collegeNames:
            next(collegeNames)
            links = {}
            for college in collegeNames:
                college = college.rstrip()
                if not college:
                    continue
                Query = college + " " + query 
                link = list(search(Query, tld="co.in", num=1, stop=1, pause=2)) 
                links[college] = link
            return links 
    except Exception as e:
        print(e)


def initializeGeneratedFile():
    try:
        with open('systemGenerated.csv', 'w') as generateFile:
            writer = csv.writer(generateFile)
            field = ["College", "Internship Links", "Hackathon Links", "Events"]
            writer.writerow(field)
    except Exception as e:
        print(e)         


def writeSystemGeneratedFile(college,internshipLink,hackathonLink,eventLink):
    try:
        with open('systemGenerated.csv', 'a') as generateFile:
            writer = csv.writer(generateFile)          
            writer.writerow([college,internshipLink,hackathonLink,eventLink])   
    except Exception as e:
        print(e)                    

def main():
    try:
            
        print("Finding Links...")
        
        with concurrent.futures.ThreadPoolExecutor() as executer:
            findinternshipLinks = executer.submit(findLinks,"internship")
            findhackathonLinks = executer.submit(findLinks,"hackathon")
            findeventLinks = executer.submit(findLinks,"events")

            internshipLinks = findinternshipLinks.result()
            hackathonLinks = findhackathonLinks.result()
            eventLinks = findeventLinks.result()

        print("Creating CSV File....")  
        
        initializeGeneratedFile()

        with open('collegeName.csv', 'r') as collegeNames:
            next(collegeNames)  
            for college in collegeNames:
                college = college.rstrip()
                if not college:
                    continue
                writeSystemGeneratedFile(college,internshipLinks[college],hackathonLinks[college],eventLinks[college])
        print('File created with the name "systemGenerated.csv"')
        
    except Exception as e:
        print(e)    


if __name__ == "__main__":
 
    start = time.time()     
    main()   
    finish = time.time()
    print(f"Time taken: {finish-start} sec.")  
