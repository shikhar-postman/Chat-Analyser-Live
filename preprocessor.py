import pandas as pd
import re
import streamlit as st


def startsWithDateAndTime(s):
    pattern = '^([0-9]+)(/)([0-9]+)(/)([0-9][0-9]), ([0-9]+):([0-9][0-9]) [AaPp][Mm] -'
    result = re.match(pattern, s)
    if result:
        return True
    return False

def FindAuthor(s):
    patterns = [
        '([\w]+):',                        # First Name
        '([\w]+[\s]+[\w]+):',              # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([\w]+)[\u263a-\U0001f999]+:',    # Name and Emoji    
        '([+]d{2} d{5} d{5}):',            # Mobile No. (India)
        '([+]d{2} d{3} d{3} d{4}):'        # Mobile No. (US)
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

def getDataPoint(line):   
    splitLine = line.split(' - ') 
    dateTime = splitLine[0]
    date, time = dateTime.split(', ') 
    message = ' '.join(splitLine[1:])
    # print(line)
    # print(date)
    if FindAuthor(message): 
        splitMessage = message.split(':') 
        author = splitMessage[0] 
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message

def check_dataframe(df):
    ### Checking shape of dataset.
    df.shape
    ### Checking basic information of dataset
    df.info()
    ### Checking no. of null values in dataset
    df.isnull().sum()
    ### Checking head part of dataset
    df.head(50)
    ### Checking tail part of dataset
    df.tail(50)
    ### Droping Nan values from dataset
    df = df.dropna()
    df = df.reset_index(drop=True)
    df.shape
    ### Checking no. of authors of group
    df['Author'].nunique()
    ### Checking authors of group
    df['Author'].unique()


def preprocess(data):
    parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe    
    messageBuffer = [] 
    date, time, author = None, None, None
    f = 0
    for line in data.splitlines():
        f = f + 1
        ### Skipping first line of the file because contains information related to something about end-to-end encryption
        if f==1:
            continue
        # line = line.strip() 
        if startsWithDateAndTime(line): 
            if len(messageBuffer) > 0: 
                parsedData.append([date, time, author, ' '.join(messageBuffer)]) 
            messageBuffer.clear() 
            date, time, author, message = getDataPoint(line) 

            messageBuffer.append(message) 
        else:
            messageBuffer.append(line)


    df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message']) # Initialising a pandas Dataframe.
    # print(df['Author'].unique())
    ### To download the created Dataframe
    temp_df = df
    temp_df.to_csv('Download.csv')
    st.download_button('Download Chat CSV','Download.csv')  # Defaults to 'text/plain'
    
    
    # check_dataframe(df)
    ## changing datatype of "Date" column.
    df["Date"] = pd.to_datetime(df["Date"],dayfirst=True)

    # ### Adding one more column of "Day" for better analysis, here we use datetime library which help us to do this task easily.
    # weeks = {
    # 0 : 'Monday',
    # 1 : 'Tuesday',
    # 2 : 'Wednesday',
    # 3 : 'Thrusday',
    # 4 : 'Friday',
    # 5 : 'Saturday',
    # 6 : 'Sunday'
    # }
    # df['Day'] = df['Date'].dt.weekday.map(weeks)
    # ### Rearranging the columns for better understanding
    # df = df[['Date','Day','Time','Author','Message']]
    # ### Changing the datatype of column "Day".
    # df['Day'] = df['Day'].astype('category')
    # ### Looking newborn dataset.
    # df.head()
    df['Only_Date'] = df['Date'].dt.date
    df['Year'] = df['Date'].dt.year
    df['Month_num'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    period = []
    for hour in df[['Day_Name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['Period'] = period

    return df


    ### message buffer is used for messages with line gaps. Long messages like 
    # Chip rate:The number of chips (bits) in the spreading signal is significantly greater than the data bits. Chip rate is measured in "megachips per second" (Mcps), which is millions of chips per second.
    # Hint: related to Bit Error Rate (BER) and Signal Noise Ration (SNR), file attachment allowed in this question.
    ## the above two messages are sent by the same user but are seperated by a '\n' so message buffer store the last messages, so that they both
    ## correspond to the same user.

