# **WhatsApp Chat Analyzer**

## Introduction

The WhatsApp Chat Analyzer is a web-based application that allows users to upload their exported WhatsApp chat files and receive a detailed analysis of the conversation. The analysis includes message frequency, user activity, sentiment analysis, word cloud, emoji usage, and important topics discussed.



## Obtaining WhatsApp Chat Export

To use the WhatsApp Chat Analyzer, follow these steps to obtain the required .txt file from WhatsApp:

1. Open the WhatsApp application on your smartphone.
2. Choose the chat conversation that you want to analyze.
3. Tap on the three dots in the top right corner to access the options menu.
4. Select "More", then choose "Export chat" .
5. Select "Without Media" to export the chat as a .txt file.


## Accessing the Application

The WhatsApp Chat Analyzer is hosted using Streamlit Sharing and can be accessed at [Demo](https://whatsappchatanalyzer00byatharv-kkjx9irgrapbp4e8ub2qju.streamlit.app/).

## Python Libraries Used

The WhatsApp Chat Analyzer utilizes the following Python libraries:
- **Streamlit**: For building the interactive web application.
- **pandas**: For data manipulation and analysis.
- **NLTK**: For natural language processing tasks such as tokenization and stop word removal.
- **WordCloud**: For generating word clouds.
- **Matplotlib**: For creating visualizations.
- **TextBlob**: For sentiment analysis.
- **Gensim**: For topic modeling.
- Additionally, a special .txt file named "stop_hinglish" is used to remove the stop words. This file includes stop words of English and commonly used words in Hindi.


## Features

- **Overall and Individual Analysis**: The WhatsApp Chat Analyzer provides both overall analysis of the entire chat as well as individual analysis for specific users. Users can choose to view insights for the entire conversation or select individual users to analyze their contributions separately.
- **Frequency Analysis**: Counts the number of messages, words, links, and media shared in the chat.
- **User Activity**: Identifies the most active users and their percentage contribution to the conversation.
- **Word Cloud**: Generates a word cloud from the most frequently used words.
- **Emoji Analysis**: Counts and analyzes the usage of emojis in the conversation.
- **Sentiment Analysis**: Provides sentiment analysis of messages to identify positive, negative, and neutral sentiments.
- **Topic Modeling**: Identifies important topics discussed in the chat.
- **Conversation Dates**: Users can input the start and end dates of the conversation in the sidebar. Based on these dates, sentiment analysis and important topics for the conversation between the specified dates are displayed.
