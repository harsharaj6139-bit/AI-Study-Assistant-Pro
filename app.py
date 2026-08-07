# ============================================================
# AI STUDY ASSISTANT PRO V5
# ============================================================

import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

from google import genai

import pandas as pd
import plotly.express as px

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="AI Study Assistant Pro",

    page_icon="📚",

    layout="wide",

    initial_sidebar_state="expanded"

)

# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(
    api_key=API_KEY
)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "history" not in st.session_state:
    st.session_state.history = []

today = datetime.now().strftime("%d %B %Y")
# ============================================================
# PDF EXPORT
# ============================================================

def create_pdf(text, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):

        story.append(
            Paragraph(
                line,
                styles["BodyText"]
            )
        )

    doc.build(story)


# ============================================================
# GEMINI
# ============================================================

def ask_ai(prompt):

    try:

        response = client.models.generate_content(

            model="gemini-3.6-flash",

            contents=prompt

        )

        return response.text

    except Exception as e:

        return f"❌ {e}"


# ============================================================
# READ PDF
# ============================================================

def read_pdf(files):

    pdf_text = ""

    total_pages = 0

    for file in files:

        reader = PdfReader(file)

        total_pages += len(reader.pages)

        for page in reader.pages:

            text = page.extract_text()

            if text:

                pdf_text += text + "\n"

    return pdf_text, total_pages
st.markdown("""

<style>

/* Google Font */

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

/* Hide Streamlit */

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

#2563EB,

#4F46E5,

#06B6D4);

padding:45px;

border-radius:28px;

text-align:center;

color:white;

box-shadow:

0 20px 40px rgba(0,0,0,.35);

margin-bottom:25px;

}

/* Glass Card */

.card{

background:

rgba(255,255,255,.07);

backdrop-filter:blur(18px);

padding:28px;

border-radius:22px;

border:1px solid rgba(255,255,255,.08);

margin-bottom:25px;

}

/* Button */

.stButton>button{

width:100%;

background:

linear-gradient(

135deg,

#2563EB,

#4F46E5);

color:white;

border:none;

padding:12px;

border-radius:14px;

font-weight:600;

}

/* Upload */

[data-testid="stFileUploader"]{

background:#1E293B;

padding:20px;

border-radius:18px;

border:2px dashed #4F46E5;

}

</style>

""",unsafe_allow_html=True)
# ============================================================
# HERO SECTION
# ============================================================

st.markdown(f"""

<div class="hero">

<h1>📚 AI Study Assistant Pro</h1>

<h3>Learn Faster • Study Smarter</h3>

<p>

🤖 Powered by Gemini AI

</p>

<p>

📅 {today}

</p>

</div>

""", unsafe_allow_html=True)
# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🤖 AI Study Assistant")

st.sidebar.markdown(
"### Your Personal AI Tutor"
)

st.sidebar.markdown("---")

feature = st.sidebar.selectbox(

"Choose Feature",

(

"💬 Chat with PDF",

"📝 AI Summary",

"📖 AI Notes",

"📚 Important Questions",

"❓ Generate MCQs",

"🃏 Flashcards",

"🎯 Quiz",

"🔑 Keywords",

"🧠 Explain Topic",

"🌍 Translate Notes",

"💼 Interview Questions",

"📅 Study Planner",

"🧠 Mind Map",

"📈 Progress Tracker",

"⭐ Bookmarks",

"📋 Cheat Sheet",

"🧮 Formula Extractor"

)

)

st.sidebar.markdown("---")

st.sidebar.success("🚀 Version 5.0")

st.sidebar.info(
"Gemini AI Connected"
)
# ============================================================
# CLEAR CHAT
# ============================================================

if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()
# ============================================================
# UPLOAD
# ============================================================

st.markdown("""

<div class="card">

<h2>📂 Upload Your PDFs</h2>

<p>

Upload one or more study PDFs.

Supported:

✅ PDF

</p>

</div>

""", unsafe_allow_html=True)

uploaded_files = st.file_uploader(

"",

type=["pdf"],

accept_multiple_files=True

)

if not uploaded_files:

    st.warning("📂 Upload a PDF to continue.")

    st.stop()
# ============================================================
# READ PDF
# ============================================================

pdf_text, pages = read_pdf(uploaded_files)

words = len(pdf_text.split())

characters = len(pdf_text)

