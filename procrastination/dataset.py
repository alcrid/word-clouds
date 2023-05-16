from sqlite3 import Timestamp
from time import time
import nltk
import json
import unidecode as uni
import nltk
from typing import List
import numpy as np
from itertools import chain



def flatten2D(lst):
    out = []
    for line in lst:
        for sent in line:
            out.append(sent)
    return out
    
#naive sentence split jff
def naive_sentenc_split(text):

    sites = ["sk","en","eu","com"]
    
    out = []
    text = text.split('?')
    for i in range(len(text)):
        if(not i == len(text)-1):
            out.append(text[i]+"? ")
      
     
    for part in range(len(out)):
        temp = []
        text = out[part].replace("!!!","!").split('!')
        for i in range(len(text)):
            if(not i == len(text)-1):
                temp.append(text[i]+"!")
            else:
                temp.append(text[i])
       
        out[part] = temp
      
    out =  flatten2D(out)

    for part in range(len(out)):
        temp = []

        text = out[part].replace("...",".").split('.')

        for i in range(len(text)):
            
            if("www" in text[i] or "http" in text[i]):
                s = ""
                if(i < len(text) -1):
                    for txt in text:
                        s += txt.strip()+ "."
                   
                
                temp.append(s)
                break


                '''print(text)
                if(i < len(text) -1 ):
                    s = text[i]+"."+text[i+1]+"."
                    if(i < len(text)-2):
                        for sit in site:
                            text[i+2]
                        if(i < len(text)-2 and text[i+2] in site):
                            s = s + text[i+2] + "." 
                            i += 2
                    else:
                        i += 1'''
                    
    
                #print(s)
                
                #temp.append(s)
            
            else:
                if(not i == len(text)-1):
                    temp.append(text[i]+".")
                else:
                    temp.append(text[i])
        
        out[part] = temp
    out =  flatten2D(out)

    for line in out:
        line.strip().replace("  ", " ")
        line.replace("\n", "").replace("\t", "")
        if(line == ''):
            line.remove()
    
    return out
   

#removes all accents from words so we don't have to deal with them
def remove_accent(s):
    s = uni.unidecode(s)
    return s

#json files save in the wrong encoding so we have to fix it 
def fix_encoding(s):
    #return s
    return uni.unidecode(s.encode('iso-8859-1').decode('utf-8'))

#experimental methods that check if the word contains accents
def contains_accent(s):
    if(remove_accent(s) != s):
        return True
    return False

# a helper method
def contains(s,a):
    return len(s) - len(s.replace(a,"")) != 0


def pr(o):
    for l in o:
        print(l)


#build a better intent classifier
#I need a better way to guess if something is a question
# an approach of trying to classify sentences into question, 
# didn't work much on this approach since I think there are better ones
def is_question(ans):
    question = ['nevedel by si','nemohla by si','nevedel by si',
    'mohol by si','mohla by si','vies mi','mozes mi',
    'by si mi','videl si','mozes',"nevies","prosim vedel","ako"]
    if(contains(ans,'?')):
        return True
    
    for ques in question:
        if(ques in ans):
            return True

    return False
    

def remove(s):
    s = uni.unidecode(s.replace(".","").replace("!","").replace("?","").replace("/","").replace("-","").replace("  "," ").replace("_","").replace(",","").replace("\"",""))
    s = s.lower()
    return s


def make_dataset(f,dataset):

    data = json.load(f)
    out = []


#gets the content of the messages from the messenger data
    print(len(data['messages']))


    for a in data['messages']:
            if("content" in a):
                for sentence in naive_sentenc_split(fix_encoding(a['content']).replace(".",". ")):
                    dataset.append(remove(sentence.replace("\n","").strip()))
                    #dataset.append(str(a["timestamp_ms"]) + "\n")






#writes the finished dataset to a json file
def write_dataset(dataset):

    json_object = json.dumps(dataset)
   
    import csv
    header = ["question","answer"]
    with open("datasets\sample", "w") as csv_file:
        for line in header:
            csv_file.write(line+",")
        csv_file.write('\n')

        for line in dataset:
            for parameter in line:
                csv_file.write(parameter+",")
            csv_file.write('\n')

   

