import os
from dotenv import load_dotenv
from pyparsing import WordStart
import streamlit as st
from pypdf import PdfReader
from google import genai
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import plotly.express as px
# -------------------------
# Load API Key
# -------------------------
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# -------------------------
# PDF Creator
# -------------------------
def create_pdf(text, filename):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):
        story.append(
            Paragraph(line, styles["BodyText"])
        )

    doc.build(story)

# -------------------------
# Gemini Function
# -------------------------
def ask_ai(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"❌ Error:\n{e}"

# -------------------------
# Streamlit Page
# -------------------------
st.set_page_config(
    page_title="AI Study Assistant Pro",
    page_icon="📚",
    layout="wide"
)
st.markdown("""
<style>

/* Main Background */
.stApp{
    background: linear-gradient(
        135deg,
        #0F172A 0%,
        #111827 50%,
        #1E293B 100%
    );
}

/* Hide Streamlit Header */
header{
    visibility:hidden;
}

/* Remove top padding */
.block-container{
    padding-top:2rem;
}
.card{
    background:rgba(255,255,255,.08);
    backdrop-filter:blur(15px);
    -webkit-backdrop-filter:blur(15px);

    border-radius:20px;
    padding:20px;

    border:1px solid rgba(255,255,255,.15);

    box-shadow:0 10px 30px rgba(0,0,0,.35);

    margin-bottom:20px;

    transition:.3s;
}

.card:hover{

    transform:translateY(-6px);

    box-shadow:0 18px 35px rgba(0,0,0,.45);

}
/* Sidebar */
section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid rgba(255,255,255,0.08);
}

/* Sidebar text */
section[data-testid="stSidebar"] *{
    color:white;
}

/* Radio button container */
div[role="radiogroup"] label{
    border-radius:10px;
    padding:8px 12px;
    transition:0.25s ease;
}

/* Hover effect */
div[role="radiogroup"] label:hover{
    background:rgba(79,70,229,0.25);
    transform:translateX(5px);
}
/* Upload Box */
[data-testid="stFileUploader"]{

background:#1E293B;

padding:25px;

border-radius:18px;

border:2px dashed #3B82F6;

transition:.3s;

}

/* Hover */

[data-testid="stFileUploader"]:hover{

border-color:#06B6D4;

box-shadow:0 0 25px rgba(59,130,246,.45);

}
/* Metric Cards */

[data-testid="metric-container"]{

background:rgba(255,255,255,0.08);

border-radius:18px;

padding:18px;

border:1px solid rgba(255,255,255,.12);

box-shadow:0 8px 20px rgba(0,0,0,.30);

transition:.3s;

}

[data-testid="metric-container"]:hover{

transform:translateY(-5px);

box-shadow:0 15px 30px rgba(0,0,0,.45);

}

[data-testid="metric-container"] label{

font-size:15px;

font-weight:bold;

}
/* Dashboard Cards */
.dashboard-card{
    border-radius:18px;
    padding:20px;
    color:white;
    text-align:center;
    transition:all 0.35s ease;
    cursor:pointer;
    box-shadow:0 8px 20px rgba(0,0,0,.35);
}

/* Hover Effect */
.dashboard-card:hover{
    transform:translateY(-8px) scale(1.03);
    box-shadow:0 20px 40px rgba(0,0,0,.55);
}

/* Fade Animation */
.dashboard-card{
    animation:fadeIn 0.8s ease;
}

@keyframes fadeIn{
    from{
        opacity:0;
        transform:translateY(25px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}
/* Navigation Bar */

.nav-item{
transition:.3s;
cursor:pointer;
font-size:17px;
font-weight:600;
color:white;
}

.nav-item:hover{

color:#38BDF8;

transform:translateY(-3px);

}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Main background */
.stApp{
    background-color:#0F172A;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#1E293B;
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* Buttons */
.stButton>button{
    width:100%;
    border-radius:12px;
    background:#2563EB;
    color:white;
    font-weight:bold;
    border:none;
    padding:10px;
}

.stButton>button:hover{
    background:#1D4ED8;
}

/* Metrics */
[data-testid="metric-container"]{
    background:white;
    border-radius:12px;
    padding:15px;
    box-shadow:0px 3px 8px rgba(0,0,0,0.15);
}

/* Text input */
.stTextInput>div>div>input{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="dashboard-card" style="
background:linear-gradient(135deg,#4F46E5,#6366F1);
">

<h1>📚 AI Study Assistant Pro</h1>

<p>Upload PDFs • Chat with AI • Generate Notes • Prepare for Exams</p>

</div>
""", unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)

st.success("""
👋 Welcome!

Upload one or more PDFs and let AI help you learn faster.

✨ Features:

• 💬 Chat with PDF
• 📝 Summary
• 📚 Notes
• ❓ MCQs
• 🃏 Flashcards
• 🎯 Quiz
""")

st.markdown("</div>", unsafe_allow_html=True)
# -------------------------
# Sidebar
# -------------------------
theme = st.sidebar.toggle("🌙 Dark Mode", value=True)
st.sidebar.markdown("""
# 🤖 AI Study Assistant

Choose a feature below.
""")

feature = st.sidebar.radio(
    "Choose",
       [
    "💬 Chat with PDF",
    "📝 Summarize PDF",
    "📝 AI Notes",
    "📚 Important Questions",
    "❓ Generate MCQs",
    "🃏 Flashcards",
    "🎯 Quiz Mode",
    "🔑 Keywords",
     "🧠 Explain Topic",
     "🌐 Translate Notes",
      "💼 Interview Questions",
      "📅 Study Planner",
      "🧠 Mind Map",
      "📈 Progress Tracker",
      "⭐ Bookmarks",
      "📋 Cheat Sheet",
      "🧮 Formula Extractor",
    "🗑 Clear Chat"
]
)
st.sidebar.markdown("---")
st.sidebar.success("Version 2.0")
st.markdown("""
### 📂 Upload Your Study Material

Upload one or more PDF files.

Supported format: **PDF**
""")
uploaded_files = st.file_uploader(
    "Upload PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

# -------------------------
# Session
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if feature == "🗑 Clear Chat":
    st.session_state.messages = []
    st.sidebar.success("Chat Cleared")

# -------------------------
# No PDF
# -------------------------
if not uploaded_files:
    st.info("📄 Upload a PDF to begin.")
    st.stop()

# -------------------------
# Read PDF
# -------------------------
pdf_text = ""

for uploaded_file in uploaded_files:

    reader = PdfReader(uploaded_file)

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pdf_text += text + "\n"

st.success("✅ PDF Uploaded Successfully")
st.progress(100)
st.markdown("""
<h2 style='color:white;'>📊 Dashboard</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    # Calculate statistics
pages = sum(len(PdfReader(f).pages) for f in uploaded_files)
words = len(pdf_text.split())
characters = len(pdf_text)

col1, col2 = st.columns(2)

with col1:

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#2563EB,#4F46E5);
    padding:25px;
    border-radius:20px;
    color:white;
    ">
    <h3>📄 Study Material</h3>

    <h1>{pages} Pages</h1>

    <p>{len(uploaded_files)} PDF(s) Uploaded</p>

    </div>
    """, unsafe_allow_html=True)

with col2:

    reading_time = max(1, words // 200)

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#10B981,#14B8A6);
    padding:25px;
    border-radius:20px;
    color:white;
    ">
    <h3>🧠 AI Analytics</h3>

    <h1>{reading_time} min</h1>

    <p>Estimated Reading Time</p>

    </div>
    """, unsafe_allow_html=True)
    st.markdown("## 🚀 Features")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("💬 Chat with PDF")

with c2:
    st.info("📝 Generate Notes")

with c3:
    st.info("❓ Generate MCQs")

c4, c5, c6 = st.columns(3)

with c4:
    st.info("🃏 Flashcards")

with c5:
    st.info("📚 Quiz Mode")

with c6:
    st.info("🧠 Mind Maps")
st.markdown("### 📈 Study Progress")

progress = min(100, int(words / 100))

st.progress(progress)

st.caption(f"Study Progress: {progress}%")

st.markdown("### 🕒 Recent Activity")

st.info("""
st.markdown("## 📊 PDF Analytics")

chart_data = {
    "Category": ["Words", "Characters"],
    "Count": [words, characters]
}

fig = px.pie(
    chart_data,
    names="Category",
    values="Count",
    hole=0.55,
    color_discrete_sequence=["#4F46E5", "#06B6D4"]
)

fig.update_layout(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)
✅ PDF Uploaded

🤖 AI Ready

📚 You can now generate:
- Summary
- Notes
- MCQs
- Flashcards
- Quiz
""")
st.markdown("## 📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
   st.markdown("""
<div style="
display:flex;
justify-content:space-around;
align-items:center;
background:#1E293B;
padding:15px;
border-radius:15px;
margin-top:15px;
margin-bottom:20px;
box-shadow:0 5px 15px rgba(0,0,0,.35);
">

<div>🏠 <b>Dashboard</b></div>

<div>📂 Documents</div>

<div>🤖 AI Tools</div>

<div>📊 Analytics</div>

<div>⚙ Settings</div>

</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#0891B2,#06B6D4);
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;">
    <h2>📝</h2>
    <h3>Total Words</h3>
    <h1>{}</h1>
    </div>
    """.format(words), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#10B981,#34D399);
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;">
    <h2>⏱</h2>
    <h3>Reading Time</h3>
    <h1>{} min</h1>
    </div>
    """.format(reading_time), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#F59E0B,#FBBF24);
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;">
    <h2>📚</h2>
    <h3>PDFs</h3>
    <h1>{}</h1>
    </div>
    """.format(len(uploaded_files)), unsafe_allow_html=True)
# =====================================================
# PDF INFORMATION
# =====================================================

# =====================================================
# SEARCH IN PDF
# =====================================================

st.subheader("🔍 Search in PDF")

search = st.text_input("Enter a keyword")

if search:

    if search.lower() in pdf_text.lower():
        st.success(f'✅ "{search}" found in the PDF.')

    else:
        st.error(f'❌ "{search}" not found in the PDF.')
# =====================================================
# PDF STATISTICS
# =====================================================

pages = sum(len(PdfReader(f).pages) for f in uploaded_files)
words = len(pdf_text.split())
characters = len(pdf_text)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("📄 Pages", pages)

with col2:
    st.metric("📝 Words", words)

with col3:
    st.metric("🔤 Characters", characters)
# =====================================================
# SUMMARY
# =====================================================

if feature == "📝 Summarize PDF":

    st.subheader("📄 AI Summary")

    if st.button("Generate Summary"):

        with st.spinner("Generating Summary..."):

            prompt = f"""
You are an AI Study Assistant.

Summarize this PDF in the following format:

1. Overview
2. Key Concepts
3. Important Points
4. Exam Revision Notes

PDF:

{pdf_text}
"""

            summary = ask_ai(prompt)

            st.write(summary)

            create_pdf(summary, "AI_Summary.pdf")

            with open("AI_Summary.pdf", "rb") as pdf_file:

                st.download_button(
                    label="📄 Download Summary as PDF",
                    data=pdf_file,
                    file_name="AI_Summary.pdf",
                    mime="application/pdf"
                )
# =====================================================
# AI NOTES
# =====================================================

elif feature == "📝 AI Notes":

    st.subheader("📝 AI Study Notes")

    if st.button("Generate Notes"):

        with st.spinner("Generating Notes..."):

            prompt = f"""
You are an AI Study Assistant.

Create easy-to-study notes from this PDF.

Format:

# Chapter-wise Notes

• Important Definitions

• Key Concepts

• Important Formulas (if any)

• Exam Tips

PDF:

{pdf_text}
"""

            notes = ask_ai(prompt)

            st.write(notes)

            create_pdf(notes, "AI_Notes.pdf")

            with open("AI_Notes.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Notes as PDF",
                    data=pdf_file,
                    file_name="AI_Notes.pdf",
                    mime="application/pdf"
                )
                # =====================================================
# IMPORTANT QUESTIONS
# =====================================================

elif feature == "📚 Important Questions":

    st.subheader("📚 Important Exam Questions")

    if st.button("Generate Questions"):

        with st.spinner("Generating Important Questions..."):

            prompt = f"""
You are an AI Study Assistant.

From this PDF, generate:

1. Five 2-Mark Questions
2. Five 5-Mark Questions
3. Five 10-Mark Questions
4. Five Viva Questions

Only use information from the PDF.

PDF:

{pdf_text}
"""

            questions = ask_ai(prompt)

            st.write(questions)

            create_pdf(questions, "Important_Questions.pdf")

            with open("Important_Questions.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Questions as PDF",
                    data=pdf_file,
                    file_name="Important_Questions.pdf",
                    mime="application/pdf"
                )
                # =====================================================
# MCQs
# =====================================================

elif feature == "❓ Generate MCQs":

    st.subheader("📝 Generate MCQs")

    if st.button("Generate MCQs"):

        with st.spinner("Generating MCQs..."):

            prompt = f"""
Generate 10 multiple choice questions from this PDF.

Include the correct answer after every question.

PDF:

{pdf_text}
"""

            mcqs = ask_ai(prompt)

            st.write(mcqs)

            create_pdf(mcqs, "MCQs.pdf")

            with open("MCQs.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📥 Download MCQs as PDF",
                    data=pdf_file,
                    file_name="MCQs.pdf",
                    mime="application/pdf"
                )
                # =====================================================
# FLASHCARDS
# =====================================================

elif feature == "🃏 Flashcards":

    st.subheader("🃏 AI Flashcards")

    if st.button("Generate Flashcards"):

        with st.spinner("Generating Flashcards..."):

            prompt = f"""
You are an AI Study Assistant.

Create 20 study flashcards from this PDF.

Format each flashcard like this:

Q: Question

A: Answer

Only use information from the PDF.

PDF:

{pdf_text}
"""

            flashcards = ask_ai(prompt)

            st.write(flashcards)

            create_pdf(flashcards, "Flashcards.pdf")

            with open("Flashcards.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📄 Download Flashcards as PDF",
                    data=pdf_file,
                    file_name="Flashcards.pdf",
                    mime="application/pdf"
                )
                # =====================================================
# QUIZ MODE
# =====================================================

elif feature == "🎯 Quiz Mode":

    st.subheader("🎯 AI Quiz")

    if st.button("Start Quiz"):

        with st.spinner("Creating Quiz..."):

            prompt = f"""
Create a quiz from this PDF.

Requirements:
- 10 Multiple Choice Questions
- Four options (A, B, C, D)
- Show the correct answer after each question.

PDF:

{pdf_text}
"""

            quiz = ask_ai(prompt)

            st.write(quiz)

            create_pdf(quiz, "Quiz.pdf")

            with open("Quiz.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Quiz PDF",
                    data=pdf_file,
                    file_name="Quiz.pdf",
                    mime="application/pdf"
                )
                

    # =====================================================
    # KEYWORD EXTRACTION
    # =====================================================
    
    elif feature == "🔑 Keywords":
    
        st.subheader("🔑 Important Keywords")
    
        if st.button("Extract Keywords"):
    
            with st.spinner("Extracting keywords..."):
    
                prompt = f"""
    You are an AI Study Assistant.
    
    Extract the 30 most important keywords from this PDF.
    
    For each keyword, give a one-line explanation.
    
    PDF:
    
    {pdf_text}
    """
    
                keywords = ask_ai(prompt)
    
                st.write(keywords)
    
                create_pdf(keywords, "Keywords.pdf")
    
                with open("Keywords.pdf", "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download Keywords as PDF",
                        data=pdf_file,
                        file_name="Keywords.pdf",
                        mime="application/pdf"
                    )
                    # =====================================================
# EXPLAIN TOPIC
# =====================================================

elif feature == "🧠 Explain Topic":

    st.subheader("🧠 Explain Any Topic")

    topic = st.text_input("Enter a topic from the PDF")

    if st.button("Explain Topic"):

        if topic:

            with st.spinner("Generating explanation..."):

                prompt = f"""
You are an AI Study Assistant.

Explain the following topic using ONLY the uploaded PDF.

Topic:
{topic}

Explain in this format:

1. Definition
2. Working
3. Advantages
4. Disadvantages
5. Applications
6. Exam Tips

PDF:

{pdf_text}
"""

                explanation = ask_ai(prompt)

                st.write(explanation)

                create_pdf(explanation, "Topic_Explanation.pdf")

                with open("Topic_Explanation.pdf", "rb") as pdf_file:

                    st.download_button(
                        label="📥 Download Explanation PDF",
                        data=pdf_file,
                        file_name="Topic_Explanation.pdf",
                        mime="application/pdf"
                    )
                    # =====================================================
# TRANSLATE NOTES
# =====================================================

elif feature == "🌐 Translate Notes":

    st.subheader("🌐 Translate PDF Content")

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

        with st.spinner("Translating..."):

            prompt = f"""
Translate the important contents of this PDF into {language}.

Keep headings and bullet points.

PDF:

{pdf_text}
"""

            translated = ask_ai(prompt)

            st.write(translated)

            create_pdf(translated, "Translated_Notes.pdf")

            with open("Translated_Notes.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Translation PDF",
                    pdf_file,
                    file_name="Translated_Notes.pdf",
                    mime="application/pdf"
                )
                # =====================================================
# INTERVIEW QUESTIONS
# =====================================================

elif feature == "💼 Interview Questions":

    st.subheader("💼 Interview Questions")

    if st.button("Generate Interview Questions"):

        with st.spinner("Generating Interview Questions..."):

            prompt = f"""
You are an AI Interview Coach.

Using ONLY this PDF, generate:

1. 20 Interview Questions
2. Short Answers
3. Technical Questions
4. HR Style Questions (if applicable)

PDF:

{pdf_text}
"""

            interview = ask_ai(prompt)

            st.write(interview)

            create_pdf(interview, "Interview_Questions.pdf")

            with open("Interview_Questions.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Interview Questions",
                    data=pdf_file,
                    file_name="Interview_Questions.pdf",
                    mime="application/pdf"
                )
                # =====================================================
# STUDY PLANNER
# =====================================================

elif feature == "📅 Study Planner":

    st.subheader("📅 AI Study Planner")

    days = st.slider(
        "Study Duration (Days)",
        1,
        30,
        7
    )

    if st.button("Generate Study Plan"):

        with st.spinner("Creating Study Plan..."):

            prompt = f"""
You are an AI Study Planner.

Create a {days}-day study timetable from this PDF.

For each day include:

• Topics to study
• Revision
• Practice Questions
• Estimated study time

PDF:

{pdf_text}
"""

            planner = ask_ai(prompt)

            st.write(planner)

            create_pdf(planner, "Study_Planner.pdf")

            with open("Study_Planner.pdf", "rb") as pdf_file:

                st.download_button(
                    label="📅 Download Study Planner",
                    data=pdf_file,
                    file_name="Study_Planner.pdf",
                    mime="application/pdf"
                )
                # =====================================================
# MIND MAP
# =====================================================

elif feature == "🧠 Mind Map":

    st.subheader("🧠 AI Mind Map")

    if st.button("Generate Mind Map"):

        with st.spinner("Creating Mind Map..."):

            prompt = f"""
You are an AI Study Assistant.

Create a hierarchical mind map from this PDF.

Format:

Main Topic
│
├── Topic 1
│     ├── Subtopic
│     ├── Subtopic
│
├── Topic 2
│     ├── Subtopic

Only use information from the PDF.

PDF:

{pdf_text}
"""

            mindmap = ask_ai(prompt)

            st.code(mindmap)

            create_pdf(mindmap, "Mind_Map.pdf")

            with open("Mind_Map.pdf", "rb") as pdf_file:

                st.download_button(
                    label="📥 Download Mind Map",
                    data=pdf_file,
                    file_name="Mind_Map.pdf",
                    mime="application/pdf"
                )
                # =====================================================
# PROGRESS TRACKER
# =====================================================

elif feature == "📈 Progress Tracker":

    st.subheader("📈 Study Progress")

    progress = st.slider(
        "How much have you completed?",
        0,
        100,
        0
    )

    st.progress(progress)

    if progress == 100:
        st.success("🎉 Congratulations! You completed the PDF.")

    elif progress >= 75:
        st.info("🔥 Almost finished!")

    elif progress >= 50:
        st.warning("📚 Keep going!")

    else:
        st.error("💪 Let's start studying!")
        # =====================================================
# BOOKMARKS
# =====================================================

elif feature == "⭐ Bookmarks":

    st.subheader("⭐ Important Bookmarks")

    topic = st.text_input("Enter a topic to bookmark")

    if st.button("Add Bookmark"):

        if "bookmarks" not in st.session_state:
            st.session_state.bookmarks = []

        if topic:
            st.session_state.bookmarks.append(topic)
            st.success("✅ Bookmark Added")

    if "bookmarks" in st.session_state:

        st.write("### 📚 Saved Bookmarks")

        for i, bookmark in enumerate(st.session_state.bookmarks, start=1):
            st.write(f"{i}. {bookmark}")
            # =====================================================
# CHEAT SHEET
# =====================================================

elif feature == "📋 Cheat Sheet":

    st.subheader("📋 AI Cheat Sheet")

    if st.button("Generate Cheat Sheet"):

        with st.spinner("Creating Cheat Sheet..."):

            prompt = f"""
You are an AI Study Assistant.

Create a one-page revision cheat sheet.

Include:

• Key Definitions
• Important Formulas (if any)
• Short Notes
• Exam Tips
• Memory Tricks

Only use information from this PDF.

PDF:

{pdf_text}
"""

            cheatsheet = ask_ai(prompt)

            st.write(cheatsheet)

            create_pdf(cheatsheet, "Cheat_Sheet.pdf")

            with open("Cheat_Sheet.pdf", "rb") as pdf_file:

                st.download_button(
                    label="📥 Download Cheat Sheet",
                    data=pdf_file,
                    file_name="Cheat_Sheet.pdf",
                    mime="application/pdf"
                )
                # =====================================================
# FORMULA EXTRACTOR
# =====================================================

elif feature == "🧮 Formula Extractor":

    st.subheader("🧮 Formula Extractor")

    if st.button("Extract Formulas"):

        with st.spinner("Extracting..."):

            prompt = f"""
You are an AI Study Assistant.

Extract all formulas, equations, syntax, algorithms,
and code snippets from the uploaded PDF.

Organize them with headings.

PDF:

{pdf_text}
"""

            formulas = ask_ai(prompt)

            st.write(formulas)

            create_pdf(formulas, "Formula_Extractor.pdf")

            with open("Formula_Extractor.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Formula PDF",
                    pdf_file,
                    file_name="Formula_Extractor.pdf",
                    mime="application/pdf"
                )
# =====================================================
# CHAT
# =====================================================

else:

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask anything about your PDF...")
    st.chat_input("💬 Ask your question here...")

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        history = "\n".join(
            [
                f'{m["role"]}: {m["content"]}'
                for m in st.session_state.messages
            ]
        )

        prompt = f"""
Answer ONLY using the uploaded PDF.

If the answer is not available, reply:

"I couldn't find this information in the uploaded PDF."

PDF:

{pdf_text}

Conversation:

{history}

Question:

{question}
"""

        with st.spinner("Thinking..."):

            answer = ask_ai(prompt)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)
st.markdown("---")

st.markdown("""
<div style="
text-align:center;
padding:20px;
color:#9CA3AF;
">

<h4>📚 AI Study Assistant Pro</h4>

Built with ❤️ using Streamlit + Gemini AI

Version 2.0

</div>
""", unsafe_allow_html=True)