reading_time = max(1, words // 200)
# ============================================================
# DASHBOARD
# ============================================================
# ============================================================
# PREMIUM DASHBOARD
# ============================================================

st.markdown("## 📊 AI Dashboard")

card1, card2, card3, card4 = st.columns(4)

cards = [
    ("📄", "Pages", pages, "#2563EB"),
    ("📝", "Words", f"{words:,}", "#8B5CF6"),
    ("🔤", "Characters", f"{characters:,}", "#10B981"),
    ("⏱", "Reading Time", f"{reading_time} min", "#F59E0B")
]

for col, (icon, title, value, color) in zip(
    [card1, card2, card3, card4], cards
):

    with col:

        st.markdown(f"""
        <div style="
        background:linear-gradient(135deg,{color},#111827);
        padding:25px;
        border-radius:22px;
        color:white;
        text-align:center;
        box-shadow:0 10px 30px rgba(0,0,0,.35);
        ">
            <div style="font-size:42px;">{icon}</div>
            <h4>{title}</h4>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)
        # ============================================================
# AI STATUS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

left, center, right = st.columns(3)

with left:
    st.success("🤖 Gemini AI Connected")

with center:
    st.info(f"📚 {len(uploaded_files)} PDF(s) Uploaded")

with right:
    st.warning("⚡ Ready to Answer")
    # ============================================================
# PDF ANALYTICS
# ============================================================

st.markdown("## 📈 PDF Analytics")

df = pd.DataFrame({

    "Metric": [

        "Pages",

        "Words",

        "Characters"

    ],

    "Value": [

        pages,

        words,

        characters

    ]

})

fig = px.bar(

    df,

    x="Metric",

    y="Value",

    text="Value",

    height=350

)

fig.update_layout(

    paper_bgcolor="#111827",

    plot_bgcolor="#111827",

    font_color="white",

    title="Uploaded PDF Statistics"

)

st.plotly_chart(

    fig,

    use_container_width=True

)
# ============================================================
# RECENT ACTIVITY
# ============================================================

st.markdown("""

<div class="card">

<h2>📌 Recent Activity</h2>

<ul>

<li>✅ PDF Uploaded Successfully</li>

<li>🤖 Gemini AI Connected</li>

<li>📄 PDF Processed</li>

<li>⚡ Dashboard Ready</li>

<li>🚀 AI Features Enabled</li>

</ul>

</div>

""", unsafe_allow_html=True)
# ============================================================
# SEARCH
# ============================================================

# ============================================================
# SMART SEARCH
# ============================================================

st.markdown("## 🔍 Smart Search")

search = st.text_input(

    "",

    placeholder="Search any keyword inside the uploaded PDF..."

)

if search:

    if search.lower() in pdf_text.lower():

        st.success(f"✅ '{search}' found in the PDF.")

    else:

        st.error(f"❌ '{search}' not found.")
# ============================================================
# CHAT WITH PDF
# ============================================================

if feature == "💬 Chat with PDF":

    st.markdown("""

    <div class="card">

    <h2>💬 AI Chat with PDF</h2>

    <p>

    Ask anything from your uploaded study material.

    </p>

    </div>

    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.success(f"📄 {pages} Pages")

    with c2:
        st.info("🤖 Gemini Online")

    with c3:
        st.warning(f"💬 {len(st.session_state.messages)} Messages")
# ============================================================
# EMPTY CHAT
# ============================================================

    if len(st.session_state.messages) == 0:

        st.markdown("""

        <div class="card">

        <h3>👋 Welcome</h3>

        <p>

        Try asking:

        <br><br>

        • Summarize Unit 1

        <br>

        • Explain DBMS

        <br>

        • Generate Viva Questions

        <br>

        • Explain Algorithms

        </p>

        </div>

        """, unsafe_allow_html=True)
# ============================================================
# CHAT HISTORY
# ============================================================

    for message in st.session_state.messages:

        avatar = "🧑" if message["role"] == "user" else "🤖"

        with st.chat_message(

            message["role"],

            avatar=avatar

        ):

            st.markdown(message["content"])
# ============================================================
# CHAT INPUT
# ============================================================

    question = st.chat_input(

        "Ask anything about your PDF..."

    )

    if question:

        st.session_state.messages.append({

            "role":"user",

            "content":question

        })

        with st.chat_message(

            "user",

            avatar="🧑"

        ):

            st.markdown(question)
            # ============================================================
# AI RESPONSE
# ============================================================

        prompt = f"""
You are an AI Study Assistant.

Answer ONLY using the uploaded PDF.

If the answer does not exist in the PDF, say:

'I couldn't find this information in the uploaded PDF.'

PDF:

{pdf_text}

Question:

{question}
"""

        with st.spinner(

            "🧠 Gemini is analyzing..."

        ):

            answer = ask_ai(prompt)

        st.session_state.messages.append({

            "role":"assistant",

            "content":answer

        })

        with st.chat_message(

            "assistant",

            avatar="🤖"

        ):

            st.markdown(answer)

            st.download_button(

                "📥 Download Answer",

                answer,

                file_name="Answer.txt",

                mime="text/plain"
            )
            # ============================================================
# AI SUMMARY
# ============================================================

elif feature == "📝 AI Summary":

    st.markdown("""
    <div class="card">
        <h2>📝 AI Summary</h2>
        <p>Create a concise summary from your uploaded PDF.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Generate Summary"):

        with st.spinner("🧠 Gemini is generating the summary..."):

            prompt = f"""
Create a structured summary using ONLY this PDF.

Include:
- Overview
- Important Topics
- Key Concepts
- Final Revision Notes

PDF:
{pdf_text}
"""

            summary = ask_ai(prompt)

            st.markdown(summary)

            create_pdf(summary, "Summary.pdf")

            with open("Summary.pdf", "rb") as pdf:

                st.download_button(
                    "📥 Download Summary",
                    pdf,
                    file_name="Summary.pdf"
                )
# ============================================================
# AI NOTES
# ============================================================

elif feature == "📖 AI Notes":

    st.markdown("""
    <div class="card">
        <h2>📖 AI Notes</h2>
        <p>Generate clean study notes.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Generate Notes"):

        with st.spinner("Generating Notes..."):

            prompt = f"""
Create chapter-wise notes from this PDF.

Include:

- Definitions
- Important Concepts
- Bullet Points
- Exam Tips

PDF:
{pdf_text}
"""

            notes = ask_ai(prompt)

            st.markdown(notes)

            create_pdf(notes, "Notes.pdf")

            with open("Notes.pdf", "rb") as pdf:

                st.download_button(
                    "📥 Download Notes",
                    pdf,
                    file_name="Notes.pdf"
                )
# ============================================================
# IMPORTANT QUESTIONS
# ============================================================

elif feature == "📚 Important Questions":

    st.markdown("""
    <div class="card">
        <h2>📚 Important Questions</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Generate Questions"):

        with st.spinner("Preparing Questions..."):

            prompt = f"""
Generate:

5 Two-Mark Questions

5 Five-Mark Questions

5 Ten-Mark Questions

5 Viva Questions

Use ONLY the uploaded PDF.

PDF:
{pdf_text}
"""

            questions = ask_ai(prompt)

            st.markdown(questions)

            create_pdf(
                questions,
                "Questions.pdf"
            )

            with open("Questions.pdf", "rb") as pdf:

                st.download_button(
                    "📥 Download Questions",
                    pdf,
                    file_name="Questions.pdf"
                )
# ============================================================
# MCQ GENERATOR
# ============================================================

elif feature == "❓ Generate MCQs":

    st.markdown("""
    <div class="card">
        <h2>❓ AI MCQ Generator</h2>
    </div>
    """, unsafe_allow_html=True)

    number = st.slider(
        "Number of MCQs",
        10,
        50,
        20
    )

    if st.button("🚀 Generate MCQs"):

        with st.spinner("Creating MCQs..."):

            prompt = f"""
Generate {number} MCQs.

Each MCQ must contain:

A)
B)
C)
D)

