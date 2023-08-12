#IMPORT REQUIRED LIBRARIES
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import words #FILE PRESENT THE SAME DIRECTORY ,INCLUDES POSITIVE AND NEGATIVE WORDS (THAT ARE NOT PRESENT IN STOP WORDS) AND CAN BE ACCESSED USING words.postive_worrds, words.negative_words
import stop #FILE PRESENT THE SAME DIRECTORY ,INCLUDES STOP WORDS ARRAY , CAN BE ACCESSED USING stop.stop_words_array
import string
import pyphen
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize

#INITIALIZE THE NEGATIVE WORD DICTIONARY , KEYS ARE THE NEGATIVE WORDS AND VALUES ARE INITIALIZED TO ZERO
def init_positive():
    dict_positive={}
    for w in words.positive_words:
        dict_positive[w]=0
    return dict_positive

#INITIALIZE THE POSITIVE WORD DICTIONARY , KEYS ARE THE POSITIVE WORDS AND VALUES ARE INITIALIZED TO ZERO
def init_negative():
    dict_negative={}
    for w in words.negative_words:
        dict_negative[w]=0
    return dict_negative


def score(clean_tokens_arr):
    #INITIALIZE DICTIOANRIES
    positive_word_count=init_positive()
    negative_word_count=init_negative()
    #FOR EACH OCCURRENCE OF KEY IN THE ARTICLE INCREMENT ITS VALUES BY 1
    for w in clean_tokens_arr:
        if w in positive_word_count.keys():
            positive_word_count[w]+=1
            # print(w)
        if w in negative_word_count.keys():
            negative_word_count[w]+=1

    #GET THE DICTIONARIES (THAT CONTAIN THE COUNT OF EACH POSITIVE AND NEGATIVE WORD IN THE ARTICLE) BY UNCOMMENTING THIS
    # print(positive_word_count)
    # print(negative_word_count)

    #TOTAL POSITIVE WORDS
    score_p=sum(positive_word_count.values())
    #TOTAL NEGATIVE WORDS
    score_n=sum(negative_word_count.values())
    #POLARITY
    polarity=(score_p-score_n)/ ((score_p + score_n) + 0.000001)
    #SUBJECTIVITY
    subjectivity=(score_p+score_n)/ ((len(clean_tokens_arr)) + 0.000001)

    return score_p,score_n,polarity, subjectivity


#FUNCTION TO GET SYLLABLE COUNT IN A WORD
def get_syllable_count(word):
    dic = pyphen.Pyphen(lang='en_US') 
    syllables = dic.inserted(word).count('-') + 1
    return syllables

#FUNCTION TO GET COMPLEX WORD COUNT
def get_complex_count(words):
    complex_words = [word for word in words if get_syllable_count(word) > 2]
    return len(complex_words)

#FUNCTION TO GET AVERAGE SYLLABLE COUNT
def avg_syllable_count(word_tokens):
    scount=0
    for w in word_tokens:
        scount+=get_syllable_count(w)
    return scount/len(word_tokens)


#FUNCTION TO GET WORD COUNT
def word_count(w_tokens):
    count=0
    for w in w_tokens:
        if w not in stopwords.words("english"):
            count+=1
    return count

#FUNCTION TO GET NUMBER OF PERSONAL PRONOUNS IN THE ARTICLE 
def count_personal_pronouns(text):
    # Define the pattern to match personal pronouns
    pronoun_pattern = r'\b(I|we|my|ours|us|We|My|Ours)\b'

    # Use regex to find all occurrences of the pattern in the text
    pronouns = re.findall(pronoun_pattern, text, flags=re.IGNORECASE)

    # Exclude the occurrences of "US" as a country name
    country_name_pattern = r'\bUS\b'
    country_name_occurrences = re.findall(country_name_pattern, text, flags=re.IGNORECASE)
    
    # Remove "US" occurrences from the personal pronouns list
    personal_pronouns = [pronoun.lower() for pronoun in pronouns if pronoun.lower() not in set(country_name_occurrences)]

    return len(personal_pronouns)


#FUNCTION TO GET AVERAGE WORD LENGTH
def avg_word_length(tokens):
    word_length_list=[]
    for w in tokens:
        word_length_list.append(len(w))
    return np.mean(word_length_list)

#IMPORT THE INPUT DATA FROM EXCEL TO PANDAS DATAFRAME
excel_data = pd.read_excel('Input.xlsx')
data = pd.DataFrame(excel_data, columns=['URL_ID', 'URL'])
list_urls=data['URL'].values

#LISTS FOR STORING OUTPUT
TITLE=[]
POSITIVE_SCORE=[]
NEGATIVE_SCORE=[]
POLARITY=[]
SUBJECTIVITY=[]
AVG_SENTENCE_LENGTH=[]
PERCENTAGE_OF_COMPLEX_WORDS=[]
FOG_INDEX=[]
AVG_NUMBER_OF_WORDS_PER_SENTENCE=[]
COMPLEX_WORD_COUNT=[]
WORD_COUNT=[]
SYLLABLE_PER_WORD=[]
PERSONAL_PRONOUNS=[]
AVG_WORD_LENGTH=[]

