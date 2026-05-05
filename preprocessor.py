import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}.*? - '

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'message_date': dates, 'user_message': messages})

    users = []
    msgs = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)

        if len(entry) > 1:
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append("group_notification")
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs

    # convert datetime
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%d/%m/%y, %I:%M %p - ',
        errors='coerce'
    )

    # IMPORTANT FEATURE COLUMNS (needed for graphs)
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df['month_num'] = df['message_date'].dt.month
    df['day'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['only_date'] = df['message_date'].dt.date

    return df