Give the correct answer after every question.

PDF:
{pdf_text}
"""

            mcqs = ask_ai(prompt)

            st.markdown(mcqs)

            create_pdf(
                mcqs,
                "MCQs.pdf"
            )

            with open("MCQs.pdf", "rb") as pdf:

                st.download_button(
                    "📥 Download MCQs",
                    pdf,
                    file_name="MCQs.pdf"
                )
# ============================================================
# FLASHCARDS
# ============================================================

elif feature == "🃏 Flashcards":

    st.markdown("""
    <div class="card">
        <h2>🃏 AI Flashcards</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Generate Flashcards"):

        with st.spinner("Preparing Flashcards..."):

            prompt = f"""
Generate 20 flashcards.

Format:

Question

Answer

Use ONLY the uploaded PDF.

PDF:
{pdf_text}
"""

            flashcards = ask_ai(prompt)

            st.markdown(flashcards)

            create_pdf(
                flashcards,
                "Flashcards.pdf"
            )

            with open("Flashcards.pdf", "rb") as pdf:

                st.download_button(
                    "📥 Download Flashcards",
                    pdf,
                    file_name="Flashcards.pdf"
                )
# ============================================================
# QUIZ MODE
# ============================================================

elif feature == "🎯 Quiz":

    st.markdown("""
    <div class="card">
    <h2>🎯 AI Quiz Generator</h2>
    <p>Create a practice quiz from your uploaded PDF.</p>
    </div>
    """, unsafe_allow_html=True)

    difficulty = st.selectbox(
        "Difficulty",
        ["Easy", "Medium", "Hard"]
    )

    total = st.slider(
        "Questions",
        5,
        25,
        10
    )

    if st.button("🚀 Generate Quiz"):

        with st.spinner("Creating Quiz..."):

            prompt = f"""
Generate {total} {difficulty} MCQs.

Each question must contain:

A)
B)
C)
D)

Provide the answer after every question.

PDF:

{pdf_text}
"""

            quiz = ask_ai(prompt)

            st.markdown(quiz)

            create_pdf(quiz, "Quiz.pdf")

            with open("Quiz.pdf","rb") as pdf:

                st.download_button(
                    "📥 Download Quiz",
                    pdf,
                    file_name="Quiz.pdf"
                )
