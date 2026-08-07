import os
from dotenv import load_dotenv
import streamlit as st
from pypdf import PdfReader
from google import genai
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import plotly.express as px

# ================================
# Load Gemini API
# ================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

# ================================
# PDF Creator
# ================================

def create_pdf(text, filename):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):
        story.append(
            Paragraph(line, styles["BodyText"])
        )

    doc.build(story)


# ================================
# Gemini Function
# ================================

def ask_ai(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"❌ {e}"


# ================================
# Streamlit Page
# ================================

st.set_page_config(
    page_title="AI Study Assistant Pro",
    page_icon="📚",
    layout="wide"
)

# ================================
# CSS
# ================================

st.markdown("""
<style>

/* Import Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

/* Background */

.stApp{
    background:
    linear-gradient(
    135deg,
    #0F172A 0%,
    #111827 40%,
    #1E293B 100%);
}

/* Header */

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

.block-container{
    padding-top:2rem;
    padding-left:3rem;
    padding-right:3rem;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] *{
    color:white;
}

/* Hero */

.hero{

background:linear-gradient(
135deg,
#4F46E5,
#2563EB,
#06B6D4);

padding:35px;

border-radius:25px;

text-align:center;

color:white;

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

background:rgba(255,255,255,.07);

backdrop-filter:blur(16px);

border:1px solid rgba(255,255,255,.12);

padding:25px;

border-radius:22px;

box-shadow:0 12px 35px rgba(0,0,0,.25);

margin-bottom:25px;

transition:.35s;

}

.card:hover{

transform:translateY(-8px);

box-shadow:0 25px 45px rgba(0,0,0,.45);

}

/* Metric */

[data-testid="metric-container"]{

background:linear-gradient(
135deg,
#1E293B,
#334155);

padding:25px;

border-radius:20px;

border:1px solid rgba(255,255,255,.08);

box-shadow:0 10px 30px rgba(0,0,0,.25);

transition:.3s;

}

[data-testid="metric-container"]:hover{

transform:scale(1.05);

}

/* Buttons */

.stButton>button{

width:100%;

padding:12px;

border-radius:15px;

border:none;

font-weight:600;

background:linear-gradient(
135deg,
#2563EB,
#4F46E5);

color:white;

transition:.3s;

}

.stButton>button:hover{

transform:translateY(-3px);

box-shadow:0 12px 25px rgba(37,99,235,.45);

}

/* File uploader */

[data-testid="stFileUploader"]{

background:#1E293B;

padding:20px;

border-radius:18px;

border:2px dashed #4F46E5;

}

/* Chat */

.stChatMessage{

border-radius:18px;

padding:18px;

background:#1E293B;

}

/* Progress */

.stProgress > div > div > div{

background:
linear-gradient(
90deg,
#2563EB,
#06B6D4);

}

/* Success */

.stSuccess{

border-radius:18px;

}

/* Warning */

.stWarning{

border-radius:18px;

}

/* Info */

.stInfo{

border-radius:18px;

}

/* Error */

.stError{

border-radius:18px;

}

</style>

""",unsafe_allow_html=True)

# ================================
# Hero Section
# ================================

st.markdown("""

<div class="hero">

<h1>📚 AI Study Assistant Pro</h1>

<h3>Learn Faster • Study Smarter</h3>

<p>
💬 Chat with PDFs • 📝 AI Notes • 📚 MCQs • 🎯 Quiz • 🧠 Mind Map
</p>

</div>

""",unsafe_allow_html=True)

# ================================
# Welcome Card
# ================================

st.markdown("""

<div class="card">

<h2>👋 Welcome</h2>

<p>

Upload one or more study PDFs and unlock powerful AI tools.

</p>

<ul>

</ul>

</div>

""",unsafe_allow_html=True)
# =====================================
# Sidebar
# =====================================

st.sidebar.title("🤖 AI Study Assistant")

feature = st.sidebar.radio(
    "Choose a Feature",
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
st.sidebar.success("Version 3.0")

# =====================================
# Upload PDF
# =====================================

uploaded_files = st.file_uploader(
    "📂 Upload PDF(s)",
    type=["pdf"],
    accept_multiple_files=True
)

# =====================================
# Session State
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if feature == "🗑 Clear Chat":
    st.session_state.messages = []
    st.sidebar.success("Chat Cleared")

# =====================================
# Wait for PDF
# =====================================

if not uploaded_files:
    st.info("📄 Upload one or more PDF files to continue.")
    st.stop()

# =====================================
# Read PDF
# =====================================

pdf_text = ""
pages = 0

for uploaded_file in uploaded_files:

    reader = PdfReader(uploaded_file)

    pages += len(reader.pages)

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pdf_text += text + "\n"

words = len(pdf_text.split())
characters = len(pdf_text)
reading_time = max(1, words // 200)

# =====================================
# Dashboard
# =====================================

st.success("✅ PDF Uploaded Successfully")

st.markdown("## 📊 Dashboard")

col1, col2, col3, col4 = st.columns(4)

cards = [
    ("📄", "Pages", pages, "#2563EB"),
    ("📝", "Words", f"{words:,}", "#7C3AED"),
    ("🔤", "Characters", f"{characters:,}", "#10B981"),
    ("⏱", "Reading", f"{reading_time} min", "#F59E0B")
]

for col, (icon, title, value, color) in zip([col1, col2, col3, col4], cards):
    with col:
        st.markdown(f"""
        <div style="
        background:linear-gradient(135deg,{color},#111827);
        padding:25px;
        border-radius:22px;
        color:white;
        text-align:center;
        box-shadow:0 10px 30px rgba(0,0,0,.35);
        transition:.3s;
        ">
            <div style="font-size:42px;">{icon}</div>
            <h4>{title}</h4>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)
# =====================================
# Search in PDF
# =====================================

st.markdown("## 🔍 Search in PDF")

search = st.text_input("Enter a keyword")

if search:

    if search.lower() in pdf_text.lower():

        st.success(f'✅ "{search}" found.')

    else:

        st.error(f'❌ "{search}" not found.')

st.markdown("---")
# =====================================
# CHAT WITH PDF
# =====================================

if feature == "💬 Chat with PDF":

    st.header("💬 Chat with Your PDF")

    # Display previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask anything from your PDF...")

    if question:

        # Show user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # AI Prompt
        prompt = f"""
You are an AI Study Assistant.

Answer ONLY using the uploaded PDF.

If the answer is not available in the PDF,
reply exactly:

"I couldn't find this information in the uploaded PDF."

PDF:

{pdf_text}

Question:

{question}
"""

        with st.spinner("🤖 Thinking..."):

            answer = ask_ai(prompt)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

# =====================================
# END CHAT
# =====================================
# =====================================
# AI SUMMARY
# =====================================

elif feature == "📝 Summarize PDF":

    st.header("📝 AI Summary")

    if st.button("Generate Summary"):

        with st.spinner("🤖 Generating Summary..."):

            prompt = f"""
You are an AI Study Assistant.

Summarize this PDF in an easy-to-understand format.

Include:

1. Overview
2. Key Concepts
3. Important Points
4. Exam Revision Notes

PDF:

{pdf_text}
"""

            summary = ask_ai(prompt)

            st.markdown(summary)

            create_pdf(summary, "AI_Summary.pdf")

            with open("AI_Summary.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Summary",
                    pdf_file,
                    file_name="AI_Summary.pdf",
                    mime="application/pdf"
                )
# =====================================
# AI NOTES
# =====================================

elif feature == "📝 AI Notes":

    st.header("📝 AI Study Notes")

    if st.button("Generate Notes"):

        with st.spinner("🤖 Creating Notes..."):

            prompt = f"""
Create well-structured study notes from this PDF.

Format:

# Chapter-wise Notes

• Important Definitions

• Key Concepts

• Important Formulae

• Exam Tips

PDF:

{pdf_text}
"""

            notes = ask_ai(prompt)

            st.markdown(notes)

            create_pdf(notes, "AI_Notes.pdf")

            with open("AI_Notes.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Notes",
                    pdf_file,
                    file_name="AI_Notes.pdf",
                    mime="application/pdf"
                )
# =====================================
# IMPORTANT QUESTIONS
# =====================================

elif feature == "📚 Important Questions":

    st.header("📚 Important Exam Questions")

    if st.button("Generate Questions"):

        with st.spinner("🤖 Generating Questions..."):

            prompt = f"""
You are an AI Study Assistant.

Using ONLY the uploaded PDF, generate:

1. Five 2-Mark Questions
2. Five 5-Mark Questions
3. Five 10-Mark Questions
4. Five Viva Questions

PDF:

{pdf_text}
"""

            questions = ask_ai(prompt)

            st.markdown(questions)

            create_pdf(questions, "Important_Questions.pdf")

            with open("Important_Questions.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Questions PDF",
                    pdf_file,
                    file_name="Important_Questions.pdf",
                    mime="application/pdf"
                )
# =====================================
# GENERATE MCQs
# =====================================

elif feature == "❓ Generate MCQs":

    st.header("❓ AI MCQ Generator")

    if st.button("Generate MCQs"):

        with st.spinner("🤖 Creating MCQs..."):

            prompt = f"""
Generate 15 multiple-choice questions from this PDF.

Each question should have:

A)
B)
C)
D)

