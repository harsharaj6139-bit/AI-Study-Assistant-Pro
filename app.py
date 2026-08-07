# ==========================================
# AI Study Assistant Pro V4.0
# Created by Harsha
# ==========================================

import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

import plotly.express as px
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="AI Study Assistant Pro",

    page_icon="📚",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# ==========================================
# SESSION STATE
# ==========================================

defaults = {

    "messages": [],

    "bookmarks": [],

    "theme": "dark"

}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ==========================================
# PDF EXPORT
# ==========================================

def create_pdf(text, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):

        story.append(

            Paragraph(line, styles["BodyText"])

        )

    doc.build(story)

# ==========================================
# GEMINI
# ==========================================

def ask_ai(prompt):

    try:

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt

        )

        return response.text

    except Exception as e:

        return str(e)
    st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html,body,[class*="css"]{

font-family:'Poppins',sans-serif;

}

/* Background */

.stApp{

background:

linear-gradient(

135deg,

#0B1120,

#111827,

#1E293B);

}

/* Hide */

header{

visibility:hidden;

}

footer{

visibility:hidden;

}

#MainMenu{

visibility:hidden;

}

/* Layout */

.block-container{

padding-top:30px;

padding-left:35px;

padding-right:35px;

}

/* Sidebar */

section[data-testid="stSidebar"]{

background:

linear-gradient(

180deg,

#0F172A,

#111827);

width:320px !important;

border-right:1px solid rgba(255,255,255,.08);

}

section[data-testid="stSidebar"] *{

color:white;

}

/* Hero */

.hero{

background:

linear-gradient(

135deg,

#4F46E5,

#2563EB,

#06B6D4);

padding:45px;

border-radius:30px;

color:white;

text-align:center;

box-shadow:

0 15px 40px rgba(0,0,0,.35);

margin-bottom:25px;

transition:.3s;

}

.hero:hover{

transform:translateY(-5px);

}

/* Cards */

.card{

background:

rgba(255,255,255,.07);

backdrop-filter:blur(18px);

padding:25px;

border-radius:22px;

border:1px solid rgba(255,255,255,.08);

margin-bottom:25px;

transition:.3s;

}

.card:hover{

transform:translateY(-6px);

}

/* Buttons */

.stButton>button{

width:100%;

border:none;

border-radius:14px;

padding:12px;

background:

linear-gradient(

135deg,

#2563EB,

#4F46E5);

color:white;

font-size:16px;

font-weight:600;

}

.stButton>button:hover{

box-shadow:

0 10px 25px rgba(37,99,235,.45);

}

/* Upload */

[data-testid="stFileUploader"]{

background:#1E293B;

padding:20px;

border-radius:18px;

border:2px dashed #4F46E5;

}

/* Metrics */

[data-testid="metric-container"]{

background:

linear-gradient(

135deg,

#1E293B,

#334155);

padding:18px;

border-radius:18px;

border:1px solid rgba(255,255,255,.08);

}

</style>

""", unsafe_allow_html=True)
    # ==========================================
# HERO
# ==========================================

st.markdown("""

<div class="hero">

<h1>📚 AI Study Assistant Pro</h1>

<h3>Learn Faster • Study Smarter • Powered by Gemini AI</h3>

<p>

💬 Chat with PDF &nbsp;&nbsp;&nbsp;
📝 AI Notes &nbsp;&nbsp;&nbsp;
📚 MCQs &nbsp;&nbsp;&nbsp;
🎯 Quiz &nbsp;&nbsp;&nbsp;
🧠 Mind Map

</p>

</div>

""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("# 🤖 AI Study Assistant")

st.sidebar.markdown(
"#### Your Personal AI Learning Companion"
)

st.sidebar.markdown("---")

feature = st.sidebar.selectbox(

    "📂 Choose Feature",

    [

        "💬 Chat with PDF",

        "📝 AI Summary",

        "📖 AI Notes",

        "📚 Important Questions",

        "❓ MCQs",

        "🃏 Flashcards",

        "🎯 Quiz",

        "🔑 Keywords",

        "🧠 Explain Topic",

        "🌍 Translate",

        "💼 Interview",

        "📅 Study Planner",

        "🧠 Mind Map",

        "📈 Progress",

        "⭐ Bookmarks",

        "📋 Cheat Sheet",

        "🧮 Formula Extractor"

    ]

)

st.sidebar.markdown("---")

st.sidebar.info("🚀 Version 4.0")

# ==========================================
# UPLOAD SECTION
# ==========================================

st.markdown("""
<div class="card">

<h2>📂 Upload Study Material</h2>

<p>

Upload one or multiple PDF files.

Supported Format:

✅ PDF

Maximum:

200 MB

</p>

</div>

""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(

"",

type=["pdf"],

accept_multiple_files=True

)

if not uploaded_files:

    st.warning("👆 Upload your study PDFs to continue.")

    st.stop()
# ==========================================
# READ PDF
# ==========================================

pdf_text = ""

pages = 0

for pdf in uploaded_files:

    reader = PdfReader(pdf)

    pages += len(reader.pages)

    for page in reader.pages:

        text = page.extract_text()

        if text:

            pdf_text += text + "\n"

words = len(pdf_text.split())

characters = len(pdf_text)

reading = max(1, words // 200)

# ==========================================
# DASHBOARD
# ==========================================

st.markdown("## 📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "📄 Pages",

        pages

    )

with col2:

    st.metric(

        "📝 Words",

        f"{words:,}"

    )

with col3:

    st.metric(

        "🔤 Characters",

        f"{characters:,}"

    )

with col4:

    st.metric(

        "⏱ Reading",

        f"{reading} min"

    )

st.markdown("---")

search = st.text_input(

"🔍 Search inside PDF"

)

if search:

    if search.lower() in pdf_text.lower():

        st.success("✅ Keyword Found")

    else:

        st.error("❌ Not Found")
# ==========================================
# READ PDF
# ==========================================

pdf_text = ""

pages = 0

for pdf in uploaded_files:

    reader = PdfReader(pdf)

    pages += len(reader.pages)

    for page in reader.pages:

        text = page.extract_text()

        if text:

            pdf_text += text + "\n"

words = len(pdf_text.split())

characters = len(pdf_text)

reading = max(1, words // 200)

# ==========================================
# DASHBOARD
# ==========================================

st.markdown("## 📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "📄 Pages",

        pages

    )

with col2:

    st.metric(

        "📝 Words",

        f"{words:,}"

    )

with col3:

    st.metric(

        "🔤 Characters",

        f"{characters:,}"

    )

with col4:

    st.metric(

        "⏱ Reading",

        f"{reading} min"

    )

st.markdown("---")

search = st.text_input(

"🔍 Search inside PDF"

)

if search:

    if search.lower() in pdf_text.lower():

        st.success("✅ Keyword Found")

    else:

        st.error("❌ Not Found")
# ==========================================
# PREMIUM DASHBOARD
# ==========================================

st.markdown("## 📊 AI Dashboard")

col1, col2, col3, col4 = st.columns(4)

cards = [

("📄","Pages",pages,"#2563EB"),

("📝","Words",f"{words:,}","#8B5CF6"),

("🔤","Characters",f"{characters:,}","#10B981"),

("⏱","Reading",f"{reading} min","#F59E0B")

]

for col,(icon,title,value,color) in zip(
[col1,col2,col3,col4],cards):

    with col:

        st.markdown(f"""

<div style="

background:linear-gradient(135deg,{color},#111827);

padding:28px;

border-radius:22px;

text-align:center;

color:white;

box-shadow:0 12px 25px rgba(0,0,0,.35);

">

<div style="font-size:42px">

{icon}

</div>

<h4>{title}</h4>

<h2>{value}</h2>

</div>

""",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

a,b,c=st.columns(3)

with a:

    st.success("🤖 Gemini AI Connected")

with b:

    st.info(f"📚 {len(uploaded_files)} PDF Uploaded")

with c:

    st.warning("⚡ AI Ready")
st.markdown("## 📈 PDF Analytics")

df=pd.DataFrame({

"Metric":[

"Pages",

"Words",

"Reading"

],

"Value":[

pages,

words,

reading

]

})

fig=px.bar(

df,

x="Metric",

y="Value",

text="Value",

height=350

)

fig.update_layout(

paper_bgcolor="#111827",

plot_bgcolor="#111827",

font_color="white"

)

st.plotly_chart(

fig,

use_container_width=True
)
st.markdown("""

<div class="card">

<h2>📌 Recent Activity</h2>

<ul>

<li>✅ PDF Uploaded</li>

<li>🤖 Gemini Connected</li>

<li>📚 AI Ready</li>

<li>💬 Chat Available</li>

<li>🎯 18 AI Features Enabled</li>

</ul>

</div>

""",unsafe_allow_html=True)
st.markdown("""

<div class="card">

<h3>🔍 Smart Search</h3>

<p>

Search anything inside your uploaded PDF.

</p>

</div>

""",unsafe_allow_html=True)

search=st.text_input("",placeholder="Search any keyword...")

if search:

    if search.lower() in pdf_text.lower():

        st.success("✅ Keyword Found")

    else:

        st.error("❌ Keyword Not Found")
    /* =======================================
CHAT UI
======================================= */

.stChatMessage{

background:#1E293B;

border-radius:18px;

padding:18px;

margin-bottom:12px;

border:1px solid rgba(255,255,255,.08);

box-shadow:0 8px 20px rgba(0,0,0,.2);

}

.chat-title{

font-size:32px;

font-weight:700;

color:white;

margin-bottom:10px;

}

.chat-subtitle{

color:#94A3B8;

font-size:15px;

margin-bottom:25px;

}
# ==========================================
# CHAT WITH PDF
# ==========================================

if feature == "💬 Chat with PDF":

    st.markdown("""
    <div class="chat-title">
        💬 AI Chat Assistant
    </div>

    <div class="chat-subtitle">
        Ask anything from your uploaded PDF.
    </div>
    """, unsafe_allow_html=True)

    # Display chat history
    for message in st.session_state.messages:

        avatar = "🧑‍🎓" if message["role"] == "user" else "🤖"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    question = st.chat_input(
        "Ask a question about your PDF..."
    )

    if question:

        st.session_state.messages.append({
            "role":"user",
            "content":question
        })

        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(question)

        prompt = f"""
You are an AI Study Assistant.

Answer ONLY from the uploaded PDF.

If the answer does not exist in the PDF, reply:

'I couldn't find this information in the uploaded PDF.'

PDF:

{pdf_text}

Question:

{question}
"""

        with st.spinner("🧠 Gemini AI is analyzing your PDF..."):

            answer = ask_ai(prompt)

        st.session_state.messages.append({
            "role":"assistant",
            "content":answer
        })

        with st.chat_message("assistant", avatar="🤖"):

            st.markdown(answer)
st.markdown(answer)

st.code(answer, language="text")
col1,col2,col3 = st.columns(3)

with col1:
    st.info(f"💬 Messages: {len(st.session_state.messages)}")

with col2:
    st.success("🤖 Gemini Online")

with col3:
    st.warning(f"📄 {pages} Pages Loaded")
    if len(st.session_state.messages) == 0:

    st.markdown("""

<div class="card">

<h2>👋 Welcome to AI Chat</h2>

<p>

Ask anything about your uploaded PDF.

Examples:

• Summarize Chapter 2

• Explain DBMS

• What are the advantages?

• Generate viva questions

</p>

</div>

""", unsafe_allow_html=True)