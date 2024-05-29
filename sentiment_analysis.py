import re
import os
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('stopwords')
nltk.download('vader_lexicon')


def give_senti_data(selected_user, df, start_date, end_date):
    try:
        if selected_user != "overall":
            df = df[df['user'] == selected_user]  # Filter by user if not 'overall'

        mask = (df['msg_dates'] >= start_date) & (df['msg_dates'] <= end_date)
        senti_analysis_data = df.loc[mask]  # Efficient filtering

        # Remove media messages and group notifications
        senti_analysis_data = senti_analysis_data[
            ~senti_analysis_data['message'].str.contains('<Media omitted>\n') &
            ~senti_analysis_data['user'].eq('grp_notification')
            ]

        senti_analysis_data = senti_analysis_data[['user', 'message']]

        # Convert messages to a single Series for easier processing
        senti_analysis_data = senti_analysis_data['message'].values

        # Create a DataFrame from the messages
        temp = pd.DataFrame(senti_analysis_data, columns=['mssgs'])

        return temp
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def give_sentiment_score(temp_data):

      analyzer=SentimentIntensityAnalyzer()
      temp_data['positive']=[analyzer.polarity_scores(i)['pos'] for i in temp_data['mssgs']]
      temp_data['negative']=[analyzer.polarity_scores(i)['neg'] for i in temp_data['mssgs']]
      temp_data['neutral']=[analyzer.polarity_scores(i)['neu'] for i in temp_data['mssgs']]
      temp_data['compound']=[analyzer.polarity_scores(i)['compound'] for i in temp_data['mssgs']]

      avg_compd=temp_data['compound'].mean()
      return avg_compd















#creating data for senti. analysis
# def give_senti_data(selected_user,df,start_date,end_date):
#
#     if (selected_user != "overall"):
#         df = df[df['user'] == selected_user]
#
#
#     # start_date = input("Enter the starting date for your sentiment analysis:")
#     # end_date = input("Enter the ending date for your sentiment analysis:")
#
#     mask = (df['msg_dates'] >= start_date) & (df['msg_dates'] <= end_date)
#     senti_analysis_data = df.loc[mask]
#     senti_analysis_data = senti_analysis_data[['user', 'message']]
#
#     senti_analysis_data = senti_analysis_data[senti_analysis_data['message'] != '<Media omitted>\n']
#     senti_analysis_data = senti_analysis_data[senti_analysis_data['user'] != 'grp_notification']
#
#     senti_analysis_data = senti_analysis_data['message']
#
#     temp = pd.DataFrame(data=senti_analysis_data.values, columns=['mssgs'])
#
#     return temp