Then provide the correct answer.

PDF:

{pdf_text}
"""

            mcqs = ask_ai(prompt)

            st.markdown(mcqs)

            create_pdf(mcqs, "MCQs.pdf")

            with open("MCQs.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download MCQs",
                    pdf_file,
                    file_name="MCQs.pdf",
                    mime="application/pdf"
                )
# =====================================
# FLASHCARDS
# =====================================

elif feature == "🃏 Flashcards":

    st.header("🃏 AI Flashcards")

    if st.button("Generate Flashcards"):

        with st.spinner("🤖 Creating Flashcards..."):

            prompt = f"""
Create 20 flashcards from this PDF.

Format:

Q:
A:

Use only information from the uploaded PDF.

PDF:

{pdf_text}
"""

            flashcards = ask_ai(prompt)

            st.markdown(flashcards)

            create_pdf(flashcards, "Flashcards.pdf")

            with open("Flashcards.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Flashcards",
                    pdf_file,
                    file_name="Flashcards.pdf",
                    mime="application/pdf"
                )
# =====================================
# QUIZ MODE
# =====================================

elif feature == "🎯 Quiz Mode":

    st.header("🎯 AI Quiz")

    if st.button("Generate Quiz"):

        with st.spinner("🤖 Creating Quiz..."):

            prompt = f"""
