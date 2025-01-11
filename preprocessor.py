import re
import pandas as pd

def prepocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df = pd.DataFrame({"user_messages" : messages, "messages_date" : dates})
    df['messages_date'] = pd.to_datetime(df['messages_date'], format ='%d/%m/%y, %I:%M %p - ')
    df.rename(columns ={"messages_date": "date"}, inplace = True)
    users = []
    messages = []

    for message in df['user_messages']:
        # Ensure message is a string
        if isinstance(message, str):
            entry = re.split(r'^(.*?):\s', message)
            if len(entry) > 2:  # Valid split
                users.append(entry[1])  # Username
                messages.append(" ".join(entry[2:]))  # Message content
            else:  # Handle group notifications or invalid format
                users.append("group notification")
                messages.append(message)
        else:  # Handle non-string (if any)
            users.append("group notification")
            messages.append("")

    # Ensure lists are populated correctly
    assert len(users) == len(df), "Users list length mismatch!"
    assert len(messages) == len(df), "Messages list length mismatch!"

    # Assign to DataFrame
    df['user'] = users
    df['message'] = messages
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df.drop(columns = ['user_messages'], inplace = True)
    df['day_name'] = df['date'].dt.day_name()
    df['year'] = df['date'].dt.year
    df['month']= df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period
    return df