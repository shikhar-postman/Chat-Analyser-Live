import emoji
import streamlit as st
import re
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
from plotnine import *
import itertools 
import altair as alt
import datetime
from datetime import date
import calendar
import seaborn as sns
import json
from json import dumps
import numpy as np
import pdfkit
from altair_saver import save
from fpdf import FPDF
import base64
# from fpdf import FPDF

# from wordcloud import WordCloud

# import streamlit_wordcloud as WordCloud

# Load Apple Color Emoji font 
prop = FontProperties(fname='/System/Library/Fonts/Apple Color Emoji.ttc')

def findDay(date):
    date = str(date)
    year, month, day = (int(i) for i in date.split('-'))   
    born = datetime.date(year, month, day)
    return born.strftime("%A")
 

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['Author'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['Message']:
        words.extend(message.split())

    num_media_msgs = df[df['Message'] == ' <Media omitted>'].shape[0]

    links = []
    URLPATTERN = re.compile(r'https:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}')
    for message in df['Message']:
        link = URLPATTERN.search(message)
        if link is None:
            continue
        links.append(link.group())
    # for message in df['Message']:
    #     links.extend(URLExtract.find_urls(message))
    return num_messages, len(words), num_media_msgs, links

def links_table(links,author):
    st.write("Total links shared: ",len(links))
    if len(links):
        st.markdown(f"""

        <p>Links shared by <strong>{author}</strong></p>

        """,unsafe_allow_html=True)

    for link in links:
        if link[0]=='w':
            link = "https://" + link
        st.markdown(f"""
            <div class="card">
                <ul>
                    <li><a href={link}>{link}</a></li>
                </ul>
            </div>
        """,unsafe_allow_html=True)

    
def topstats_table(df,author,report):
    total_messages, total_words,total_media,links = fetch_stats(author, df)
    total_links = len(links)

    temp_html = f"""
            <div class="table-responsive" >
                <h4>Top Stats of {author}</h4>
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th scope="col text-justify" class="text-center">Total Messages</th>
                            <th scope="col" class="text-center">Total Words</th>
                            <th scope="col" class="text-center">Total Media</th>
                            <th scope="col" class="text-center">Total Links</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="table-secondary">
                            <th class="text-center">{total_messages}</th>
                            <td class="text-center">{total_words}</td>
                            <td class="text-center">{total_media}</td>
                            <td class="text-center">{total_links}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        """
    st.markdown(temp_html, unsafe_allow_html=True)
    temp_html2 = f"""
    <div class="card">
        <ul>
            <p>op Stats of {author}</p>
            <li>Total Messages : {total_messages} </li>
            <li>Total words : {total_words} </li>
            <li>Total Media Sent : {total_media} </li>
            <li>Total Links Sent : {total_links} </li>
        </ul>
    </div>
    """
    return temp_html2,links

# def create_word_cloud(selected_user,df):

#     f = open('stop_hinglish.txt', 'r')
#     stop_words = f.read()

#     if selected_user != 'Overall':
#         df = df[df['Author'] == selected_user]

#     temp = df[df['Author'] != 'group_notification']
#     temp = temp[temp['Message'] != ' <Media omitted>\n']

#     def remove_stop_words(message):
#         y = []
#         for word in message.lower().split():
#             if word not in stop_words:
#                 y.append(word)
#         return " ".join(y)

#     wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
#     temp['Message'] = temp['Message'].apply(remove_stop_words)
#     df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
#     return df_wc


def monthly_timeline(df,selected_user):

    if selected_user != 'Overall':
        df = df[df['Author'] == selected_user]

    timeline = df.groupby(['Year', 'Month_num', 'Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['Time'] = time
    # st.write(timeline)
    ### Naive code to find the max mess month
    # idx = timeline['Message'].idxmax()
    # st.write(df.iloc[idx])
    
    maxx_mssg = 0
    maxx_idx = 0

    minn_mssg = 400000
    minn_idx = 0
    for idx in timeline.index:
        if timeline['Message'][idx] > maxx_mssg:
            maxx_mssg = timeline['Message'][idx]
            maxx_idx = idx 
        if timeline['Message'][idx] < minn_mssg:
            minn_mssg = timeline['Message'][idx]
            minn_idx = idx

    # st.write(maxx_idx)
    mostactive_month = timeline['Month'][maxx_idx]
    mostactive_year = timeline['Year'][maxx_idx]

    leastactive_month = timeline['Month'][minn_idx]
    leastactive_year = timeline['Year'][minn_idx]

    # st.header(f"Least Active Month was {leastactive_month} in {leastactive_year} with a total of {minn_mssg} messages.")
    # Most Active Month with Year
    st.markdown(f"""
            <div>
                <br>
                <p>Here are some important facts:</p>
                <ul>
                    <li>Most Active Month of <strong>{selected_user}</strong> was <strong>{mostactive_month}</strong> in <strong>{mostactive_year}</strong> with a total of <strong>{maxx_mssg}</strong> messages.</li>
                    <br/>
                    <li>Least Active Month of <strong>{selected_user}</strong> was <strong>{leastactive_month}</strong> in <strong>{leastactive_year}</strong> with a total of <strong>{minn_mssg}</strong> messages.</li>
                    <br/>
                </ul>
            </div>
        """,unsafe_allow_html=True)

    st.write(timeline)
    st.write(f"Monthly Timeline of {selected_user}")
    fig,ax = plt.subplots()
    ax.plot(timeline['Time'], timeline['Message'],color='green')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    # return timeline


def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

def daily_timeline(df,selected_user,report):

    if selected_user != 'Overall':
        df = df[df['Author'] == selected_user]

    daily_timeline = df.groupby('Only_Date').count()['Message'].reset_index()
    # st.write(daily_timeline)

    maxx_mssg = 0
    maxx_idx = 0
    for idx in daily_timeline.index:
        if daily_timeline['Message'][idx] > maxx_mssg:
            maxx_mssg = daily_timeline['Message'][idx]
            maxx_idx = idx 
    
    mostactive_day = daily_timeline['Only_Date'][maxx_idx]

    minn_mssg = 400000
    minn_idx = 0
    for idx in daily_timeline.index:
        if daily_timeline['Message'][idx] < minn_mssg:
            minn_mssg = daily_timeline['Message'][idx]
            minn_idx = idx 
    
    leastactive_day = daily_timeline['Only_Date'][minn_idx]
    mostactive_weekday = findDay(mostactive_day)
    leastactive_weekday = findDay(leastactive_day)
    if report==0:
        st.markdown(f"""
            <div>
                <br>
                <p>Here are some interesting facts:</p>
                <ul>
                    <li>Most Active Day of <strong>{selected_user}</strong> was <strong>{mostactive_day} ({mostactive_weekday})</strong> with a total of <strong>{maxx_mssg}</strong> messages.</li>
                    <li>Least Active Day of <strong>{selected_user}</strong> was <strong>{leastactive_day} ({leastactive_weekday})</strong> with a total of <strong>{minn_mssg}</strong> messages.</li>
                    <br/>
                </ul>
            </div>
        """,unsafe_allow_html=True)
    # daily timeline
    daily_timeline.columns = ['Date','Messages']
    
    daily_timeline['Date'] = daily_timeline['Date'].astype(str)


    
    c = alt.Chart(daily_timeline).mark_circle().encode(
            color='Messages',
            y=alt.Y('Date',sort='-x'),
            x='Messages',
            tooltip = ['Date','Messages']
        ).properties(
            title = 'Daily Activity'
        ).configure_mark(
            opacity=1,
            # color='red'
        )     
    if report==0:
        st.write("Below is the Week Activity chart of ",selected_user)
        st.altair_chart(c, use_container_width=True)

    c.save('chart.png')
    

    # pdfkit.from_file('simple.html', 'out2.pdf')
    # st.write("\n")
    # st.write(f"Daily Timeline of {selected_user}")
    # fig, ax = plt.subplots()
    # ax.plot(daily_timeline['Only_Date'], daily_timeline['Message'], color='orange')
    # plt.xticks(rotation='vertical')
    # st.pyplot(fig)
    # return daily_timeline

def week_activity_map(df,selected_user,report):

    if selected_user != 'Overall':
        df = df[df['Author'] == selected_user]

    busy_day = df['Day_Name'].value_counts()
    # st.write(busy_day['Monday'])
    maxx_mssg = 0
    most_busyday = ""
    minn_mssg = 400000
    least_busyday = ""

    f = 0  # temp
    for day in busy_day.index:
        if f==0:
            most_busyday = day 
            maxx_mssg = busy_day[day]
        
        f = f + 1
        least_busyday = day
        minn_mssg = busy_day[day]

    
    if report==0:
        st.markdown(f"""
            <div>
                <br>
                <p>Here are some important facts:</p>
                <ul>
                    <li>Most Weekly Active Day of <strong>{selected_user}</strong> was <strong>{most_busyday}</strong> with a collective total of <strong>{maxx_mssg}</strong> messages.</li>
                    <li>Least Weekly Active Day of <strong>{selected_user}</strong> was <strong>{least_busyday}</strong> with a collective total of <strong>{minn_mssg}</strong> messages.</li>
                    <br/>
                </ul>
            </div>
        """,unsafe_allow_html=True)
    

    # st.write("Most busy day")
    # fig,ax = plt.subplots()
    # ax.bar(busy_day.index,busy_day.values,color='purple')
    # plt.xticks(rotation='vertical')
    # st.pyplot(fig)
    
    # st.write(df.head(5))\
    busy_day = busy_day.reset_index(level=0)
    busy_day.columns = ['Day','Message']
    # st.write(busy_day)

    
    c = alt.Chart(busy_day).mark_bar().encode(
            color='Message',
            y=alt.Y('Day',sort='-x'),
            x='Message',
            tooltip = ['Day','Message']
        ).properties(
            title = 'Weekly Activity'
        ).configure_mark(
            opacity=1,
            # color='red'
        )     
    if f==0:
        st.write("Below is the Week Activity chart of ",selected_user)
        st.altair_chart(c, use_container_width=True)
    c.save('week_activity_map.png')
    # st.write(busy_day)
    # c = alt.Chart(busy_day.reset_index()).mark_line().encode(
    #     x='index:T',
    #     y='Day_Name:Q',
    # )
    # st.altair_chart(c, use_container_width=True)
    # return df['Day_Name'].value_counts()

def month_activity_map(df,selected_user):

    if selected_user != 'Overall':
        df = df[df['Author'] == selected_user]

    st.write("Most busy Month")
    busy_day = df['Month'].value_counts()
    fig,ax = plt.subplots()
    ax.bar(busy_day.index,busy_day.values,color='purple')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    # return df['month'].value_counts()

def activity_heatmap(df,selected_user):

    if selected_user != 'Overall':
        df = df[df['Author'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_Name', columns='Period', values='Message', aggfunc='count').fillna(0)
    st.write("Weekly Activity Map")
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    st.pyplot(fig)
    # return user_heatmap


def most_common_words(df,selected_user,report):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Author'] == selected_user]

    temp = df[df['Author'] != 'group_notification']
    temp = temp[temp['Message'] != ' <Media omitted>']

    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words and len(word)>2:
                words.append(word)



    # most_common_df = pd.DataFrame(Counter(words).most_common(20))
    # # st.title("Most Common Words")
    # # # most_common_df = helper.most_common_words(selected_user, df)
    # # fig, ax = plt.subplots()
    # # ax.barh(most_common_df[0], most_common_df[1])
    # # plt.xticks(rotation='vertical')
    # # st.pyplot(fig)
    # st.write(most_common_df)
    # most_common_df[0] = most_common_df[0].astype(str)
    # most_common_df[1] = most_common_df[1].astype(str)

    unique_words = set(words)
    count_words = dict.fromkeys(unique_words, 0)

    for w in words:
        count_words[w] = count_words[w] + 1
    
    # for e in unique_words:
        # print(e,count_words[e])
    count_words = {key: value for key, value in sorted(count_words.items(), key=lambda item: item[1],reverse=True)}
    # count_words = dict((v,k) for k,v in count_words.items())
    # count_words = dict(itertools.islice(count_words.items(), 20)) 
    words_df = pd.DataFrame.from_dict(count_words,orient ='index',columns=['Word Count'])
    words_df['Word'] = words_df.index


    # st.write(words_df)
    # st.bar_chart(words_df)
    # alt.Chart(words_df).mark_point().encode(
    #     color='msg_count',
    #     y='index',
    #     x='msg_count'
    # )

    if report==0:
        st.markdown(f"""
            <div>
                <br>
                <p>Here are some important facts:</p>
                <ul>
                <p> Top 5 most used words by {selected_user} are:
                    <li><strong>{words_df['Word'][0]}</strong> used <strong>{words_df['Word Count'][0]}</strong> times.</li>
                    <li><strong>{words_df['Word'][1]}</strong> used <strong>{words_df['Word Count'][2]}</strong> times.</li>
                    <li><strong>{words_df['Word'][3]}</strong> used <strong>{words_df['Word Count'][3]}</strong> times.</li>
                    <li><strong>{words_df['Word'][4]}</strong> used <strong>{words_df['Word Count'][4]}</strong> times.</li>
                    <li><strong>{words_df['Word'][5]}</strong> used <strong>{words_df['Word Count'][5]}</strong> times.</li>
                </ul>
            </div>
        """,unsafe_allow_html=True)
    
    
    c = alt.Chart(words_df.head(20)).mark_bar().encode(
            color='Word Count',
            y=alt.Y('Word',sort='-x'),
            x='Word Count',
            tooltip = ['Word','Word Count']
        ).properties(
            title = 'Word Frequency Chart'
        ).configure_mark(
            opacity=1,
            # color='red'
        )     
    if report==0:
        st.write("Below is the word frequency chart of ",selected_user)
        st.altair_chart(c, use_container_width=True)
    c.save('word_chart.png')
    # return most_common_df

def emoji_table(df,selected_user,report):
    if selected_user != 'Overall':
        df = df[df['Author'] == selected_user]
    emojis = []
    for message in df['Message']:
        for c in message:
            if c in emoji.UNICODE_EMOJI['en']:
                emojis.append(c)
        # if any(char in emoji.UNICODE_EMOJI['en'] for char in message):
        #     print(message)
        #     emojis.append(message)
    # emoji_df = pd.DataFrame(Counter(emojis).most_common(20))
    # print(emojis)
    unique_emojis = set(emojis)
    count_emojis = dict.fromkeys(unique_emojis, 0)

    for e in emojis:
        count_emojis[e] = count_emojis[e] + 1
    
    # for e in unique_emojis:
        # print(e,count_emojis[e])
    count_emojis = {key: value for key, value in sorted(count_emojis.items(), key=lambda item: item[1],reverse=True)}
    count_emojis = dict(itertools.islice(count_emojis.items(), 10)) 
    emoji_df = pd.DataFrame.from_dict(count_emojis,orient ='index',columns=['Emoji Count'])
    # st.bar_chart(emoji_df)
    # st.write(emoji_df)
    emoji_df['Emoji'] = emoji_df.index
    
    c = alt.Chart(emoji_df.head(20)).mark_bar().encode(
            color='Emoji Count',
            # y='Emoji',
            y=alt.Y('Emoji', sort='-x'),
            x='Emoji Count',
            tooltip = ['Emoji','Emoji Count']
        ).properties(
            title = 'Emoji Frequency Chart'
        ).configure_mark(
            opacity=1,
            # color='red'
        )  
    if report==0:
        st.write("Below is the emoji frequency chart of ",selected_user)   
        st.altair_chart(c, use_container_width=True)

    c.save('emoji_chart.png')
    # Horizontal stacked bar chart
    # data = pd.melt(emoji_df.reset_index(), id_vars=["index"])
    # chart = (
    #     alt.Chart(data)
    #     .mark_bar()
    #     .encode(
    #         x=alt.X("value", type="quantitative", title=""),
    #         y=alt.Y("index", type="nominal", title=""),
    #         color=alt.Color("variable", type="nominal", title=""),
    #         order=alt.Order("variable", sort="descending"),
    #     )
    # )
    # st.altair_chart(chart, use_container_width=True)


    #emoji analysis
    # emoji_df = helper.emoji_helper(selected_user, df)
    # st.title("Emojis Analysis")
    # cnt = 0
    # for key,value in count_emojis.items():
    #     if cnt>=5:
    #         break
    #     cnt = cnt + 1
    #     st.markdown(f"""
    #         <div class="card">
    #             <ul>
    #                 <li>{key} : {value}</li>
    #             </ul>
    #         </div>
    #     """,unsafe_allow_html=True)
    # st.write(emoji_df)
    # col1, col2 = st.columns(2)

    # with col1:
    #     st.dataframe(emoji_df)
    # with col2:
    #     fig, ax = plt.subplots()
    #     ax.pie(emoji_df[1].head(), labels = emoji_df[0].head(), autopct = "%0.2f")
    #     st.pyplot(fig)
    # return emoji_df 
# def top_emoji(df,author):







### For Top Stats Card, use the below code:

"""
    <div class="card" style="margin:1rem;">
        <div class="card-body">
            <h2 class="card-title">Top Statistics of {author}</h5>
            <h4 class="card-subtitle mb-2 text-muted">Total Messages --> {total_messages}</h6>
            <h4 class="card-subtitle">Total words--> {total_words}</p>
        </div>
    </div>

"""


# def find_sentimentreport(df):
    


def group_icon_changed(df):
    cnt = 0
    s = "changed this group's icon"
    for message in df['Message']:
        cnt = cnt + message.count(s)

    st.write("Group Icon changed a total of",cnt,"times.")