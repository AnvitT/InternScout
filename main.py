from googlesearch import search
import csv

with open('SystemGenerated.csv', 'w') as generateFile:
    with open('collegeName.csv', 'r') as collegeNames:
        writer = csv.writer(generateFile)
        field = ["College", "Link"]
        writer.writerow(field)
        next(collegeNames)
        for i in collegeNames:
            query = i + 'intership'
            for j in search(query, tld="co.in", num=1, stop=10, pause=2):
                writer.writerow([i,j])
                break 