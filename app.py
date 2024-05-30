import streamlit as st
import preprocessor, analysis_Funcs, sentiment_analysis
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'data' not in st.session_state:
    st.session_state.data = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'selected_user' not in st.session_state:
    st.session_state.selected_user = "overall"
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False
if 'show_sentiment_analysis' not in st.session_state:
    st.session_state.show_sentiment_analysis = False
if 'Show_Imp_Topics_discussed' not in st.session_state:
    st.session_state.Show_Imp_Topics_discussed = False

# Set up the sidebar and main interface
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    st.session_state.uploaded_file = uploaded_file
    bytes_data = uploaded_file.getvalue()
    st.session_state.data = bytes_data.decode("utf-8")
    st.session_state.df = preprocessor.preprocess(st.session_state.data)

if st.session_state.df is not None:
    df = st.session_state.df

    # Fetch unique users and prepare user selection
    user_list = df['user'].unique().tolist()
    if 'grp_notification' in user_list:
        user_list.remove('grp_notification')
    user_list.sort()
    user_list.insert(0, "overall")

    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list,
                                         index=user_list.index(st.session_state.selected_user))
    st.session_state.selected_user = selected_user

    if st.sidebar.button("Show Analysis"):
        st.session_state.show_analysis = True

    if st.session_state.show_analysis:
        # Fetch and display statistics
        num_mssg, words, noof_media_mssg, noof_links = analysis_Funcs.fetch_stats(selected_user, df)
        st.title("Top Stats")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_mssg)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media Messages")
            st.title(noof_media_mssg)
        with col4:
            st.header("Links Shared")
            st.title(noof_links)

        # Monthly timeline
        st.title("Monthly Timeline")
        timeline = analysis_Funcs.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_df = analysis_Funcs.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_df['only_dates'], daily_df['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = analysis_Funcs.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = analysis_Funcs.monthly_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(busy_month.index, busy_month.values, color='yellow')
            st.pyplot(fig)

        # Most active users
        if selected_user == 'overall':
            st.title('Most Active Users')
            x, new_df = analysis_Funcs.most_active_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Word Cloud")
        df_wc = analysis_Funcs.create_worldcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words
        most_common_df = analysis_Funcs.most_common_words(selected_user, df)
        st.title("Most Common Words")
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji analysis
        emoji_df = analysis_Funcs.emoji_helper(selected_user, df)
        st.title("Emojis Used")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1][:11], labels=emoji_df[0][:11], autopct="%0.2f")
            st.pyplot(fig)


        # Sentiment Analysis
        st.title("Sentiment Analysis")
        st.divider()
        st.markdown("Enter the  starting and Ending dates of chats you want the sentimental analysis of in the sidebar")
        st.divider()

        start_date = st.sidebar.date_input("Start date", min_value=df['msg_dates'].min(),
                                           max_value=df['msg_dates'].max())
        end_date = st.sidebar.date_input("End date", min_value=df['msg_dates'].min(), max_value=df['msg_dates'].max())

        # Convert start_date and end_date to datetime
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        if st.sidebar.button("Show Sentiment Analysis"):
            st.session_state.show_sentiment_analysis = True

        if st.session_state.show_sentiment_analysis:
            sentiment_df = sentiment_analysis.give_senti_data(selected_user, df, start_date, end_date)
            if sentiment_df is not None:


                senti_score = sentiment_analysis.give_sentiment_score(sentiment_df)
                if(selected_user=='overall'):
                    done_by = 'group'
                else:
                    done_by = selected_user

                if(senti_score>0.02):
                    st.write(f"The Overall Sentiment of the chat over the given dates between {start_date} and {end_date} "
                             f"wrt {done_by} is **__POSITIVE__**")

                elif(senti_score<-0.02):
                    st.write(f"The Overall Sentiment of the chat over the given dates between {start_date} and {end_date} "
                             f"wrt {done_by} is **__NEGATIVE_**")
                else:
                    st.write(f"The Overall Sentiment of the chat over the given dates between {start_date} and {end_date} "
                             f"wrt {done_by} is **__NEUTRAL__**")



                if st.button("Show Imp Topics discussed"):
                    st.session_state.Show_Imp_Topics_discussed = True

                if st.session_state.Show_Imp_Topics_discussed:

                    st.divider()
                    st.write("Few Important topics over this time period were:")
                    topic_df = sentiment_analysis.topic_modelling(sentiment_df)
                    st.dataframe(topic_df)
                    st.divider()


