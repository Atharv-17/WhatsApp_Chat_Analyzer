from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import re


extractor = URLExtract()
def fetch_stats(selected_user, df):
    if (selected_user != "overall"):
        df = df[df['user'] == selected_user]
    #no of mssgs
    num_mssg = df.shape[0]

    #no of words
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    word_len = len(words)

    #no of media mssgs
    noof_media_mssg=df[df['message']=='<Media omitted>\n'].shape[0]

    #no on links

    links = []

    for mssg in df['message']:
        links.extend(extractor.find_urls(mssg))

    return num_mssg, word_len, noof_media_mssg, len(links)


def most_active_user(df):
    x = df['user'].value_counts().head()
    dt=(round(df['user'].value_counts()/df.shape[0]*100,2)).reset_index().rename(columns={'percent':'name', 'count':'percent'})
    return x, dt


def create_worldcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if (selected_user != "overall"):
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'grp_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']


    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc= wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words= f.read()


    if (selected_user != "overall"):
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'grp_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)


    most_common_df = pd.DataFrame(Counter(words).most_common(25))
    return most_common_df


def emoji_helper(selected_user,df):
    if (selected_user != "overall"):
        df = df[df['user'] == selected_user]

    emo_list = []

    for msg in df['message']:
        emozi = re.findall(r'[^\w\s,.!*&@#~$%*?+-<>|=\'"(\)"’"]', msg)
        emo_list.extend(emozi)
    emo = Counter(emo_list).most_common(len(Counter(emo_list)))
    emo_df = pd.DataFrame(emo)
    return emo_df


def monthly_timeline(selected_user, df):
    if (selected_user != "overall"):
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if (selected_user != "overall"):
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_dates').count()['message'].reset_index()
    return daily_timeline


def week_activity(selected_user, df):

    if (selected_user != "overall"):
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity(selected_user, df):

    if (selected_user != "overall"):
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