# ============================================================
# KEYWORDS
# ============================================================

elif feature == "🔑 Keywords":

    st.markdown("""
    <div class="card">
    <h2>🔑 Important Keywords</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Extract Keywords"):

        prompt = f"""
Extract the 30 most important keywords.

Explain each in one line.

PDF:

{pdf_text}
"""

        keywords = ask_ai(prompt)

        st.markdown(keywords)

        create_pdf(keywords,"Keywords.pdf")

        with open("Keywords.pdf","rb") as pdf:

            st.download_button(
                "📥 Download Keywords",
                pdf,
                file_name="Keywords.pdf"
            )# ============================================================
# EXPLAIN TOPIC
# ============================================================

elif feature == "🧠 Explain Topic":

    st.markdown("""
    <div class="card">
    <h2>🧠 Explain Topic</h2>
    </div>
    """, unsafe_allow_html=True)

    topic = st.text_input(
        "Enter Topic"
    )

    if st.button("Explain"):

        prompt = f"""
Explain this topic using ONLY the uploaded PDF.

Topic:

{topic}

Include:

Definition

Working

Advantages

Applications

PDF:

{pdf_text}
"""

        explanation = ask_ai(prompt)

        st.markdown(explanation)

        create_pdf(
            explanation,
            "Topic.pdf"
        )

        with open("Topic.pdf","rb") as pdf:

            st.download_button(
                "📥 Download",
                pdf,
                file_name="Topic.pdf"
            )# ============================================================
# TRANSLATE
# ============================================================

elif feature == "🌍 Translate Notes":

    st.markdown("""
    <div class="card">
    <h2>🌍 Translate Notes</h2>
    </div>
    """, unsafe_allow_html=True)

    language = st.selectbox(

        "Choose Language",

        [

            "Hindi",

            "Kannada",

            "Telugu",

            "Tamil",

            "Malayalam"

        ]

    )

    if st.button("Translate"):

        prompt = f"""
Translate the uploaded PDF into {language}.

Maintain headings and formatting.

PDF:

{pdf_text}
"""

        translated = ask_ai(prompt)

        st.markdown(translated)

        create_pdf(
            translated,
            "Translation.pdf"
        )

        with open("Translation.pdf","rb") as pdf:

            st.download_button(
                "📥 Download",
                pdf,
                file_name="Translation.pdf"
            )# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

elif feature == "💼 Interview Questions":

    st.markdown("""
    <div class="card">
    <h2>💼 AI Interview Questions</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Generate Interview Questions"):

        prompt = f"""
Generate:

Technical Questions

HR Questions

Short Answers

Use ONLY the uploaded PDF.

PDF:

{pdf_text}
"""

        interview = ask_ai(prompt)

        st.markdown(interview)

        create_pdf(
            interview,
            "Interview.pdf"
        )

        with open("Interview.pdf","rb") as pdf:

            st.download_button(
                "📥 Download",
                pdf,
                file_name="Interview.pdf"
            )
# ============================================================
# STUDY PLANNER
# ============================================================

elif feature == "📅 Study Planner":

    st.markdown("""
    <div class="card">
    <h2>📅 AI Study Planner</h2>
    <p>Create a personalized study plan from your uploaded PDF.</p>
    </div>
    """, unsafe_allow_html=True)

    days = st.slider("Study Duration (Days)", 1, 30, 7)

    if st.button("🚀 Generate Study Plan"):

        with st.spinner("Creating Study Plan..."):

            prompt = f"""
Create a {days}-day study plan.

Include:

- Daily Topics
- Revision
- Practice Questions
- Final Revision Day

PDF:

{pdf_text}
"""

            planner = ask_ai(prompt)

            st.markdown(planner)

            create_pdf(planner, "StudyPlanner.pdf")

            with open("StudyPlanner.pdf", "rb") as pdf:

                st.download_button(
                    "📥 Download Study Plan",
                    pdf,
                    file_name="StudyPlanner.pdf"
                )# ============================================================
# MIND MAP
# ============================================================

elif feature == "🧠 Mind Map":

    st.markdown("""
    <div class="card">
    <h2>🧠 AI Mind Map</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Generate Mind Map"):

        prompt = f"""
Create a hierarchical text mind map using ONLY the uploaded PDF.

PDF:

{pdf_text}
"""

        mindmap = ask_ai(prompt)

        st.code(mindmap)

        create_pdf(
            mindmap,
            "MindMap.pdf"
        )

        with open("MindMap.pdf","rb") as pdf:

            st.download_button(
                "📥 Download Mind Map",
                pdf,
                file_name="MindMap.pdf"
            )# ============================================================
# PROGRESS TRACKER
# ============================================================

elif feature == "📈 Progress Tracker":

    st.markdown("""
    <div class="card">
    <h2>📈 Progress Tracker</h2>
    </div>
    """, unsafe_allow_html=True)

    progress = st.slider(
        "Study Progress",
        0,
        100,
        0
    )

    st.progress(progress)

    if progress == 100:
        st.success("🎉 Course Completed!")

    elif progress >= 75:
        st.info("🔥 Almost Finished!")

    elif progress >= 50:
        st.warning("📚 Keep Going!")

    else:
        st.error("💪 Let's Start!")# ============================================================
# BOOKMARKS
# ============================================================

elif feature == "⭐ Bookmarks":

    st.markdown("""
    <div class="card">
    <h2>⭐ Bookmarks</h2>
    </div>
    """, unsafe_allow_html=True)

    bookmark = st.text_input("Bookmark Name")

    if st.button("Add Bookmark"):

        if bookmark:

            st.session_state.bookmarks.append(bookmark)

            st.success("Bookmark Saved")

    if st.session_state.bookmarks:

        st.markdown("### Saved Bookmarks")

        for i, item in enumerate(
            st.session_state.bookmarks,
            start=1
        ):

            st.write(f"{i}. {item}")# ============================================================
# CHEAT SHEET
# ============================================================

elif feature == "📋 Cheat Sheet":

    st.markdown("""
    <div class="card">
    <h2>📋 AI Cheat Sheet</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Generate Cheat Sheet"):

        prompt = f"""
Create a one-page cheat sheet.

Include:

- Key Definitions
- Important Formulae
- Revision Tips

PDF:

{pdf_text}
"""

        cheat = ask_ai(prompt)

        st.markdown(cheat)

        create_pdf(
            cheat,
            "CheatSheet.pdf"
        )

        with open("CheatSheet.pdf","rb") as pdf:

            st.download_button(
                "📥 Download Cheat Sheet",
                pdf,
                file_name="CheatSheet.pdf"
            )# ============================================================
# FORMULA EXTRACTOR
# ============================================================

elif feature == "🧮 Formula Extractor":

    st.markdown("""
    <div class="card">
    <h2>🧮 Formula Extractor</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Extract Formulae"):

        prompt = f"""
Extract all formulas, equations, syntax and algorithms from this PDF.

PDF:

{pdf_text}
"""

        formulas = ask_ai(prompt)

        st.markdown(formulas)

        create_pdf(
            formulas,
            "Formulae.pdf"
        )

        with open("Formulae.pdf","rb") as pdf:

            st.download_button(
                "📥 Download Formulae",
                pdf,
                file_name="Formulae.pdf"
            )# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown("""
<div style='text-align:center;
padding:20px;
color:#94A3B8;'>

<h3>📚 AI Study Assistant Pro V5</h3>

<p>
Built with ❤️ using Python • Streamlit • Gemini AI
</p>

<p>
© 2026 Harsha
</p>

</div>
""", unsafe_allow_html=True)