import re
import pandas as pd

# read file
with open("chat.txt", encoding="utf-8") as f:
    data = f.read()

# pattern for splitting messages
pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}.*? - '

messages = re.split(pattern, data)[1:]
dates = re.findall(pattern, data)

# create dataframe
df = pd.DataFrame({'message_date': dates, 'user_message': messages})

# extract user + message
users = []
msgs = []

for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s', message)
    if len(entry) > 1:
        users.append(entry[1])
        msgs.append(entry[2])
    else:
        users.append('group_notification')
        msgs.append(entry[0])

df['user'] = users
df['message'] = msgs

print(df.head())


user_counts = df['user'].value_counts()
print(user_counts)