Create a quiz using ONLY the uploaded PDF.

Requirements:
- 10 Multiple Choice Questions
- Four options (A, B, C, D)
- Show the correct answer after each question.

PDF:

{pdf_text}
"""

            quiz = ask_ai(prompt)

            st.markdown(quiz)

            create_pdf(quiz, "Quiz.pdf")

            with open("Quiz.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Quiz PDF",
                    pdf_file,
                    file_name="Quiz.pdf",
                    mime="application/pdf"
                )
# =====================================
# KEYWORDS
# =====================================

elif feature == "🔑 Keywords":

    st.header("🔑 Important Keywords")

    if st.button("Extract Keywords"):

        with st.spinner("🤖 Extracting Keywords..."):

            prompt = f"""
Extract the 30 most important keywords from this PDF.

For each keyword give a one-line explanation.

PDF:

{pdf_text}
"""

            keywords = ask_ai(prompt)

            st.markdown(keywords)

            create_pdf(keywords, "Keywords.pdf")

            with open("Keywords.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Keywords",
                    pdf_file,
                    file_name="Keywords.pdf",
                    mime="application/pdf"
                )
# =====================================
# EXPLAIN TOPIC
# =====================================

elif feature == "🧠 Explain Topic":

    st.header("🧠 Explain Topic")

    topic = st.text_input("Enter a topic")

    if st.button("Explain"):

        if topic:

            with st.spinner("🤖 Explaining..."):

                prompt = f"""
Using ONLY the uploaded PDF,

Explain:

{topic}

Include:

• Definition

• Working

• Advantages

• Disadvantages

• Applications

PDF:

{pdf_text}
"""

                explanation = ask_ai(prompt)

                st.markdown(explanation)

                create_pdf(explanation, "Topic_Explanation.pdf")

                with open("Topic_Explanation.pdf", "rb") as pdf_file:

                    st.download_button(
                        "📥 Download Explanation",
                        pdf_file,
                        file_name="Topic_Explanation.pdf",
                        mime="application/pdf"
                    )
# =====================================
# TRANSLATE NOTES
# =====================================

elif feature == "🌐 Translate Notes":

    st.header("🌐 Translate Notes")

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

        with st.spinner("🤖 Translating..."):

            prompt = f"""
Translate the important content of this PDF into {language}.

Keep headings and bullet points.

PDF:

{pdf_text}
"""

            translated = ask_ai(prompt)

            st.markdown(translated)

            create_pdf(translated, "Translated_Notes.pdf")

            with open("Translated_Notes.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Translation",
                    pdf_file,
                    file_name="Translated_Notes.pdf",
                    mime="application/pdf"
                )
# =====================================
# INTERVIEW QUESTIONS
# =====================================

elif feature == "💼 Interview Questions":

    st.header("💼 AI Interview Questions")

    if st.button("Generate Interview Questions"):

        with st.spinner("🤖 Generating Interview Questions..."):

            prompt = f"""
Using ONLY the uploaded PDF,

Generate:

• Technical Interview Questions

• HR Questions (if applicable)

• Short Answers

PDF:

