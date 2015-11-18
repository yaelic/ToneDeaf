__author__ = 'yaelcohen'

import re, math, collections, itertools
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import pyglet
import os.path
from Tkinter import *
import re
from wave import open as waveOpen
#from ossaudiodev import open as ossOpen
import subprocess

## stem and lower case ot ad ly to stuff
negative = ["no","stop","tired","bad","suck","worst","horrible","terrible","outrageous","disaster","unhappy","disappointed","hard","tough","difficult","fail","sad","unfortunate","flunk","rough","hate"]
positive = ["great","amazing","fun", "happy","good","thanks","wow","awesome","best","super",'groovy',"cool","lovely","nice","fabulous","fantastic","love","like"]
sorry =["sorry", "apologize", "sadly","regret","unfortunately","bother"]
please = ["please", "request","may","kindly","help","dear","thank","bless"]
exc = ["!", "asap","quickly","fast","hurry", "now", "urgent","immediately","right away","first thing in the", "as soon as" ]
money = ["pay","owe","$","money","expensive","cheep","buy","spend","dollars","debit","credit","debt", "broke","dime","penny","currency", "stock","share","invest","lend","bank","check","lend","loan","overdraft","tax","interest","bills"]
love =["miss","love","wait","nice","fun","care","feel","heart","hug","kiss","crazy","xoxo","dear","honey","sweet","sweetie","pumpkin","darling","precious","sunshine","babe","doll","baby"]

def parseText(text):
    """

    :param text:
    :return:
    """
    res = {
        'words' : 0,
        'verbs' : 0,
        'sorry_please'  : 0,
        'exclamation' : 0,
        'positive' : 0,
        'money' : 0,
        'negative':0,
        'love': 0
    }
    SentenceTokenizer = nltk.tokenize.PunktSentenceTokenizer()
    stem1 =nltk.stem.porter.PorterStemmer()
    stem2 = nltk.stem.lancaster.LancasterStemmer()
    stem3 = nltk.stem.WordNetLemmatizer()
    verbPattern = re.compile('^V')
    wordPattern = re.compile('^[A-Za-z]')
    posPattern = re.compile('^[A-Z]')
    sentences =SentenceTokenizer.tokenize(text)
    for s in sentences :
        pos = nltk.word_tokenize(s)
        words = nltk.pos_tag(pos)
        for word in words:
            stemmedWord1 = stem1.stem(word[0])
            stemmedWord2 = stem2.stem(word[0])
            stemmedWord3 = stem3.lemmatize(word[0])
            pos = word[1]
            w = word[0].lower()
            isWord = wordPattern.match(w)
            isPos = posPattern.match(pos)
            if isWord and isPos:
                res["words"] += 1
            verb = verbPattern.match(pos)
            if verb:
                res["verbs"] +=1
            if w in positive or stemmedWord1 in positive or stemmedWord2 in positive or stemmedWord3 in positive or checkStem(positive, stem1,w) or checkStem(positive, stem2,w):
                res["positive"] += 1
            if w in negative or stemmedWord1 in negative or stemmedWord2 in negative or stemmedWord3 in negative or checkStem(negative, stem1,w) or checkStem(negative, stem2,w):
                res["negative"] += 1
            if w in sorry or stemmedWord1 in sorry or stemmedWord2 in sorry or stemmedWord3 in sorry or checkStem(sorry, stem1,w) or checkStem(sorry, stem2,w):
                res["sorry_please"] += 1
            if w in please or stemmedWord1 in please or stemmedWord2 in please or stemmedWord3 in please or checkStem(please, stem1,w) or checkStem(please, stem2,w):
                res["sorry_please"] += 1
            if w in exc or stemmedWord1 in exc or stemmedWord2 in exc or stemmedWord3 in exc or checkStem(exc, stem1,w) or checkStem(exc, stem2,w):
                res["exclamation"] += 1
            if w in money or stemmedWord1 in money or stemmedWord2 in money or stemmedWord3 in money or checkStem(money, stem1,w) or checkStem(money, stem2,w):
                res["money"] += 1
            if w in love or stemmedWord1 in love or stemmedWord2 in love or stemmedWord3 in love or checkStem(love, stem1,w) or checkStem(love, stem2,w):
                res["love"] += 1
    print "Done reading"
    print res
    return res

def checkStem(list, stemmer, word):
    for w in list:
        if stemmer.stem(word) == stemmer.stem(w):
            return True
    return False

def calc_res(res):
    wc = res['words']*1.0

    if res['money']/wc >= 0.02:
        print "money!"
        return "money"
    if res['love']/wc >= 0.15:
        print "In love.."
        return "love"
    if res["sorry_please"]/wc >=0.08:
        print "princes"
        return "suck-up"
    if res['negative'] > res['positive'] and res['negative']/wc >=0.03:
        print "sad"
        return "negative"
    if res['negative'] < res['positive'] and res['positive']/wc >=0.04:
        print "happy"
        return "positive"

    if res['verbs']/wc >= 0.24:
        print "bossy!"
        return "bossy"
    else:
        print "boring"
        return "snore"


def make_sound(res):
    audio_file = "/Users/yaelcohen/Desktop/sound/explosion-01.mp3"
    bark_bossy = "/Users/yaelcohen/Desktop/sound/DogsBarking-SoundBible.com-625577590.wav"
    whine_negative = "/Users/yaelcohen/Desktop/sound/Whine-SoundBible.com-1207627053.mp3"
    ahh_love = "/Users/yaelcohen/Desktop/sound/Aww-SoundBible.com-1421700712.wav"
    laugh_positive = "/Users/yaelcohen/Desktop/sound/laugh-man-02.wav"
    cash_money = "/Users/yaelcohen/Desktop/sound/Cha_Ching_Register-Muska666-173262285.wav"
    snorr_rest = "/Users/yaelcohen/Desktop/sound/snore-02.wav"
    suckUP = "/Users/yaelcohen/Desktop/sound/SuckUp-SoundBible.com-923941205.wav"

    if res == "bossy":
        os.system("afplay " + bark_bossy)
    if res == "love":
        os.system("afplay " + ahh_love)
    if res == "money":
        os.system("afplay " + cash_money)
    if res == "snore":
        os.system("afplay " + snorr_rest)
    if res == "negative":
        os.system("afplay " + whine_negative)
    if res == "positive":
        os.system("afplay " + laugh_positive)
    if res == "suck-up":
        os.system("afplay " + suckUP)
    print "make sound"

def runner():
    data = text.get("1.0",END)
    res = parseText(data)
    outcome = calc_res(res)
    make_sound(outcome)


t= "go do your homework now! don't forget to eat lunch, wash the dishes and walk the dog"
t= "baby I miss like crazy.. cant wait till you come back. love you XOXO "
t="Dear man, I'm really sorry to bother you but unfortunately I need your help. I would be forever greatfull if you are willing to help me"
t="Dad, all my friends have an Iphone and I done.. can you please buy me one.. Its not that expensive and I'll pay you back with kisses"
t="this day sucks! I hate my dad.. Im coming straight to your place"



################## GUI ###################
root = Tk()
root.title("Sound Send")
root.geometry("400x400")

app =Frame(root)
textfr = Frame(root)
text=Text(textfr,height=30,width=50,background='white')
scroll=Scrollbar(textfr)
text.configure(yscrollcommand=scroll.set)
button = Button(app,text = "send",command = runner)

app.pack(side=BOTTOM)
textfr.pack(side=TOP)
text.pack(side=LEFT)
scroll.pack(side=RIGHT,fill=Y)
button.pack(side= RIGHT )

root.mainloop()





