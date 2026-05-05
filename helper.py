from collections import Counter
import pandas as pd
import re
import emoji
from wordcloud import WordCloud


# ---------------- STATS ----------------
def fetch_stats(user, df):

    if user != "Overall":
        df = df[df['user'] == user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())

    num_words = len(words)

    num_media_messages = df[df['message'] == "<Media omitted>"].shape[0]

    links = []
    for message in df['message']:
        links.extend(re.findall(r'http\S+', message))

    return num_messages, num_words, num_media_messages, len(links)


# ---------------- MOST BUSY USERS ----------------
def most_busy_users(df):

    x = df['user'].value_counts().head()

    new_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    new_df.columns = ['user', 'percent']

    return x, new_df


# ---------------- EMOJI ANALYSIS ----------------
def emoji_helper(df):

    emojis = []

    for message in df['message']:
        for char in message:
            if char in emoji.EMOJI_DATA:
                emojis.append(char)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])

    return emoji_df


# ---------------- WORDCLOUD ----------------
def create_wordcloud(user, df):

    if user != "Overall":
        df = df[df['user'] == user]

    text = " ".join(df['message'])

    wc = WordCloud(width=500, height=500, background_color="white").generate(text)

    return wc


# ---------------- MOST COMMON WORDS ----------------
def most_common_words(user, df):

    if user != "Overall":
        df = df[df['user'] == user]

    words = []

    for message in df['message']:
        words.extend(message.lower().split())

    common_words = Counter(words).most_common(20)

    return zip(*common_words)


# ---------------- MONTHLY TIMELINE ----------------
def monthly_timeline(user, df):

    if user != "Overall":
        df = df[df['user'] == user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i]) + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


# ---------------- DAILY TIMELINE ----------------
def daily_timeline(user, df):

    if user != "Overall":
        df = df[df['user'] == user]

    daily = df.groupby('message_date').count()['message'].reset_index()

    return daily