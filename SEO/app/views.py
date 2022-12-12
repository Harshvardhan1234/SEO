from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.

import string

import re

from bs4 import BeautifulSoup
import requests

import pandas as pd

import nltk
from nltk.corpus import stopwords
# nltk.download('stopwords')

stop_word = stopwords.words('english')


import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq



import spacy
from spacy.lang.en.examples import sentences 


nlp = spacy.load("en_core_web_sm")
en = spacy.load('en_core_web_sm')

stopwords = en.Defaults.stop_words


punctuation = list(string.punctuation)
# print(punctuation)






def home(request):
    return render(request, 'home.html')



def preprocess(request):
    
    score = 0
       
    data = request.POST["data"]  
      
    html_page = requests.get(data).text
    soup = BeautifulSoup(html_page , 'lxml')

     
    # key_word_search(html_page,soup)
    # print(key_word_search(html_page,soup)[1])
    # print(key_word_search(html_page,soup)[0])
    
    # ________________________________________key word______________________________________________________________
    
    if key_word_search(html_page,soup)[2] ==0:
        score +=0
    elif key_word_search(html_page,soup)[2] <=10 and key_word_search(html_page,soup)[2] >=3:
        score+=7.5
        print("score: ",score,"\n value:",key_word_search(html_page,soup)[2])
        
    elif key_word_search(html_page,soup)[2] >= 10:
        score+=20
        print("score: ",score,"\n value:",key_word_search(html_page,soup)[2])
    
    # ________________________________________ H - TAG COUNT______________________________________________________________
    
    print(h_tags(html_page,soup))
    
    
    score +=sum(h_tags(html_page,soup)[0:2])
    print("score: ",score,"\n value:",sum(h_tags(html_page,soup)[0:2]))
    # ________________________________________ META TAGS______________________________________________________________
    
    meta = meta_tags(html_page)
    
    print("\n____________________________________________________________________________\n")
    print(meta[0],meta[1])
    
    if meta[0] ==0 or meta[1] < 5:  
        score +=7
    elif meta[0] ==0:
        score +=0
        
    else:

        probability = meta[0]/(meta[0]+meta[1])
        
        
        if probability <= 15:
            score += 7
            print("score: ",score,"\n probability:",probability)
            
        if probability >15:
            score += 20
            print("score: ",score,"\n probability:",probability)
        
    
    # ________________________________________ CURRENT TREND______________________________________________________________
    current_trend(html_page,soup)
    
    
    # print("\n____________________________________________________________________________\n")
    
  
    
    return render(request, 'home.html',{'keyWord':key_word_search(html_page,soup)[0],
                                        'flush':key_word_search(html_page,soup)[1],
                                        "hTags":h_tags(html_page,soup),
                                        "metaTags":meta})









def meta_tags(html_page):
    soup = BeautifulSoup(html_page , 'lxml')
    # print(soup)

    meta_list = []
    
    follow = "rel=[\'|\"]follow|rel=[\'|\"][a-zA-z]+ follow"

    match = re.findall(follow, str(soup))

    print("follow  links => ",len(match))
    meta_list.append(len(match))



    nofollow = "rel=[\'|\"]nofollow|rel=[\'|\"][a-zA-z]+ nofollow"

    matchx = re.findall(nofollow, str(soup))

    print("follow  links => ",len(matchx))
    meta_list.append(len(matchx))
    
    
    
    
    return meta_list











def h_tags(html_page,soup):
    
    h_tags_count = []
    tages = ["h1",'h2',"h3"]
    count = 0

    h1 = []
    h2 = []
    h3 = []

    for x in tages:

        for link in soup.find_all(x):
            count +=1

            if x == 'h1':
                h1.append(link.text.replace('\n',''))


            if x == 'h2':
                h2.append(link.text.replace('\n',''))

            if x == 'h3':
                h3.append(link.text.replace('\n',''))




    #         print(link.text)

        # print(x,"=>",count)
        h_tags_count.append(count)
        count = 0
        
        
    return h_tags_count
        
        



def key_word_search(html_page,soup):

    tages = ["h1",'h2',"h3"]
    count = 0

    h1 = []
    h2 = []
    h3 = []

    for x in tages:

        for link in soup.find_all(x):
            count +=1

            if x == 'h1':
                h1.append(link.text.replace('\n',''))


            if x == 'h2':
                h2.append(link.text.replace('\n',''))

            if x == 'h3':
                h3.append(link.text.replace('\n',''))
        count = 0


    h_tage_sentance = ""


    h_tags = [h1,h2]

    for hh in h_tags:
        for x in hh:           #''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
            for y in x:
                if y in punctuation or y =='–':
        #             print("|",y,"|")
                    continue

                else:
                    h_tage_sentance += y
        

            h_tage_sentance += " "


    doc = nlp(h_tage_sentance)


    key_words = []
    for x in doc:

        if len(x) <=2:    # ignoring 2 words letter
            continue

        if (x.lemma_ not in stopwords) and (x.lemma_ not in stopwords):
            key_words.append(x)


    for x in key_words:
        if len(x) == 1:
            key_words.remove(x)



    key_word_lemma = []

    for x in key_words:
        key_word_lemma.append(x.lemma_)
   
    para = soup.find_all("p")
    
    
    
    
    required_para_lenght = len(para)*.25

    # print("No of paragraph : ",len(para))

    count =0

    total_word_count = 0

    words = []

    for x in para:

        if count > required_para_lenght:
            break

        doc = nlp(x.text)

        for data in doc:
            total_word_count +=1
            data = data.lemma_

            if data in key_word_lemma:
    #             print(data)
                words.append(data)
        count +=1

    unique_key_word = [*set(words)]   
    
    key_word_flusing = {}
        
    
    for  f in unique_key_word:
        key_word_flusing[f] = 0
        
    for datax in words:
        key_word_flusing[datax]+=1
        
#     print(max(key_word_flusing.values()))
#     print(total_word_count)
#     print(key_word_flusing)
    
    
#     print(total_word_count/max(key_word_flusing.values()))
    kwf = "NO Key Word Flusing"
    if key_word_flusing.values() ==0:
        temp = [1]
        
    else:
        temp = key_word_flusing.values()
    if total_word_count/max(key_word_flusing.values()) < 37.00:
        kwf = "key word flusing"
        print("key word flusing")
        
        
        
        
    ret_data = [unique_key_word,kwf,len(words)]
    return ret_data

    





def current_trend(html_page,soup):

    pytrends = TrendReq(hl='en-US')     
    keywords = key_word_search(html_page,soup)[0][:5]
    pytrends.build_payload(keywords, timeframe='today 5-y')


    data = pytrends.interest_over_time()
    data = data.drop('isPartial', axis=1)




    #plot data
    plt.plot(data)

    #add titles
    plt.suptitle('Programming Language Searches on Google Trends')
    plt.xlabel('years')                       
    plt.ylabel('weekly searches')  

    #add legend
    plt.legend(keywords, loc='upper left')
    plt.savefig(r'app/static/key_word.jpg')
    # plt.show()


    country_data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)

    try:
        data2 = country_data[key_word_search(html_page,soup)[0][0]].nlargest(10)
    
        data2 = data2.to_frame()



        data2.plot(kind='bar', legend=None)

        #titles
        plt.suptitle('Countries with the highest number of Python searches on Google ('+key_word_search(html_page,soup)[0][0]+')')
        plt.ylabel('Number of searches')
        plt.xlabel('Countries')
        plt.savefig(r'app/static/country.png')
    # plt.show()
    except:
        car = 1


     