{pdf_text}
"""

            interview = ask_ai(prompt)

            st.markdown(interview)

            create_pdf(interview, "Interview_Questions.pdf")

            with open("Interview_Questions.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Interview Questions",
                    pdf_file,
                    file_name="Interview_Questions.pdf",
                    mime="application/pdf"
                )
# =====================================
# INTERVIEW QUESTIONS
# =====================================

elif feature == "💼 Interview Questions":

    st.header("💼 AI Interview Questions")

    if st.button("Generate Interview Questions"):

        with st.spinner("🤖 Generating Interview Questions..."):

            prompt = f"""
Using ONLY the uploaded PDF,

Generate:

• Technical Interview Questions

• HR Questions (if applicable)

• Short Answers

PDF:

{pdf_text}
"""

            interview = ask_ai(prompt)

            st.markdown(interview)

            create_pdf(interview, "Interview_Questions.pdf")

            with open("Interview_Questions.pdf", "rb") as pdf_file:

                st.download_button(
                    "📥 Download Interview Questions",
                    pdf_file,
                    file_name="Interview_Questions.pdf",
                    mime="application/pdf"
                )
# =====================================
# MIND MAP
# =====================================

elif feature == "🧠 Mind Map":

    st.header("🧠 AI Mind Map")

    if st.button("Generate Mind Map"):

        with st.spinner("🤖 Creating Mind Map..."):

            prompt = f"""
Create a hierarchical text mind map using ONLY the uploaded PDF.

PDF:

{pdf_text}
"""

            mindmap = ask_ai(prompt)

            st.code(mindmap)

            create_pdf(mindmap,"Mind_Map.pdf")

            with open("Mind_Map.pdf","rb") as pdf_file:

                st.download_button(
                    "📥 Download Mind Map",
                    pdf_file,
                    file_name="Mind_Map.pdf",
                    mime="application/pdf"
                )
# =====================================
# PROGRESS TRACKER
# =====================================

elif feature == "📈 Progress Tracker":

    st.header("📈 Progress Tracker")

    progress = st.slider("Study Progress",0,100,0)

    st.progress(progress)

    if progress == 100:
        st.success("🎉 Congratulations! Course Completed!")

    elif progress >= 75:
        st.info("🔥 Almost Finished!")

    elif progress >= 50:
        st.warning("📚 Keep Going!")

    else:
        st.error("💪 Let's Start Studying!")

# =====================================
# BOOKMARKS
# =====================================

elif feature == "⭐ Bookmarks":

    st.header("⭐ Bookmarks")

    topic = st.text_input("Enter Bookmark")

    if "bookmarks" not in st.session_state:
        st.session_state.bookmarks=[]

    if st.button("Add Bookmark"):

        if topic:

            st.session_state.bookmarks.append(topic)

            st.success("Bookmark Added")

    if st.session_state.bookmarks:

        st.write("### Saved Bookmarks")

        for i,item in enumerate(st.session_state.bookmarks,1):

            st.write(f"{i}. {item}")

# =====================================
# CHEAT SHEET
# =====================================

elif feature == "📋 Cheat Sheet":

    st.header("📋 AI Cheat Sheet")

    if st.button("Generate Cheat Sheet"):

        with st.spinner("🤖 Creating Cheat Sheet..."):

            prompt=f"""
Create a one-page revision cheat sheet.

Include:

• Key Definitions

• Important Formulae

• Exam Tips

PDF:

{pdf_text}
"""

            cheat=ask_ai(prompt)

            st.markdown(cheat)

            create_pdf(cheat,"Cheat_Sheet.pdf")

            with open("Cheat_Sheet.pdf","rb") as pdf:

                st.download_button(
                    "📥 Download Cheat Sheet",
                    pdf,
                    file_name="Cheat_Sheet.pdf",
                    mime="application/pdf"
                )
# =====================================
# FORMULA EXTRACTOR
# =====================================

elif feature == "🧮 Formula Extractor":

    st.header("🧮 Formula Extractor")

    if st.button("Extract Formulae"):

        with st.spinner("🤖 Extracting..."):

            prompt=f"""
Extract all important formulas, equations, syntax and algorithms from this PDF.

PDF:

{pdf_text}
"""

            formulas=ask_ai(prompt)

            st.markdown(formulas)

            create_pdf(formulas,"Formula_Extractor.pdf")

            with open("Formula_Extractor.pdf","rb") as pdf:

                st.download_button(
                    "📥 Download Formula PDF",
                    pdf,
                    file_name="Formula_Extractor.pdf",
                    mime="application/pdf"
                )
st.markdown("---")

st.markdown("""
<div style='text-align:center;color:gray;padding:15px;'>

<h4>📚 AI Study Assistant Pro</h4>

Built with ❤️ using Python • Streamlit • Gemini AI

Version 3.0

</div>
""", unsafe_allow_html=True)
