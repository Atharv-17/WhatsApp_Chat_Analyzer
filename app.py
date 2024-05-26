import streamlit as st
import preprocessor, analysis_Funcs
import matplotlib.pyplot as plt


st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)


    #ffetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('grp_notification')
    user_list.sort()
    user_list.insert(0,"overall")

    selected_user=st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

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

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = analysis_Funcs.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical');
        st.pyplot(fig)

        #dailt timeline
        st.title("Daily Timeline")
        daily_df = analysis_Funcs.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_df['only_dates'], daily_df['message'], color='black')
        plt.xticks(rotation='vertical');
        st.pyplot(fig)

        #activity  map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = analysis_Funcs.week_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most busy Month")
            busy_month = analysis_Funcs.monthly_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.barh(busy_month.index, busy_month.values, color='yellow')
            st.pyplot(fig)


        #most busy member in group

        if selected_user == 'overall':
            st.title('Most active users')
            x,new_df=analysis_Funcs.most_active_user(df)
            fig, ax = plt.subplots()


            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        #WordCloud
        st.title("Word Cloud")
        df_wc=analysis_Funcs.create_worldcloud(selected_user,df)
        fig, ax= plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df=analysis_Funcs.most_common_words(selected_user,df)
        st.title("Most common words")
        fig, ax =plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji analysis
        emoji_df=analysis_Funcs.emoji_helper(selected_user,df)
        st.title("Emojis Used")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax =plt.subplots()
            ax.pie( emoji_df[1][:11],labels=emoji_df[0][:11], autopct="%0.2f")
            st.pyplot(fig)
