import pandas as pd

enquire_df = pd.read_csv('./all_data/label_data/car_enquire.csv')
breakdown_df = pd.read_csv('./all_data/new_data/breakdown.csv')
testdrive_df = pd.read_csv('./new_testdrive.csv')
#feedback = pd.read_csv('./all_data/label_data/feedback_tweets.csv')
#reply = pd.read_csv('./all_data/label_data/reply_tweets.csv')
#feedback = pd.concat([feedback, reply])
quality_df = pd.read_csv('./all_data/label_data/quality.csv')

import re
import nltk
#nltk.download('stopwords')
from nltk.probability import FreqDist
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english')) # Creates a list of stopwords
import seaborn as sns
import matplotlib.pyplot as plt
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet
import numpy as np
np.random.seed(2018)
import nltk
#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

# To clean the text of unnecessary data
def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"how's", "how is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r'\S*@\S*\s?', '', text)
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', '', text)
    text = re.sub(r"[^A-Za-z]", " ", text)
    return text

breakdown_df['text'] = breakdown_df['text'].apply(lambda x : clean_text(x))
testdrive_df['text'] = testdrive_df['text'].apply(lambda x: clean_text(x))
enquire_df['text'] = enquire_df['text'].apply(lambda x: clean_text(x))
quality_df['text'] = quality_df['text'].apply(lambda x: clean_text(x))

#Removing yes from stop_testdrive
def word_splitter(obj):
    obj = obj.split(' ')
    return(len(obj) > 2)
testdrive_df = testdrive_df[testdrive_df['text'].map(word_splitter)]

# Displays the most frequently used word
def count_words(data):
    words = ' '.join([text for text in data])
    words = words.split()
    fdist = FreqDist(words)
    words_df = pd.DataFrame({'words': list(fdist.keys()), 'keys': list(fdist.values())})
    
    freq = words_df.nlargest(columns='keys', n=50)
    
    plt.figure(figsize=(12,15)) 
    ax = sns.barplot(data=freq, x="keys", y="words") 
    ax.set(ylabel = 'Word') 
    plt.show()
    
'''# Before filtering
count_words(breakdown_df['text'])
count_words(testdrive_df['text'])
count_words(feedback['text'])
count_words(quality_df['text'])
count_words(car_enq_df['text'])'''


# Removing stopwords from cleaned texts
def remove_stop_words(data):
    filtered_text = [lemmatize_stemming(word) for word in data.split() if word not in stop_words]
    filtered_size = [word for word in filtered_text if len(word) > 2]
    return ' '.join(filtered_size)

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)
  
def lemmatize_stemming(text):
   return  WordNetLemmatizer().lemmatize(text, get_wordnet_pos(text))

'''def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result'''

breakdown_df['text'] = breakdown_df['text'].apply(lambda x : remove_stop_words(x))
testdrive_df['text'] = testdrive_df['text'].apply(lambda x: remove_stop_words(x))
enquire_df['text'] = enquire_df['text'].apply(lambda x: remove_stop_words(x))
quality_df['text'] = quality_df['text'].apply(lambda x: remove_stop_words(x))


'''# After filtering
count_words(breakdown_df['text'])
count_words(testdrive_df['text'])
count_words(feedback['text'])
count_words(quality_df['text'])
count_words(car_enq_df['text'])'''


pooled_data = breakdown_df
pooled_data = pooled_data.append(testdrive_df, ignore_index = True)
pooled_data = pooled_data.append(enquire_df, ignore_index = True)
pooled_data = pooled_data.append(quality_df, ignore_index = True)


print(type(pooled_data))

pooled_data.to_csv(r'new_data.csv')
