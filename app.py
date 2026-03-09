import streamlit as st
import pandas as pd
from utils.predict import analyze_comment

# ---------------------------------------------
# PAGE CONFIG
# ---------------------------------------------

st.set_page_config(
    page_title="Safeguard AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------
# SESSION STATE
# ---------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------------------------------------
# CSS STYLING (YOUR ORIGINAL THEME)
# ---------------------------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(180deg,#0b1220,#0f1b2d);
color:white;
font-family: 'Segoe UI', sans-serif;
}

/* Hero */

.hero{
text-align:center;
padding-top:120px;
padding-bottom:100px;
}

.hero h1{
font-size:64px;
font-weight:800;
}

.hero p{
font-size:20px;
color:#b6c2d9;
}

/* Button */

.stButton>button{
background:#16a34a;
color:white;
border:none;
padding:14px 28px;
border-radius:10px;
font-size:18px;
font-weight:600;
}

.stButton>button:hover{
background:#22c55e;
transform:scale(1.05);
}

/* Section title */

.section-title{
text-align:center;
font-size:38px;
font-weight:700;
margin-top:60px;
}

/* Cards */

.card{
background:#1c2a3a;
padding:30px;
border-radius:16px;
border:1px solid #2c3c4f;
transition:0.3s;
}

.card:hover{
transform:translateY(-6px);
box-shadow:0 6px 20px rgba(0,0,0,0.4);
}

.card p{
color:#a8b3c7;
}

/* Footer */

.footer{
margin-top:120px;
padding:40px;
text-align:center;
color:#9fb0c8;
border-top:1px solid #2c3c4f;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------
# NAVBAR
# ---------------------------------------------

col1, col2, col3, col4, col5, col6 = st.columns([2,1,1,1,1,1])

with col1:
    st.markdown("### 💬 Safeguard AI")

with col2:
    if st.button("Home"):
        st.session_state.page = "home"

with col3:
    if st.button("Analytics"):
        st.session_state.page = "analysis"

with col4:
    if st.button("Batch"):
        st.session_state.page = "batch"

with col5:
    if st.button("Assistant"):
        st.session_state.page = "assistant"

with col6:
    if st.button("About"):
        st.session_state.page = "about"

# ---------------------------------------------
# HOME PAGE
# ---------------------------------------------

if st.session_state.page == "home":

    st.markdown("""
    <div class="hero">

    <h1>Safeguard AI: Cyberbullying Detection</h1>

    <p>
    AI that listens. Instantly detect cyberbullying,
    analyze sentiment and understand harmful online speech.
    </p>

    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Get Started"):
        st.session_state.page = "analysis"

    st.markdown(
        '<div class="section-title">✨ Platform Capabilities</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>🔍 Comment Analysis</h3>
        <p>
        Analyze individual social media comments and detect
        cyberbullying, offensive speech and harmful language.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>📂 Batch Moderation</h3>
        <p>
        Upload CSV files containing thousands of comments
        and run moderation analysis instantly.
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>🤖 AI Assistant</h3>
        <p>
        Ask the AI assistant questions about cyberbullying
        and moderation insights.
        </p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------
# ANALYTICS PAGE
# ---------------------------------------------

elif st.session_state.page == "analysis":

    st.header("🔍 Comment Analysis")

    comment = st.text_area("Enter a social media comment")

    if st.button("Analyze Comment"):

        if comment.strip() == "":
            st.warning("Please enter a comment")

        else:

            with st.spinner("Analyzing comment..."):
                result = analyze_comment(comment)

            st.subheader("Prediction Results")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Language", result["language"])
            col2.metric("Sentiment", result["sentiment"])
            col3.metric("Category", result["category"])
            col4.metric("Subcategory", result["subcategory"])

# ---------------------------------------------
# BATCH PAGE
# ---------------------------------------------

elif st.session_state.page == "batch":

    st.header("📂 Batch Comment Analysis")

    uploaded_file = st.file_uploader(
        "Upload CSV file",
        type=["csv"]
    )

    if uploaded_file:

        df = pd.read_csv(uploaded_file)

        if "comment" not in df.columns:
            st.error("CSV must contain a column named 'comment'")

        else:

            with st.spinner("Analyzing comments..."):

                predictions = []

                for text in df["comment"]:
                    result = analyze_comment(str(text))
                    predictions.append(result)

            results_df = pd.DataFrame(predictions)

            final_df = pd.concat([df, results_df], axis=1)

            st.subheader("Analysis Results")

            st.dataframe(final_df)

            csv = final_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Report",
                data=csv,
                file_name="cyberbullying_analysis_report.csv",
                mime="text/csv"
            )

# ---------------------------------------------
# AI ASSISTANT PAGE
# ---------------------------------------------

elif st.session_state.page == "assistant":

    st.header("🤖 Moderation Assistant")

    question = st.chat_input(
        "Ask about cyberbullying detection or moderation"
    )

    if question:

        st.chat_message("user").write(question)

        response = """
Cyberbullying refers to harmful online behavior such as:

• insults  
• harassment  
• threats  
• humiliation  
• offensive language  

Safeguard AI detects cyberbullying using a hierarchical NLP system that analyzes:

1. Language  
2. Sentiment  
3. Category of speech  
4. Subcategory of harmful behavior
"""

        st.chat_message("assistant").write(response)

# ---------------------------------------------
# ABOUT PAGE
# ---------------------------------------------

elif st.session_state.page == "about":

    st.title("About Safeguard AI")

    st.write("""
Safeguard AI is an AI-powered cyberbullying detection system
designed to analyze multilingual online comments and identify
harmful speech patterns.

The system uses machine learning and transformer models to
classify comments into language, sentiment, category and
subcategory levels.
""")

    st.subheader("Technologies Used")

    st.write("""
• Scikit-learn  
• Hugging Face Transformers  
• XLM-RoBERTa  
• Streamlit  
""")

    st.subheader("Authors")

    st.write("""
Stella Kiarie  
Kumati Dapash  
Morvine Otieno  
Doris Mutie  
""")

# ---------------------------------------------
# FOOTER
# ---------------------------------------------

st.markdown("""
<div class="footer">

<h4>AI-enabled Cyberbullying Detection System</h4>

<p>Powered by Scikit-Learn and Hugging Face Transformers</p>

<br>

<p>
Developed by Stella Kiarie, Kumati Dapash,<br>
Morvine Otieno and Doris Mutie
</p>

<br>

<p>© 2026 All Rights Reserved.</p>

</div>
""", unsafe_allow_html=True)