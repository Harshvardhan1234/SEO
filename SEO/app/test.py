from pytrends.request import TrendReq

import matplotlib.pyplot as plt

import pandas as pd


import string


from bs4 import BeautifulSoup
import requests

import pandas as pd

import nltk
from nltk.corpus import stopwords
# nltk.download('stopwords')

stop_word = stopwords.words('english')





import spacy
from spacy.lang.en.examples import sentences 


nlp = spacy.load("en_core_web_sm")
en = spacy.load('en_core_web_sm')

stopwords = en.Defaults.stop_words






def current_trend():

    pytrends = TrendReq(hl='en-US')     
    keywords = [ 'Database', 'use', 'Android', 'error']
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
    # plt.savefig('static//key_word.jpg')
    plt.show()


    #extract country-level kewords search data
    country_data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True)

    #get countries with the highest searches of "Python"
    data2 = country_data['Database'].nlargest(10)
    
#     print(max(key_word_search(html_page)[0], key = len))
    #convert to dataframe
    data2 = data2.to_frame()



    data2.plot(kind='bar', legend=None)

    #titles
    plt.suptitle('Countries with the highest number of Python searches on Google Database')
    plt.ylabel('Number of searches')
    plt.xlabel('Countries')
    # plt.savefig('static//country.png')
    plt.show()




current_trend()