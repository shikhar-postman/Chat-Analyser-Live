from time import sleep
import streamlit as st
import preprocessor
import helper
import base64
from fpdf import FPDF
import matplotlib.pyplot as plt
import PIL
from tempfile import NamedTemporaryFile
# from sklearn.datasets import load_iris
from fpdf import FPDF, HTMLMixin

class PDF(FPDF, HTMLMixin):
    pass


def create_download_link(val, filename):

    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download Chat Report PDF</a>'


def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


def create_report(df):

    helper.daily_timeline(df,'Overall',1)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 12)
    pdf.cell(180, 10, txt = "Daily Activity Time Series Graph of Overall", 
         ln = 1, align = 'C')
    pdf.image('chart.png', 50, 25, 100, 200)




    helper.week_activity_map(df,'Overall',1)
    pdf.add_page()
    pdf.cell(180, 10, txt = "Week Activity Time Series Graph of Overall", 
         ln = 1, align = 'C')
    # image = PIL.Image.open("week_activity_map.png")
    # width, height = image.size
    pdf.image('week_activity_map.png', 50, 25, 100, 50)




    helper.most_common_words(df,'Overall',1)
    pdf.cell(180, 150, txt = "Word Frequency Graph of Overall", 
         ln = 1, align = 'C')
    pdf.image('word_chart.png', 50, 100, 80, 50)


    pdf.add_page()
    helper.emoji_table(df,'Overall',1)
    pdf.cell(180, 10, txt = "Emoji Frequency Graph of Overall", 
         ln = 1, align = 'C')
    pdf.image('emoji_chart.png', 50, 20, 100, 50)


    html = create_download_link(pdf.output(dest="S"), "testfile")
    st.markdown(html, unsafe_allow_html=True)


    # show_pdf('testfile.pdf')


# df = load_iris(as_frame=True)["data"]


# figs = []

# for col in df.columns:
#     fig, ax = plt.subplots()
#     ax.plot(df[col])
#     st.pyplot(fig)
#     figs.append(fig)

# export_as_pdf = st.button("Export Report")


# if export_as_pdf:
#     pdf = FPDF()
#     for fig in figs:
#         pdf.add_page()
#         with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
#                 fig.savefig(tmpfile.name)
#                 pdf.image(tmpfile.name, 10, 10, 200, 100)
#     html = create_download_link(pdf.output(dest="S"), "testfile")
#     st.markdown(html, unsafe_allow_html=True)