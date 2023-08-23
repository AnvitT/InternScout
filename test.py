from fuzzywuzzy import fuzz
import nltk
import time

text = "In light of the ever-changing landscape and keeping everyone's wellbeing in mind, we have decided to adapt our usual forum to an even more inclusive setting. Brace yourself for an exciting, groundbreaking tech event unlike any other, accessible right from the comfort of your home or office. Our aim, as always, is to provide you with an immersive experience that disrupts boundaries and transcends borders. No need to worry about your geographical location or travel restrictions, all you need is a reliable internet connection to tap into the wealth of knowledge we've curated. You are just a click away from joining us in this innovative tech journey unfolding in the digital realm."
textList = text.lower().split()
def wordDistance(textList,firstWord,secondWord):
    ans = len(textList)
    L = None
    for R in range(len(textList)):
        if textList[R] == firstWord or textList[R] == secondWord:
            if L is not None and textList[R] != textList[L]:
                ans = min(ans, R - L - 1)
                L = R
        return -1 if ans == len(textList) else ans
print(wordDistance(textList,"in","light"))

def shortestDistance(s, word1, word2) :
 
    d1 = -1; d2 = -1;
    ans = 100000000;
 
    # Traverse the string
    for i in range(len(s)) :
        if (s[i] == word1) :
            d1 = i;
        if (s[i] == word2) :
            d2 = i;
        if (d1 != -1 and d2 != -1) :
            ans = min(ans, abs(d1 - d2));
 
    # Return the answer
    return ans;




# print(nltk.sent_tokenize(text))
