from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def getText(url):
    try:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        return " ".join(soup.get_text().lower().split())
    except:
        try:
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context 
            page = urlopen(url)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            return " ".join(soup.get_text().lower().split())
        except:
            return ""


def detector(text):

    onlinePointCounter = 0
    offlinePointCounter = 1
    textList = text.split()
    relevantOnlineWords = []
    relevantOfflineWords = []

    sureConclusionsOnline = ["held","virtual","online","digital","web based","live-stream","video conference","webinar","remote","zoom","held","virtual.","online.","digital.","web based.","live-stream.","video conference.","webinar.","remote.","zoom.","off-campus","off-campus."]
    
    for i in textList:
        check = [elem in i for elem in sureConclusionsOnline]
        if True in check:
            relevantOnlineWords.append(i)
        if check.count(True) >= 1:
            onlinePointCounter += 1  

    sureConclusionsOffline = ["held","offline","physical","face-to-face","on-campus","on-premises","offline.","physical.","face-to-face.","in-person","in-person.","on-campus.","on-premises."]
    littleLessSure = ["accommodation","accommodation.","travel","travel.","hostel","hostel.","hostels","hostels."]

    for i in textList:
        check = [elem in i for elem in sureConclusionsOffline]
        lessSureCheck = [elem in i for elem in littleLessSure]
        if True in check:
            relevantOfflineWords.append(i)
        if check.count(True) >= 1:
            offlinePointCounter += 1
        if lessSureCheck.count(True) >= 1:
            offlinePointCounter += 0.5

    if len(relevantOfflineWords) ==0 and len(relevantOnlineWords) == 0:
        return "Not Sure"
    
    indexes = []
    totalItems = len(textList)

    if len(relevantOnlineWords) > len(relevantOfflineWords):
        relevantWords = relevantOnlineWords
    else:
        relevantWords = relevantOfflineWords    

    for i in textList:
        for j in relevantWords:
            if i == j:
                indexes.append(textList.index(i))

    sentences = {}
    
    for i in set(indexes):
        sentence = []
        for j in range(i,totalItems):
            sentence.append(textList[j])
            if textList[j][-1] == ".":
                break
            if len(sentence) > 20:
                break
        sentences[i] = sentence       
    
    complementaryWords = ["attend","attend","arrange","arranged","arrange.","arranged.","competition","competition."]

    nonComplementaryWords = ["registration","registration.","application","applications","application.","applications."]
    
    relevantCounter = 0
    
    for i in set(indexes):
        check = [elem in sentences[i] for elem in complementaryWords]
        nonCheck = [elem in sentences[i] for elem in nonComplementaryWords]

        if check.count(True) >= 3:
            relevantCounter += 3
        if check.count(True) == 2:
            relevantCounter += 2
        if check.count(True) == 1:
            relevantCounter += 1
        if nonCheck.count(True) >=1:
            relevantCounter -= 1  
    
    if len(relevantOnlineWords) > len(relevantOfflineWords):
        onlinePointCounter += relevantCounter
    else:
        offlinePointCounter += relevantCounter
      
    if onlinePointCounter > offlinePointCounter:
        return "Online"   
    else:
        return "Offline"    


def determine(url):
    try:
        text = getText(url)
        return detector(text) 
    except:
        return "Not Sure!"

# Currently Working below!!

# from fuzzywuzzy import fuzz
# from nltk import tokenize
# from nltk.corpus import stopwords
# from nltk.corpus import wordnet
# # from concurrent.futures import ThreadPoolExecutor
# from nltk.stem import WordNetLemmatizer


# # Removing stopwords (unnecessary words) from the text.
# def removeStopwords(text):
#     textList = text.split()
#     for i in textList:
#         if i in stopwords:
#             textList.remove(i) 
#     return textList


# # Determine ONLINE/OFFLINE
# def determine(text):
#     onlinePointCounter = 0
#     offlinePointCounter = 0

#     textList = removeStopwords(text)
#     lemmatizer = WordNetLemmatizer()

#     # Calculating Wratio of each word with respect to some relevant words.
#     sureConclusionsOnline = ["virtual","online","digital","web based","live-stream","video conference","webinar","remote","zoom","off-campus"]
#     sureConclusionsOffline = ["offline","physical","face-to-face","on-campus","on-premises","in-person"]

#     def getOnlineWratios():
#         onlineWratios = {}
#         for i in textList:
#             i = lemmatizer.lemmatize(i)
#             for j in sureConclusionsOnline:
#                 tempRatio = fuzz.WRatio(i,j)
#                 onlineWratios[i] = tempRatio
#         return onlineWratios        

#     def getOfflineWratios():
#         offlineWratios = {}
#         for i in textList:
#             i = lemmatizer.lemmatize(i)
#             for j in sureConclusionsOffline:
#                 tempRatio = fuzz.WRatio(i,j)
#                 offlineWratios[tempRatio,j] = i
#         return offlineWratios
    
#     sentencesList = tokenize.sent_tokenize(text)

#     def checkSameSentence(word1,word2):
#         for i in 

    
#     # with ThreadPoolExecutor() as executer:
#     #     findOnlineWratios = executer.submit(getOnlineWratios)   
#     #     findOfflineWratios = executer.submit(getOfflineWratios)  

#     #     onlineWratios = findOnlineWratios.result()
#     #     offlineWratios = findOfflineWratios.result()

#     onlineWratios = getOnlineWratios()
#     offlineWratios = getOfflineWratios()
#     print(onlineWratios)
#     # print(offlineWratios)





# if __name__ == "__main__":
#     stopwords = set(stopwords.words('english'))
#     text = "Given the prevailing health circumstances and the organizers' preference for broad and unrestricted participation, the imminent art exhibition will not physically occur in its typical setting. Instead, art enthusiasts can look forward to engaging with all pieces of art through a groundbreaking, user-friendly digital platform. This transition allows you to explore every art piece at your leisure and from the confinements of your own space. Essentially, the timing and date of this set-up will replicate the original plans."
#     determine(text)


