import re
import pandas as pd
import matplotlib.pyplot as plt
import emoji
from collections import Counter

# ------------------ READ FILE ------------------
with open("chat.txt", encoding="utf-8") as f:
    data = f.read()

# ------------------ CLEAN DATA ------------------
pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}.*? - '

messages = re.split(pattern, data)[1:]
dates = re.findall(pattern, data)

df = pd.DataFrame({'message_date': dates, 'user_message': messages})

# ------------------ USER + MESSAGE ------------------
users = []
msgs = []

for message in df['user_message']:
    entry = re.split(r'([\w\W]+?):\s', message)  # fixed warning with r''
    if len(entry) > 1:
        users.append(entry[1])
        msgs.append(entry[2])
    else:
        users.append('group_notification')
        msgs.append(entry[0])

df['user'] = users
df['message'] = msgs

# ------------------ DATE FORMATTING ------------------
df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
df['hour'] = df['message_date'].dt.hour
df['day'] = df['message_date'].dt.day_name()

# ------------------ BASIC INFO ------------------
print("\n📊 DATA PREVIEW:")
print(df.head())

# ------------------ MOST ACTIVE USERS ------------------
print("\n🔥 Most Active Users:")
user_counts = df['user'].value_counts()
print(user_counts)

# ------------------ USER BAR GRAPH ------------------
user_counts.head().plot(kind='bar', title="Most Active Users")
plt.xlabel("Users")
plt.ylabel("Messages")
plt.show()

# ------------------ ACTIVITY BY HOUR ------------------
hour_counts = df['hour'].value_counts().sort_index()

plt.plot(hour_counts.index, hour_counts.values)
plt.title("Activity by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Messages")
plt.show()

# ------------------ MOST COMMON WORDS ------------------
words = []
for message in df['message']:
    for word in message.lower().split():
        words.append(word)

common_words = Counter(words)
print("\n💬 Most Common Words:")
print(common_words.most_common(10))

# ------------------ EMOJI ANALYSIS ------------------
emojis = []
for message in df['message']:
    for char in message:
        if char in emoji.EMOJI_DATA:
            emojis.append(char)

emoji_counts = Counter(emojis)

print("\n😂 Top Emojis:")
print(emoji_counts.most_common(10))

# ------------------ EMOJI GRAPH ------------------
top_emojis = emoji_counts.most_common(5)

if top_emojis:
    e = [i[0] for i in top_emojis]
    c = [i[1] for i in top_emojis]

    plt.bar(e, c)
    plt.title("Top Emojis Used")
    plt.show()

