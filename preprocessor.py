def preprocess(data):
    pattern = pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2}\s?[APM]*)\] (.*?): (.*)$'

    # Extract all parts from data
split_data = re.split(pattern, data, flags=re.MULTILINE)

with open("C:\wp chat\_chat.txt", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

# The sender names appear every 4th element, and messages appear every 5th element
senders = split_data[3::5]  # Extract sender names
messages = split_data[4::5]  # Extract messages

# Print sender with their message
for sender, msg in zip(senders, messages):
    print(f"{sender}: {msg}")

    
# Extract all matches from data
matches = re.findall(pattern, data, re.MULTILINE)

# Extract dates and times
dates_times = [(match[0], match[1]) for match in matches]  # match[0] = date, match[1] = time

# Print the dates and times
for date, time in dates_times:
    print(f"Date: {date}, Time: {time}")

import pandas as pd
import re

# Assuming 'data' is the raw chat data



# Extract all matches from data
matches = re.findall(pattern, data, re.MULTILINE)

# Create lists to store messages and dates
messages = []
dates = []

# Extract messages and dates from matches
for match in matches:
    dates.append(match[0])  # Date is the first capture group
    messages.append(match[3])  # Message is the fourth capture group

# Create DataFrame
df = pd.DataFrame({'user_message': messages, 'message_date': dates})

# Convert date column to datetime format
df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y') # Adjusted format

# Rename column
df.rename(columns={'message_date': 'date'}, inplace=True)

# Extract messages and dates using regex
pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}:\d{2}\s?[APM]*)\] (.*?): (.*)$'
matches = re.findall(pattern, data, re.MULTILINE)

# Create lists to store extracted data
dates = [match[0] for match in matches]
times = [match[1] for match in matches]
users = [match[2] for match in matches]
messages = [match[3] for match in matches]

# Create DataFrame with extracted data
df = pd.DataFrame({'date': dates, 'time': times, 'user': users, 'message': messages})

# Convert 'date' column to datetime objects
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y')

df['month']=df['date'].dt.month_name()
df['day']=df['date'].dt.day

df['hour']=df['date'].dt.hour
df['minute']=df['date'].dt.minute

return df