#FOR EACH URL PRESENT IN THE IMPUT FILE RUN THE LOOP TO GET RESULTS INTO THE ABOVE LIST
for u in list_urls:
    response = requests.get(u)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    #EXTRACT TITLE FROM THE TITLE TAG
    title=soup.title.string.replace(' | Blackcoffer Insights','')
    if title:
        TITLE.append(title)
    else:
        TITLE.append("TITLE NOT FOUND") #IF TITLE IS NOT FOUND
    paragraphs = soup.find_all('p')[16:-3]
    article_text=""
#Extract the text contents of the paragraphs
    for p in paragraphs:
        article_text+=p.text

# Sent Tokenize the entire text
    s_tokens = sent_tokenize(article_text) 
    #WORD TOKENS INCLUDING PUNCTUATION AND OTHERS LIKE  ['’','s','ve','t','ll']:
    tokens=[]
    for s in s_tokens:
        tokens.extend(word_tokenize(s))

# print("NUMBER OF WORDS BEFORE CLEANING: ")
# print(len(tokens)) 

#WORD TOKENS WITHOUT PUNCTUATION AND  ['’','s','ve','t','ll']:
    word_tokens=[]          
    for w in tokens:
        if w not in string.punctuation and w not in ['’','s','ve','t','ll']:
            if '.' in w:
                word_tokens.extend(w.split('.'))
            else:
                word_tokens.append(w)
    

#CLEANING TOKENS->TOKENS THAT ARE NOT IN STOP WORDS OR PUNCTUATION LIST
    clean_text_tokens=[]
    for w in word_tokens:
        w=w.lower()
        if w not in stop.stop_words_array:
            clean_text_tokens.append(w)
    
# print("NUMBER OF WORDS AFTER CLEANING: ")
# print(len(clean_text_tokens))

#GETTING SCORES AND APPENDING TO LIST FOR THE CORESSPONDING ARTICLE 
    POSITIVE_SCORE.append(score(clean_text_tokens)[0])
    NEGATIVE_SCORE.append(score(clean_text_tokens)[1])
    POLARITY.append(score(clean_text_tokens)[2])
    SUBJECTIVITY.append(score(clean_text_tokens)[3])
    
# Analysis of Readability
    num_words=len(word_tokens)
    num_sent=len(s_tokens)
    avg_w_per_sent=num_words/num_sent
    AVG_NUMBER_OF_WORDS_PER_SENTENCE.append(avg_w_per_sent)

# 1. AVG SENTENCE LENGTH
    avg_sent_length=num_words/num_sent
    AVG_SENTENCE_LENGTH.append(avg_sent_length)

#2. PERCENT COMPLEX WORDS
    cc=get_complex_count(word_tokens)
    percent_complex_words=(cc/num_words)*100
    PERCENTAGE_OF_COMPLEX_WORDS.append(percent_complex_words)
    COMPLEX_WORD_COUNT.append(cc)

#3 FOG INDEX
    fog_index=0.4*(avg_sent_length+percent_complex_words)
    FOG_INDEX.append(fog_index)

#5. WORD COUNT
# We count the total cleaned words present in the text by 
# removing the stop words (using stopwords class of nltk package).
# and removing any punctuations like ? ! , . from the word before counting.

    wc=word_count(word_tokens)
    WORD_COUNT.append(wc)

#6 AVG SYLLABLE COUNT
    avg_sc=avg_syllable_count(word_tokens)
    SYLLABLE_PER_WORD.append(avg_sc)

# 7. PERSONAL PRONOUNS
    pp=count_personal_pronouns(article_text)
    PERSONAL_PRONOUNS.append(pp)

#8. AVG WORD LENGTH
    avg_word_len=avg_word_length(tokens)
    AVG_WORD_LENGTH.append(avg_word_len)

#ADDING THE COLUMNS AND VALUES FOR EACH ARTICLE IN THE DATAFRAME 'data'
data['TITLE']=TITLE
data['POSITIVE_SCORE']=POSITIVE_SCORE
data['NEGATIVE_SCORE']=NEGATIVE_SCORE
data['POLARITY']=POLARITY
data['SUBJECTIVITY']=SUBJECTIVITY
data['AVG_SENTENCE_LENGTH']=AVG_SENTENCE_LENGTH
data['PERCENTAGE_OF_COMPLEX_WORDS']=PERCENTAGE_OF_COMPLEX_WORDS
data['FOG_INDEX']=FOG_INDEX
data['AVG_NUMBER_OF_WORDS_PER_SENTENCE']=AVG_NUMBER_OF_WORDS_PER_SENTENCE
data['COMPLEX_WORD_COUNT']=COMPLEX_WORD_COUNT
data['WORD_COUNT']=WORD_COUNT
data['SYLLABLE_PER_WORD']=SYLLABLE_PER_WORD
data['PERSONAL_PRONOUNS']=PERSONAL_PRONOUNS
data['AVG_WORD_LENGTH']=AVG_WORD_LENGTH

print(data)
# Export DataFrame to Excel
excel_file_path = 'output.xlsx'
data.to_excel(excel_file_path, index=False)
