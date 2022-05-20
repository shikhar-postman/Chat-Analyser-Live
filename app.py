from time import sleep
import streamlit as st
import preprocessor
import os
# os.system('cls||clear')
import helper
import base64
from fpdf import FPDF
import matplotlib.pyplot as plt
import report
from tempfile import NamedTemporaryFile
# from sklearn.datasets import load_iris
st.title("Whatsapp Chat Analyzer")

## adding bootstrap 
st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">""", unsafe_allow_html=True)



uploaded_file = st.sidebar.file_uploader("Choose a file",type=['txt'])
if uploaded_file is not None:
    raw_text = str(uploaded_file.read(),"utf-8")
    df = preprocessor.preprocess(raw_text)
    # st.text(raw_text)

    #fetch unique users

    user_list = df['Author'].unique().tolist()
    if None in user_list:
        user_list.remove(None)
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    # report_pdf = report.create_report(df)
    if st.sidebar.button("Show Analysis"):

        # TOP STATS CARD
        temp_html,links = helper.topstats_table(df,selected_user,0)
        # st.write(df)
        # LINKS CARD
        with st.expander(f"Show links sent by {selected_user}"):
            helper.links_table(links,selected_user)

        # EMOJI CARD
        with st.expander(f"Show Emoji Analysis of {selected_user}"):
            helper.emoji_table(df,selected_user,0)

        # Common Words Card
        with st.expander(f"Show Commonly used words by {selected_user}"):
            helper.most_common_words(df,selected_user,0)
        
        # Monthly timeline 
        with st.expander(f"Show Monthly Timeline Stats of {selected_user}"):
            helper.monthly_timeline(df,selected_user)

        # Week Activity Map
        with st.expander(f"Show Week Activity of {selected_user}"):
            helper.week_activity_map(df,selected_user,0)

        # Daily timeline 
        with st.expander(f"Show Daily Timeline Stats of {selected_user}"):
            helper.daily_timeline(df,selected_user,0)

        # Month Activity Map
        # with st.expander(f"Show Monthy Activity Map of {selected_user}"):
        #     helper.month_activity_map(df,selected_user)
        # # Activity heatmap
        # with st.expander(f"Show Activity Heat Map of {selected_user}"):
        #     helper.activity_heatmap(df,selected_user)


        # with st.expander(f"Sentiment Report"):
        #     helper.find_sentimentreport(df)


        # Group Icon Changed
        with st.expander(f"Show some facts"):
            helper.group_icon_changed(df)


    


    # with open("Download.csv",encoding="utf8") as f:
    #     st.download_button('Download Chat Report', f)  # Defaults to 'text/plain'


    
