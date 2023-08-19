from googlesearch import search
import csv

with open('SystemGenerated.csv', 'w') as generateFile:
    with open('collegeName.csv', 'r') as collegeNames:
        writer = csv.writer(generateFile)
        field = ["College", "Internship Links", "Hackathon Links", "Events"]
        writer.writerow(field)
        next(collegeNames)
        for college in collegeNames:

            internshipQuery = college + 'intership'
            hackathonQuery = college + 'hackathon'
            eventsQuery = college + 'events'

            internshipLink = list(search(internshipQuery, tld="co.in", num=1, stop=1, pause=3))
            hackathonLink = list(search(hackathonQuery, tld="co.in", num=1, stop=1, pause=3))
            eventLink = list(search(eventsQuery, tld="co.in", num=1, stop=1, pause=3))
            writer.writerow([college,internshipLink[0],hackathonLink[0],eventLink[0]])