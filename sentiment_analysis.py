import re
import os
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy
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



def preprocess_text(text):
    nlp = spacy.load('en_core_web_sm')
    stop_words = set(stopwords.words('english'))
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and token.lemma_ not in stop_words]
    return ' '.join(tokens)

def topic_modelling(temp_data):

    temp_data['processed_txt'] = temp_data['mssgs'].apply(preprocess_text)
    data_list = list(temp_data['processed_txt'])

    vectorizer = CountVectorizer(analyzer='word')
    X = vectorizer.fit_transform(data_list)

    # Create and fit an LDA model
    lda = LatentDirichletAllocation(n_components=5)
    lda.fit(X)

    topics = []
    terms = vectorizer.get_feature_names_out()
    for idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[-5:][::-1]
        top_words = [terms[i] for i in top_words_idx]
        topics.append({
            'Topic': f'Topic {idx + 1}',
            'Top Words': ", ".join(top_words)
        })

    topics_df = pd.DataFrame(topics)
    return topics_df
















