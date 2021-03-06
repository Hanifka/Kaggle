# -*- coding: utf-8 -*-
"""nlp-with-disaster-tweets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LVFUUgUVkx-lg6eDP1O6tpd-WOG7FvM_
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
# import re
# from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer
# from sklearn.feature_extraction. text import TfidfVectorizer
# from sklearn.svm import LinearSVC
# from sklearn.pipeline import Pipeline
# from sklearn.model_selection import train_test_split
# from sklearn.feature_selection import SelectKBest, chi2
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from wordcloud import WordCloud,STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.stem import LancasterStemmer,WordNetLemmatizer
import re, string, unicodedata
from string import punctuation

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

sw = stopwords.words("english")

"""# Import Data"""

training = pd.read_csv('/kaggle/input/nlp-getting-started/train.csv')
test = pd.read_csv('/kaggle/input/nlp-getting-started/test.csv')

# Commented out IPython magic to ensure Python compatibility.
test['target'] = np.nan
training['train_test'] = 0
test['train_test'] = 1
alldata = pd.concat([training,test])

# %matplotlib inline
alldata.columns

total = training.isnull().sum().sort_values(ascending=False)
percent = (training.isnull().sum()/training.isnull().count()).sort_values(ascending=False)
missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data.head(20)

"""# Data Exploration

* Disaster tweet detected 42 % in training dataset
* Wreckage is the most frequently detetcted as distaster in column keyword 
* Location column is garbage data
"""

training.target.value_counts(normalize = True)

training.describe()

training['keyword'].value_counts()

training['location'].value_counts()

col = ['keyword', 'location']
for i in col:  
    print(pd.pivot_table(training, index = 'target', columns = i,values = 'id',aggfunc='count'));print()

"""# Data Preparation"""

alldata.drop(['location'], axis=1, inplace=True)

def hapus_url(text):
    return re.sub(r'http\S+','', text)
def remove_special_characters(text, remove_digits=True):
    pattern=r'[^a-zA-Z0-9\s]'
    text=re.sub(pattern,'',text)
    return text
def stemmer(text):
    ps=nltk.porter.PorterStemmer()
    text=' '.join([ps.stem(word) for word in text.split()])
    return text

def final_clean(text):
    final_text= []
    for i in text.split():
        if i.strip().lower() not in sw and i.strip().lower().isalpha():
            final_text.append(i.strip().lower())
    return " ".join(final_text)

def clean(text):
    text = hapus_url(text)
    text = remove_special_characters(text, remove_digits=True)
    text = stemmer(text)
    text = final_clean(text)
    return text

alldata['text'] = alldata['text'].apply(clean)
training['text'] = training['text'].apply(clean)
test['text'] = test['text'].apply(clean)

alldata.head(50)

alldata.drop(["keyword"], axis=1, inplace=True)

alldata['target'].value_counts()

x_train=alldata[alldata.train_test == 0].drop(['train_test'],axis=1)
x_test=alldata[alldata.train_test == 1].drop(['train_test'],axis=1)
x_test.drop(["target"], axis=1, inplace=True)

x_train.info

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
x_test.columns

alldata.info()

"""# Training"""

from sklearn.feature_extraction.text import TfidfVectorizer

tfidf_vect = TfidfVectorizer()

text1 = tfidf_vect.fit_transform(x_train["text"])
text2 = tfidf_vect.transform(x_test["text"])

def transform(text):
    tfidf_vectorizer=TfidfVectorizer().fit(text)
    tfidf_text=tfidf_vectorizer.transform(text)
    return tfidf_text

from sklearn.svm import SVC
from sklearn.metrics import classification_report

model = SVC()
model.fit(text1,training['target'])

pred_svm = model.predict(text1)
print(classification_report(pred_svm, training['target']))

pred_svm2 = model.predict(text2)

submission = pd.DataFrame({'id':test['id'], 'target':pred_svm2})
submission.head ()

submission.to_csv('submission.csv',index=False)