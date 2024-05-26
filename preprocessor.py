import pandas as pd
import re

def preprocess(data):
    pat = '\d{1,2}\/\d{1,2}\/\d{1,2},\s\d{1,2}:\d{1,2}\s[AP]M\s-\s'
    dates = re.findall(pat, data)

    cleaned_dates = [s.replace('\u202f', ' ') for s in dates]

    mssgs = re.split(pat, data)[1:]

    df = pd.DataFrame({'user_message': mssgs, 'message_date': cleaned_dates})

    df['msg_dates'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')


    df = df.drop('message_date', axis=1)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            # if colan : not present
            users.append('grp_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['msg_dates'].dt.year
    df['month_num'] = df['msg_dates'].dt.month
    df['only_dates'] = df['msg_dates'].dt.date
    df['day_name'] = df['msg_dates'].dt.day_name()
    df['month'] = df['msg_dates'].dt.month_name()
    df['day'] = df['msg_dates'].dt.day
    df['hour'] = df['msg_dates'].dt.hour
    df['minute'] = df['msg_dates'].dt.minute

    return df