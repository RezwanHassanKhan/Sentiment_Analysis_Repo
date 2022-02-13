# -*- coding: utf-8 -*-
"""SentimentTextBlob.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zGeTij2g5rMvbiuDmNrrEwvJy68MagI5
"""

import pandas as pd
from textblob import TextBlob
from wordcloud import WordCloud 
import numpy as np
import re
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount("/content/drive")

data1=pd.read_csv('/content/drive/MyDrive/Bigtech - 20-09-2020 till 13-10-2020.csv')

data1.shape

data2=pd.read_csv('/content/drive/MyDrive/Bigtech - 12-07-2020 till 19-09-2020.csv')

data2.shape

data=data2.append(data1)

data.shape

data['text']

df=pd.DataFrame(data['text'].astype(str))

# Create a function to clean the tweets
def cleanTxt(text):
 text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
 text = re.sub('#', '', text) # Removing '#' hash tag
 text = re.sub('RT[\s]+', '', text) # Removing RT
 text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
 
 return text


# Clean the tweets
df['Tweets'] = df['text'].apply(cleanTxt)

# Show the cleaned tweets
df

# Create a function to get the subjectivity
def getSubjectivity(text):
   return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity
def getPolarity(text):
   return  TextBlob(text).sentiment.polarity
# Create two new columns 'Polarity'
df['Polarity'] = df['Tweets'].apply(getPolarity)

# Show the new dataframe with columns 'Subjectivity' & 'Polarity'
df

ds=df.loc[df['file_name'] =='Amazon' ]
ds.head()

# word cloud visualization
allWords = ' '.join([twts for twts in ds['Tweets']])
wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)


plt.imshow(wordCloud, interpolation="bilinear")
plt.axis('off')
plt.show()

# word cloud visualization
allWords = ' '.join([twts for twts in df['Tweets']])
wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)


plt.imshow(wordCloud, interpolation="bilinear")
plt.axis('off')
plt.show()

# Create a function to compute negative (-1), neutral (0) and positive (+1) analysis
def getAnalysis(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'
df['Analysis'] = df['Polarity'].apply(getAnalysis)
# Show the dataframe
df

# Plotting and visualizing the counts
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Analysis'].value_counts().plot(kind = 'bar')
plt.show()

# Plotting 
plt.figure(figsize=(8,6)) 
for i in range(0, df.shape[0]):
  plt.scatter(df["Polarity"][i], df["Subjectivity"][i], color='Blue') 
# plt.scatter(x,y,color)   
plt.title('Sentiment Analysis') 
plt.xlabel('Polarity') 
plt.ylabel('Subjectivity') 
plt.show()

df['created_at']=data['created_at']
df['file_name']=data['file_name']
df

ds=df.loc[df['file_name'] =='Apple' ]
ds.head()

# word cloud visualization
allWords = ' '.join([twts for twts in ds['Tweets']])
wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size=110).generate(allWords)


plt.imshow(wordCloud, interpolation="bilinear")
plt.axis('off')
plt.show()

df['date'] =  pd.to_datetime(df['created_at'])

df.drop(columns="created_at",inplace=True)

df['year']= df['date'].dt.year
df['month']= df['date'].dt.month
df['day']= df['date'].dt.day

df

df.to_csv('tweets.csv')

df.to_csv('/content/drive/MyDrive/tweets.csv')

#c=0
#for x,row in df.iterrows():
  #if(row['file_name']=='AMD'):
    #print(row['Tweets'])
    #ds.append({'Tweets':row['Tweets']}, ignore_index=True)
    #print("")
  #c=c+1
  #if c>10:
    #break

ds['Tweets']

x=(df['file_name']=='Youtube')

x

stock=pd.read_csv('/content/drive/MyDrive/StockPrice.csv')

stock

#setting index as date
stock['Date'] = pd.to_datetime(stock.Date,format='%m/%d/%Y')
stock.index = stock['Date']

#plot
plt.figure(figsize=(16,8))
plt.plot(stock['APPL'], label='OPEN')

#creating a separate dataset
new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])

for i in range(0,len(data)):
    new_data['Date'][i] = data['Date'][i]
    new_data['Close'][i] = data['Close'][i]

def getSIA(text):
  sia=SentimentIntensityAnalyzer()
  sentiment=sia.polarity_scores(text)
  return sentiment

def perday_positivetweet(dataset):
  for x in range(len(df)):
    if df.date[x]