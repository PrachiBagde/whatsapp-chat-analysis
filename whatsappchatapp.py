import seaborn as sns
import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

from helper import daily_timeline

st.sidebar.title("Whatsapp Chat Analysis")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()  #-
    data = bytes_data.decode("utf-8")
    df = preprocessor.prepocess(data)

    st.dataframe(df)

    #fetch unique users
    user_list = df["user"].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("show Analysis"):
        num_messages, words, num_media_message, num_links = helper.fetch_stats(selected_user, df )
        st.title("Top Statistic of Whatsapp Chat")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Share")
            st.title(num_media_message)

        with col4:
            st.header("Link Shared")
            st.title(num_links)

    if selected_user == 'Overall':
        st.title("Most Busy Users")
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color = 'red')
            ax.set_xticklabels(x.index,rotation=30)
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

    most_common_df = helper.most_common_words(selected_user,df)

    st.dataframe(most_common_df)

    fig,ax = plt.subplots()

    ax.bar(most_common_df[0],most_common_df[1],color = 'orange')
    plt.xticks(rotation = 'vertical')
    st.title("Most Common Words")
    st.pyplot(fig)

    emoji_df = helper.emoji_helper(selected_user,df)
    st.title("Emoji Analysis")

    col1,col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)

    with col2:
        fig,ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels= emoji_df[0].head(), autopct = "%0.2f")
        st.pyplot(fig)

    st.title("Monthly Timeline Analysis")
    timeline = helper.monthly_timeline(selected_user,df)

    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'])
    plt.xticks(rotation='vertical')
    plt.figure(figsize=(35,6))
    st.pyplot(fig)

    #Daily Timeline

    st.title("Daily Timeline Analysis")
    daily_timeline = helper.daily_timeline(selected_user,df)

    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'],daily_timeline['message'], color = 'green')
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)

    st.title("Acitivity Map")
    col1 ,col2 = st.columns(2)

    with col1:
        st.header("Most Busy Day")
        busy_day = helper.weekly_activity_map(selected_user,df)

        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values,color = 'purple')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

    with col2:
        st.header("Most Busy Month")
        busy_month = helper.monthly_activity_map(selected_user,df)

        fig,ax = plt.subplots()
        ax.bar(busy_month.index,busy_month.values,color = 'magenta')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

    st.title("Online Activity Map")
    user_heatmap = helper.activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)