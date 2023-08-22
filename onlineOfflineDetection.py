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

    sureConclusionsOnline = ["held","virtual","online","digital","web based","live-stream","video conference","webinar","remote","zoom","held","virtual.","online.","digital.","web based.","live-stream.","video conference.","webinar.","remote.","zoom."]
    
    for i in textList:
        check = [elem in i for elem in sureConclusionsOnline]
        if True in check:
            relevantOnlineWords.append(i)
        if check.count(True) >= 3:
            onlinePointCounter += 3
        if check.count(True) == 2:
            onlinePointCounter += 2
        if check.count(True) == 1:
            onlinePointCounter += 1  

    sureConclusionsOffline = ["held","offline","physical","face-to-face","on-campus","on-premises","accommodation","offline.","physical.","face-to-face.","on-campus.","on-premises.","accommodation.","travel","travel."]
    
    for i in textList:
        check = [elem in i for elem in sureConclusionsOffline]
        if True in check:
            relevantOfflineWords.append(i)
        if check.count(True) >= 3:
            offlinePointCounter += 3
        if check.count(True) == 2:
            offlinePointCounter += 2
        if check.count(True) == 1:
            offlinePointCounter += 1  
    
    if len(relevantOfflineWords) and len(relevantOnlineWords) == 0:
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

    complementaryWords = ["registration","registration.","attend","attend","arrange","arranged","arrange.","arranged."]
    
    relevantCounter = 0
    
    for i in indexes:
        check = [elem in sentences[i] for elem in complementaryWords]
        if check.count(True) >= 3:
            relevantCounter += 3
        if check.count(True) == 2:
            relevantCounter += 2
        if check.count(True) == 1:
            relevantCounter += 1 

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