import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("WhatsApp Chat Analyzer 📊")

st.sidebar.title("Controls")

uploaded_file = st.sidebar.file_uploader("Upload Chat File")

if uploaded_file is not None:

    data = uploaded_file.getvalue().decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.insert(0, "Overall")

    user = st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Show Analysis"):

        # STATS
        stats = helper.fetch_stats(user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Messages", stats[0])
        with col2:
            st.metric("Words", stats[1])
        with col3:
            st.metric("Media", stats[2])
        with col4:
            st.metric("Links", stats[3])

        # MONTHLY TIMELINE
        st.subheader("Monthly Timeline")

        timeline = helper.monthly_timeline(user, df)

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')

        plt.xticks(rotation=90)
        st.pyplot(fig)