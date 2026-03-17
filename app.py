import streamlit as st
from inference.predict import analyze_comment

st.set_page_config(layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "home"

def set_bg_gradient():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(
                135deg,
                #000000 100%,   /* black */
                #DC2626 0%,  /* Kenyan red */
                #16A34A 0%  /* Kenyan green */
            );
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_gradient()
# -----------------------
st.markdown("""
<style>

/* Main Streamlit background */
[data-testid="stAppViewContainer"]{
    background-color:#0B0F14;   /* Kenyan dark black */
}

/* Make inner containers transparent so background shows */
[data-testid="stHeader"]{
    background: transparent;
}

section.main{
    background: transparent;
}

.block-container{
    background: transparent;
}

</style>
""", unsafe_allow_html=True)
# NAVBAR CSS
# -----------------------
# NAVBAR CSS
st.markdown("""
<style>

/* ---------- NAVBAR CONTAINER ---------- */
.navbar-container{
display:flex;
justify-content:space-between;
align-items:center;
padding:10px 10px 5px 10px;
margin-bottom:15px;
}

/* ---------- BRAND ---------- */
.nav-brand{
display:flex;
align-items:center;
gap:12px;
}

.nav-logo{
font-size:26px;
}

.nav-title{
font-size:26px;
font-weight:700;
color:#F9FAFB;
}

.nav-subtitle{
font-size:13px;
color:#9CA3AF;
margin-top:-2px;
}

/* ---------- NAV BUTTONS ---------- */
div.stButton > button{

background: linear-gradient(135deg,#111827,#DC2626,#16A34A);

color:white;

border:none;

border-radius:12px;

height:42px;

font-size:16px;

font-weight:600;

padding:0px 16px;

white-space:nowrap;

transition:0.25s;

}

/* Hover */
div.stButton > button:hover{

background: linear-gradient(135deg,#DC2626,#16A34A);

transform:translateY(-2px);

box-shadow:0 4px 12px rgba(0,0,0,0.4);

}

/* ---------- ACTIVE TAB ---------- */
.active-tab button{

background: linear-gradient(135deg,#DC2626,#16A34A);

border-bottom:3px solid white;

}

/* ---------- NAVBAR DIVIDER ---------- */
.nav-divider{
height:3px;
background:#DC2626;
border-radius:2px;
margin-top:10px;
margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)
# -----------------------
# NAVBAR
# -----------------------
# initialize page state
if "page" not in st.session_state:
    st.session_state.page = "home"

nav1, nav2 = st.columns([3,7])

# ---------- BRAND ----------
with nav1:
    st.markdown("""
    <div class="nav-brand">
        <div class="nav-logo">🇰🇪</div>
        <div>
            <div class="nav-title">VibeCheck Kenya</div>
            <div class="nav-subtitle">Smart Moderation for the 254</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ---------- NAVIGATION ----------
with nav2:

    c1,c2,c3,c4,c5 = st.columns([1.2,1.2,1.2,1.2,1.2])

    with c1:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "home"

    with c2:
        if st.button("📊 Analysis", use_container_width=True):
            st.session_state.page = "analysis"

    with c3:
        if st.button("📥 Batch", use_container_width=True):
            st.session_state.page = "batch"

    with c4:
        if st.button("🤖 Assistant", use_container_width=True):
            st.session_state.page = "assistant"

    with c5:
        if st.button("⚙ System", use_container_width=True):
            st.session_state.page = "system"

# divider
st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

# ------------------------
# -----------------------------
# PAGE FUNCTIONS
# -----------------------------
def show_analysis():

    import plotly.graph_objects as go

    st.markdown("## 📊 Comment Analysis")

    comment = st.text_area(
        "Enter a comment to analyze",
        placeholder="Example: Wewe ni fala kabisa"
    )

    if st.button("Analyze Comment"):

        if comment.strip() == "":
            st.warning("Please enter a comment.")
            return

        with st.spinner("Analyzing comment..."):
            result = analyze_comment(comment)

        st.success("Analysis Completed")

        # -----------------------------
        # CATEGORY COLORS
        # -----------------------------

        category_colors = {
            "Constructive": "#16A34A",
            "Others": "#F59E0B",
            "Irony": "#38BDF8",
            "Offensive": "#FB923C",
            "Cyberbullying": "#DC2626",
            "Harmful": "#991B1B"
        }

        color = category_colors.get(result["category"], "#9CA3AF")

        # -----------------------------
        # TOXICITY SCORE
        # -----------------------------

        toxicity_scores = {
            "Constructive": 1,
            "Others": 2,
            "Irony": 3,
            "Offensive": 6,
            "Cyberbullying": 8,
            "Harmful": 10
        }

        toxicity_level = toxicity_scores.get(result["category"], 3)

        # -----------------------------
        # TOXICITY METER
        # -----------------------------

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=toxicity_level,
            title={'text': "Toxicity Level"},
            gauge={
                'axis': {'range': [0,10]},
                'bar': {'color': color},
                'steps': [
                    {'range':[0,3],'color':"#16A34A"},
                    {'range':[3,6],'color':"#F59E0B"},
                    {'range':[6,10],'color':"#DC2626"}
                ]
            }
        ))

        fig.update_layout(
            paper_bgcolor="#111827",
            font=dict(color="#F9FAFB"),
            margin=dict(l=20,r=20,t=40,b=20)
        )

        # -----------------------------
        # RESULT DISPLAY
        # -----------------------------

        col1, col2 = st.columns([1,1])

        with col1:

            st.markdown("### Moderation Results")

            st.metric("Language", result["language"])
            st.metric("Sentiment", result["sentiment"])

            st.markdown(
                f"""
                <div style="
                margin-top:15px;
                padding:22px;
                background:#111827;
                border-radius:14px;
                border-left:6px solid {color};
                ">

                <h4 style="color:#9CA3AF;margin-bottom:5px;">
                Category
                </h4>

                <h2 style="color:{color};margin-top:0;">
                {result["category"]}
                </h2>

                <h4 style="color:#9CA3AF;margin-top:15px;margin-bottom:5px;">
                Subcategory
                </h4>

                <h3 style="color:#F9FAFB;margin-top:0;">
                {result["subcategory"]}
                </h3>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.plotly_chart(fig, use_container_width=True)
import pandas as pd
import plotly.express as px
import streamlit as st

import pandas as pd
import plotly.express as px
import streamlit as st
def show_batch():

    import pandas as pd
    import plotly.express as px

    st.markdown("## 📂 Batch Comment Moderation")
    st.write("Upload a CSV file for large-scale analysis.")

    # ---------------------------
    # SESSION STATE
    # ---------------------------

    if "batch_df" not in st.session_state:
        st.session_state.batch_df = None

    if "batch_results" not in st.session_state:
        st.session_state.batch_results = None

    if "uploaded_file_id" not in st.session_state:
        st.session_state.uploaded_file_id = None

    # ---------------------------
    # FILE UPLOADER
    # ---------------------------

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"],
        key="batch_uploader"
    )

    if uploaded_file is not None:

        file_id = uploaded_file.name + str(uploaded_file.size)

        if st.session_state.uploaded_file_id != file_id:

            df = pd.read_csv(uploaded_file)

            st.session_state.uploaded_file_id = file_id
            st.session_state.batch_df = df
            st.session_state.batch_results = None

        df = st.session_state.batch_df

        # ---------------------------
        # DETECT TEXT COLUMN
        # ---------------------------

        if "comment" in df.columns:
            text_col = "comment"

        elif "text" in df.columns:
            text_col = "text"

        else:
            st.error(
                f"CSV must contain **comment** or **text** column.\n\n"
                f"Columns detected: {list(df.columns)}"
            )
            return

        # ---------------------------
        # PREVIEW DATASET
        # ---------------------------

        st.markdown("### 📄 Dataset Preview")
        st.dataframe(df.head())

        # ---------------------------
        # RUN MODERATION
        # ---------------------------

        if st.session_state.batch_results is None:

            if st.button("🚀 Run Moderation Analysis"):

                results = []
                progress_bar = st.progress(0)

                for i, text in enumerate(df[text_col]):

                    prediction = analyze_comment(str(text))
                    results.append(prediction)

                    progress_bar.progress((i + 1) / len(df))

                results_df = pd.DataFrame(results)

                final_df = pd.concat(
                    [df.reset_index(drop=True), results_df],
                    axis=1
                )

                st.session_state.batch_results = final_df

                st.success("✅ Batch analysis completed!")

    # ---------------------------
    # DISPLAY RESULTS
    # ---------------------------

    if st.session_state.batch_results is not None:

        final_df = st.session_state.batch_results

        st.markdown("---")
        st.subheader("📊 Moderation Results")

        # ---------------------------
        # SUMMARY METRICS
        # ---------------------------

        st.markdown("### 📈 Key Insights")

        col1, col2, col3, col4 = st.columns(4)

        total = len(final_df)
        toxic = final_df[final_df["category"].isin(["Cyberbullying", "Harmful"])].shape[0]
        positive = final_df[final_df["sentiment"] == "Positive"].shape[0]
        negative = final_df[final_df["sentiment"] == "Negative"].shape[0]

        col1.metric("Total Comments", total)
        col2.metric("Toxic Comments", toxic)
        col3.metric("Positive", positive)
        col4.metric("Negative", negative)

        # ---------------------------
        # HIGHLIGHT TOXIC COMMENTS
        # ---------------------------

        st.markdown("### ⚠️ High Risk Comments")

        toxic_df = final_df[final_df["category"].isin(["Cyberbullying", "Harmful"])]

        if len(toxic_df) > 0:
            st.dataframe(toxic_df.head(10))
        else:
            st.success("No harmful comments detected")

        # ---------------------------
        # SORT DATA
        # ---------------------------

        priority_order = {
            "Harmful": 1,
            "Cyberbullying": 2,
            "Offensive": 3,
            "Irony": 4,
            "Others": 5,
            "Constructive": 6
        }

        final_df["priority"] = final_df["category"].map(priority_order)
        final_df = final_df.sort_values("priority")

        st.markdown("### 📄 Full Results")
        st.dataframe(final_df.drop(columns=["priority"]))

        # ---------------------------
        # DOWNLOAD
        # ---------------------------

        csv = final_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Labeled Dataset",
            csv,
            "moderated_comments.csv",
            "text/csv"
        )

        # ---------------------------
        # DASHBOARD (KENYAN COLORS)
        # ---------------------------

        st.markdown("### 📊 Dataset Insights")

        col1, col2 = st.columns(2)

        # Kenyan flag color palette
        colors = ["#16A34A", "#DC2626", "#000000", "#F59E0B", "#9CA3AF"]

        with col1:

            fig1 = px.pie(
                final_df,
                names="category",
                title="Comment Category Distribution",
                hole=0.4,
                color_discrete_sequence=colors
            )

            fig1.update_layout(
                plot_bgcolor="#111827",
                paper_bgcolor="#111827",
                font=dict(color="#F9FAFB")
            )

            st.plotly_chart(fig1, use_container_width=True)

        with col2:

            lang_counts = final_df["language"].value_counts().reset_index()
            lang_counts.columns = ["language", "count"]

            fig2 = px.bar(
                lang_counts,
                x="language",
                y="count",
                title="Languages Detected",
                color="language",
                color_discrete_sequence=["#16A34A", "#DC2626", "#000000"]
            )

            fig2.update_layout(
                plot_bgcolor="#111827",
                paper_bgcolor="#111827",
                font=dict(color="#F9FAFB")
            )

            st.plotly_chart(fig2, use_container_width=True)

        # ---------------------------
        # INSIGHTS
        # ---------------------------

        st.markdown("### 🧠 Insights")

        if toxic > 0:
            st.warning(f"{toxic} harmful comments detected. Immediate moderation recommended.")
        else:
            st.success("Dataset is mostly safe with minimal harmful content.")
def show_assistant():

    st.markdown("## 🤖 AI Moderation Assistant")

    st.write("Ask about moderation, system features, or analyze a comment.")

    # ----------------------------
    # QUICK PROMPTS
    # ----------------------------

    st.markdown("### Quick Questions")

    p1, p2, p3 = st.columns(3)
    p4, p5, p6 = st.columns(3)

    if p1.button("What is cyberbullying?"):
        user_prompt = "What is cyberbullying?"

    elif p2.button("What languages does the system support?"):
        user_prompt = "What languages are supported?"

    elif p3.button("How does the moderation system work?"):
        user_prompt = "How does the system work?"

    elif p4.button("How can social media reduce cyberbullying?"):
        user_prompt = "How to reduce cyberbullying?"

    elif p5.button("Explain moderation categories"):
        user_prompt = "Explain moderation categories"

    elif p6.button("Analyze: wewe ni fala kabisa"):
        user_prompt = "Analyze: wewe ni fala kabisa"

    else:
        user_prompt = None

    # ----------------------------
    # CHAT HISTORY
    # ----------------------------

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    chat_input = st.chat_input("Ask something or type: Analyze: your comment")

    if chat_input:
        user_prompt = chat_input

    if user_prompt:

        prompt = user_prompt.lower()

        # COMMENT ANALYSIS
        if prompt.startswith("analyze:"):

            comment = user_prompt.split(":",1)[1].strip()

            result = analyze_comment(comment)

            response = f"""
Comment Analysis Result

Language: {result['language']}

Sentiment: {result['sentiment']}

Category: {result['category']}

Subcategory: {result['subcategory']}
"""

        # CYBERBULLYING EXPLANATION
        elif "cyberbullying" in prompt:

            response = """
Cyberbullying refers to online harassment or insults targeting a person.

Examples include:
• Direct insults
• Threatening language
• Harassment
• Public humiliation
"""

        # SUPPORTED LANGUAGES
        elif "languages" in prompt:

            response = """
The moderation system supports:

• English
• Kiswahili
• Kenyan Sheng

The AI can detect code-mixed language used in Kenyan social media.
"""

        # SYSTEM PIPELINE
        elif "how does the system work" in prompt:

            response = """
The AI moderation system works in four stages:

1️⃣ Text preprocessing  
2️⃣ Language detection  
3️⃣ Sentiment analysis  
4️⃣ Transformer toxicity classification
"""

        # REDUCE CYBERBULLYING
        elif "reduce cyberbullying" in prompt:

            response = """
Ways to reduce cyberbullying:

• Automatically filter toxic comments
• Use AI moderation tools
• Encourage positive community guidelines
• Block repeat offenders
"""

        # MODERATION CATEGORIES
        elif "categories" in prompt:

            response = """
The system classifies comments into these categories:

Constructive → Positive engagement  
Cyberbullying → Harassment or insults  
Harmful → Dangerous or abusive language  
Offensive → Profanity or rude language  
Irony → Sarcasm or mocking tone  
Others → Neutral comments
"""

        else:

            response = """
I can help with:

• Explaining cyberbullying
• Explaining moderation categories
• Explaining how the system works
• Analyzing comments

Try typing:

Analyze: your comment
"""

        st.session_state.chat_history.append(("user", user_prompt))
        st.session_state.chat_history.append(("assistant", response))

    # ----------------------------
    # DISPLAY CHAT
    # ----------------------------

    for role, message in st.session_state.chat_history:

        with st.chat_message(role):
            st.write(message)
def show_system():

    # -------------------------
    # SECTION TITLE
    # -------------------------

    st.markdown("""
    <h2 style="text-align:center;margin-bottom:30px;">
    ⚙ AI Moderation System Overview
    </h2>
    """, unsafe_allow_html=True)


    # -------------------------
    # INTRO CARD
    # -------------------------

    st.markdown("""
    <div style="
    background:#111827;
    padding:28px;
    border-radius:14px;
    border-top:3px solid #DC2626;
    margin-bottom:35px;
    ">
    <h4 style="margin-bottom:10px;color:#F9FAFB;">
    AI-enabled Kenyan Social Media Moderation
    </h4>

    <p style="color:#D1D5DB;">
    This system detects cyberbullying and harmful content across
    multilingual Kenyan online conversations using machine learning
    and transformer-based models.
    </p>
    </div>
    """, unsafe_allow_html=True)


    # -------------------------
    # AI PIPELINE
    # -------------------------

    st.markdown("### 🧠 Moderation Pipeline")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div style="background:#111827;padding:18px;border-radius:12px;border-left:4px solid #16A34A;">
        <b>1️⃣ Preprocessing</b><br>
        Cleaning and normalization of comments.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#111827;padding:18px;border-radius:12px;border-left:4px solid #16A34A;">
        <b>2️⃣ Language Detection</b><br>
        Detects English, Kiswahili, or Sheng.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:#111827;padding:18px;border-radius:12px;border-left:4px solid #16A34A;">
        <b>3️⃣ Sentiment Analysis</b><br>
        Determines comment emotion.
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="background:#111827;padding:18px;border-radius:12px;border-left:4px solid #16A34A;">
        <b>4️⃣ Toxicity Classification</b><br>
        Detects cyberbullying and harmful language.
        </div>
        """, unsafe_allow_html=True)


    st.write("")


    # -------------------------
    # MODEL COMPONENTS
    # -------------------------

    st.markdown("### 🧩 Model Components")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background:#111827;padding:22px;border-radius:12px;">
        • Language Detection Model<br>
        • Sentiment Analysis Model<br>
        • Category Classification Model
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#111827;padding:22px;border-radius:12px;">
        • Transformer Subcategory Models<br>
        • Feature Engineering Modules<br>
        • Text Preprocessing Pipeline
        </div>
        """, unsafe_allow_html=True)


    st.write("")


    # -------------------------
    # SUPPORTED LANGUAGES
    # -------------------------

    st.markdown("### 🌍 Supported Languages")

    col1, col2, col3 = st.columns(3)

    col1.metric("English", "Supported")
    col2.metric("Kiswahili", "Supported")
    col3.metric("Kenyan Sheng", "Supported")


    st.write("")


    # -------------------------
    # MODERATION CATEGORIES
    # -------------------------

    st.markdown("### 🏷 Moderation Categories")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;">
        <b>Constructive</b><br>
        Positive engagement
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;margin-top:10px;">
        <b>Cyberbullying</b><br>
        Harassment or insults
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;">
        <b>Offensive</b><br>
        Profanity or rude language
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;margin-top:10px;">
        <b>Harmful</b><br>
        Dangerous or abusive text
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;">
        <b>Irony</b><br>
        Sarcasm or mockery
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;margin-top:10px;">
        <b>Others</b><br>
        Neutral comments
        </div>
        """, unsafe_allow_html=True)


    st.write("")


    # -------------------------
    # MODEL PERFORMANCE
    # -------------------------

    st.markdown("### 📈 Model Performance")

    col1, col2, col3 = st.columns(3)

    col1.metric("Language Model", "95% Accuracy")
    col2.metric("Sentiment Model", "92% Accuracy")
    col3.metric("Category Model", "90% Accuracy")


    st.write("")


    # -------------------------
    # TECHNOLOGY STACK
    # -------------------------

    st.markdown("### 🛠 Technology Stack")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;">
        <b>Frontend</b><br>
        Streamlit
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;margin-top:10px;">
        <b>Machine Learning</b><br>
        Scikit-Learn
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;">
        <b>Transformers</b><br>
        HuggingFace
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#111827;padding:20px;border-radius:12px;margin-top:10px;">
        <b>Data Processing</b><br>
        Pandas
        </div>
        """, unsafe_allow_html=True)
# -----------------------------
# PAGE ROUTER
# -----------------------------
if st.session_state.page == "analysis":
    show_analysis()

elif st.session_state.page == "batch":
    show_batch()

elif st.session_state.page == "assistant":
    show_assistant()

elif st.session_state.page == "system":
    show_system()

else:
    # HOME PAGE

    # ------------------------
    # HERO SECTION

    st.markdown("""
    <style>

    /* HERO SECTION */
    .hero-section{
    background: linear-gradient(135deg,#111827,#DC2626,#16A34A);
    padding:50px 60px;
    border-radius:18px;
    text-align:center;

    /* expand width */
    width:95%;
    margin-left:auto;
    margin-right:auto;

    margin-top:25px;
    margin-bottom:40px;

    box-shadow:0 8px 30px rgba(0,0,0,0.35);
    }

    /* Title */
    .hero-title{
    font-size:42px;
    font-weight:800;
    color:white;
    margin-bottom:12px;
    }

    /* Subtitle */
    .hero-sub{
    font-size:19px;
    color:#F9FAFB;
    margin-bottom:26px;
    }

    /* STYLE STREAMLIT BUTTON TO MATCH HERO */
    div.stButton > button {
        background:white;
        color:#111827;
        padding:12px 28px;
        font-size:17px;
        font-weight:700;
        border-radius:10px;
        border:none;
        box-shadow:0px 5px 14px rgba(0,0,0,0.25);
        transition:0.25s;
    }

    /* Hover */
    div.stButton > button:hover {
        background:#16A34A;
        color:white;
        transform:translateY(-2px);
    }

    </style>
    """, unsafe_allow_html=True)


    st.markdown("""
    <div class="hero-section">

    <div class="hero-title">
    🛡 Kenyan Cyberbullying Detection AI
    </div>

    <div class="hero-sub">
    Moderate social media comments in <b>Sheng, Kiswahili, and English</b>
    </div>

    </div>
    """, unsafe_allow_html=True)


    # Center button
    col1, col2, col3 = st.columns([3,2,3])

    with col2:
        if st.button("Start Analysis →", use_container_width=True):
            st.session_state.page = "analysis"
            st.rerun()

    # FEATURE CARDS
    # ------------------------
    st.markdown("""
    <style>

    /* FEATURE CARD */
    .feature-card{
        background:#111827;
        padding:32px;
        border-radius:18px;
        border-top:3px solid #DC2626;

        /* ensure equal height */
        height:100%;
        min-height:260px;

        display:flex;
        flex-direction:column;
        justify-content:flex-start;

        box-shadow:0 6px 18px rgba(0,0,0,0.35);
        transition:all 0.25s ease;
    }

    /* Hover */
    .feature-card:hover{
        transform:translateY(-6px);
        border-top:3px solid #16A34A;
    }

    /* ICON */
    .feature-icon{
        font-size:26px;
        margin-bottom:14px;
    }

    /* TITLE */
    .feature-title{
        font-size:22px;
        font-weight:700;
        color:#F9FAFB;
        margin-bottom:10px;
    }

    /* TEXT */
    .feature-text{
        font-size:16px;
        color:#D1D5DB;
        line-height:1.6;
        flex-grow:1;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <hr style="
    border:none;
    height:3px;
    background: linear-gradient(
    90deg,
    transparent,
    #DC2626,
    #16A34A,
    transparent
    );
    margin-top:40px;
    margin-bottom:40px;
    border-radius:2px;
    ">
    """, unsafe_allow_html=True)

    st.markdown("""
    <h2 style="
    text-align:center;
    font-size:32px;
    margin-bottom:40px;
    color:#F9FAFB;
    ">
    ✨ Platform Capabilities
    </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🛡</div>
            <div class="feature-title">Comment Analysis</div>
            <div class="feature-text">
            Analyze individual social media comments to detect cyberbullying,
            harassment, and offensive language in Sheng, Kiswahili, and English.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📂</div>
            <div class="feature-title">Batch Comment Processing</div>
            <div class="feature-text">
            Upload CSV datasets of comments for large-scale moderation and
            identify harmful content trends across thousands of messages.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Moderation Assistant</div>
            <div class="feature-text">
            Interact with an AI assistant to understand predictions,
            explain model outputs, and gain insights into toxic patterns.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    <hr style="
    border:none;
    height:3px;
    background: linear-gradient(
    90deg,
    transparent,
    #DC2626,
    #16A34A,
    transparent
    );
    margin-top:40px;
    margin-bottom:40px;
    border-radius:2px;
    ">
    """, unsafe_allow_html=True)
    st.write("")
    st.markdown("""
    <style>

    /* WORKFLOW CONTAINER */
    .workflow-card{
        background:#111827;
        padding:26px;
        border-radius:16px;
        border-left:4px solid #DC2626;
        min-height:160px;
        transition:all 0.25s ease;
    }

    /* Hover */
    .workflow-card:hover{
        border-left:4px solid #16A34A;
        transform:translateY(-4px);
    }

    /* STEP NUMBER */
    .workflow-step{
        font-size:18px;
        font-weight:700;
        color:#F9FAFB;
        margin-bottom:6px;
    }

    /* STEP TITLE */
    .workflow-title{
        font-size:20px;
        font-weight:700;
        color:#F9FAFB;
        margin-bottom:8px;
    }

    /* DESCRIPTION */
    .workflow-text{
        font-size:15px;
        color:#D1D5DB;
        line-height:1.5;
    }

    </style>
    """, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("""
    <h2 style="text-align:center;margin-bottom:40px;">
    ⚙️ How the Moderation System Works
    </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-step">Step 1</div>
            <div class="workflow-title">Input Comment</div>
            <div class="workflow-text">
            A social media comment is collected from platforms
            like YouTube, X, TikTok, or other online discussions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-step">Step 2</div>
            <div class="workflow-title">Language Detection</div>
            <div class="workflow-text">
            The system identifies whether the text contains
            English, Kiswahili, or Sheng expressions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-step">Step 3</div>
            <div class="workflow-title">Sentiment Analysis</div>
            <div class="workflow-text">
            The emotional tone of the comment is analyzed
            to determine if it expresses positive,
            neutral, or negative sentiment.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-step">Step 4</div>
            <div class="workflow-title">Toxicity Classification</div>
            <div class="workflow-text">
            The model classifies the comment into categories
            such as constructive, offensive, harmful,
            or cyberbullying.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    <hr style="
    border:none;
    height:3px;
    background: linear-gradient(
    90deg,
    transparent,
    #DC2626,
    #16A34A,
    transparent
    );
    margin-top:40px;
    margin-bottom:40px;
    border-radius:2px;
    ">
    """, unsafe_allow_html=True)
    ##--------------------------------
    st.markdown("""
    <style>

    /* WHY SECTION CARD */
    .impact-card{
        background:#111827;
        padding:32px;
        border-radius:16px;
        border-top:3px solid #DC2626;
        height:100%;
    }

    /* TITLE */
    .impact-title{
        font-size:22px;
        font-weight:700;
        color:#F9FAFB;
        margin-bottom:14px;
    }

    /* TEXT */
    .impact-text{
        font-size:16px;
        color:#D1D5DB;
        line-height:1.6;
    }

    </style>
    """, unsafe_allow_html=True)
    ##--------------------------------
    st.markdown("""
    <h2 style="text-align:center;margin-bottom:40px;">
    🇰🇪 Why Kenyan Social Media Moderation Matters
    </h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="impact-card">
            <div class="impact-title">The Reality of Kenyan Online Spaces</div>
            <div class="impact-text">
            ✅ Kenya has one of the most vibrant digital communities in Africa.
            Millions of users engage daily on platforms such as YouTube,
            X (Twitter), TikTok, and Facebook.
            <br><br>
            ✅ While these platforms enable connection, creativity,
            and public conversation, they also expose individuals
            to large volumes of harmful comments and cyberbullying.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="impact-card">
            <div class="impact-title">Why Localized Moderation Is Needed</div>
            <div class="impact-text">
            ✅ Kenyan online conversations often combine English,
            Kiswahili, and Sheng in the same sentence.
            <br><br>
            ✅ Because most moderation tools are designed for
            standard English, harmful comments written using
            local slang or code-mixed language frequently
            bypass traditional detection systems.
            <br><br>
            ✅ AI systems trained specifically for Kenyan
            digital communication are essential for creating
            safer and healthier online communities.
            </div>
        </div>
        """, unsafe_allow_html=True)
    ##--------------------------------
    ##-----------impacts section ---------------------
    ##--------------------------------
    ##--------------------------------
    st.markdown("""
    <style>

    /* IMPACT CARD */
    .impact-box{
        background:#111827;
        padding:30px;
        border-radius:16px;
        border-top:3px solid #16A34A;
        min-height:170px;
        transition:all 0.25s ease;
    }

    /* hover */
    .impact-box:hover{
        transform:translateY(-6px);
        border-top:3px solid #DC2626;
    }

    /* icon */
    .impact-icon{
        font-size:28px;
        margin-bottom:10px;
    }

    /* title */
    .impact-heading{
        font-size:20px;
        font-weight:700;
        color:#F9FAFB;
        margin-bottom:10px;
    }

    /* text */
    .impact-text{
        font-size:15px;
        color:#D1D5DB;
        line-height:1.6;
    }

    </style>
    """, unsafe_allow_html=True)
    ##--------------------------------
    st.markdown("""
    <hr style="
    border:none;
    height:3px;
    background: linear-gradient(
    90deg,
    transparent,
    #DC2626,
    #16A34A,
    transparent
    );
    margin-top:40px;
    margin-bottom:40px;
    border-radius:2px;
    ">
    """, unsafe_allow_html=True)
    ###--------------------------------
    st.markdown("""
    <h2 style="text-align:center;margin-bottom:35px;">
    🎯 Impact of This System
    </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="impact-box">
            <div class="impact-icon">🧑‍💻</div>
            <div class="impact-heading">Content Creators</div>
            <div class="impact-text">
            Automatically detect and filter toxic comments, allowing
            creators to maintain safer and more positive online communities.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="impact-box">
            <div class="impact-icon">🏢</div>
            <div class="impact-heading">Brands & Organizations</div>
            <div class="impact-text">
            Monitor public conversations and sentiment to protect
            brand reputation and respond quickly to harmful discussions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="impact-box">
            <div class="impact-icon">🛡</div>
            <div class="impact-heading">Online Communities</div>
            <div class="impact-text">
            Encourage respectful interactions and reduce cyberbullying
            by identifying harmful language across multilingual conversations.
            </div>
        </div>
        """, unsafe_allow_html=True)
    # ------------------------
    # STATS SECTION
    st.markdown("""
    <hr style="
    border:none;
    height:3px;
    background: linear-gradient(
    90deg,
    transparent,
    #DC2626,
    #16A34A,
    transparent
    );
    margin-top:40px;
    margin-bottom:40px;
    border-radius:2px;
    ">
    """, unsafe_allow_html=True)
    # ------------------------
    import plotly.express as px
    import pandas as pd
    st.markdown(
        """
        <div style="
            height:120px;
            background: linear-gradient(
                90deg,
                rgba(22,163,74,0.15),
                rgba(220,38,38,0.15)
            );
            margin:40px -60px;
            border-radius:12px;
        ">
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <h2 style="
            text-align:center;
            font-size:36px;
            font-weight:700;
            margin-top:10px;
            margin-bottom:25px;
            color:#F9FAFB;
        ">
            📊  Platform Insights 
        </h2>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Comments Analyzed", "12,210")
    col2.metric("Cyberbullying Detected", "1,210")
    col3.metric("Languages Supported", "3")
    col4.metric("Model Accuracy", "92%")
    st.markdown(
        """
        <div style="
            height:2px;
            background: linear-gradient(
                90deg,
                transparent,
                #16A34A,
                #DC2626,
                transparent
            );
            margin:35px 0 25px 0;
            border-radius:4px;
        ">
        </div>
        """,
        unsafe_allow_html=True
    )
    import plotly.express as px
    import pandas as pd

    # -------- Sample Data --------
    st.markdown(
        """
        <h2 style="
            text-align:center;
            font-size:36px;
            font-weight:700;
            margin-top:10px;
            margin-bottom:25px;
            color:#F9FAFB;
        ">
            📈 Moderation Analytics
        </h2>
        """,
        unsafe_allow_html=True
    )
    data = pd.DataFrame({
        "Category": ["Constructive", "Others", "Offensive", "Harmful", "Cyberbullying","Irony"],
        "Count": [3200, 2320, 1800, 900, 1210, 2780]
    })

    language_data = pd.DataFrame({
        "Language": ["English", "Kiswahili", "Kenyan_Slang"],
        "Count": [3200, 2870, 6140]
    })

    sentiment_data = pd.DataFrame({
        "Sentiment": ["Positive", "Neutral", "Negative"],
        "Count": [5760, 2890, 3560]
    })

    # -------- Row 1 --------

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            data,
            x="Category",
            y="Count",
            color="Category",
            title="Comment Category Distribution",
            color_discrete_sequence=[
                "#16A34A",  # green
                "#DC2626",  # red
                "#F59E0B",
                "#38BDF8",
                "#A78BFA"
            ]
        )

        fig.update_layout(
            plot_bgcolor="#111827",
            paper_bgcolor="#111827",
            font=dict(color="#F9FAFB"),
            margin=dict(l=20, r=20, t=50, b=20)
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig2 = px.pie(
            language_data,
            names="Language",
            values="Count",
            title="Language Distribution",
            color_discrete_sequence=[
                "#16A34A",
                "#DC2626",
                "#9CA3AF"
            ]
        )

        fig2.update_layout(
            plot_bgcolor="#111827",
            paper_bgcolor="#111827",
            font=dict(color="#F9FAFB")
        )

        st.plotly_chart(fig2, use_container_width=True)

    # -------- Row 2 --------

    st.write("")

    fig3 = px.bar(
        sentiment_data,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        title="Sentiment Analysis Overview",
        color_discrete_sequence=[
            "#16A34A",  # positive
            "#9CA3AF",  # neutral
            "#DC2626"   # negative
        ]
    )

    fig3.update_layout(
        plot_bgcolor="#111827",
        paper_bgcolor="#111827",
        font=dict(color="#F9FAFB"),
        margin=dict(l=20, r=20, t=50, b=20)
    )

    st.plotly_chart(fig3, use_container_width=True)

    # -------- footer section--------
    st.markdown("""
    <style>

    /* Footer container */
    .footer{
        margin-top:60px;
        padding:35px;
        background:#111827;
        border-top:3px solid #DC2626;
        text-align:center;
        color:#9CA3AF;
        border-radius:10px 10px 0 0;
    }

    /* footer title */
    .footer-title{
        font-size:18px;
        font-weight:600;
        color:#F9FAFB;
        margin-bottom:10px;
    }

    /* developer names */
    .footer-devs{
        font-size:15px;
        margin-top:8px;
        line-height:1.6;
    }

    /* copyright */
    .footer-copy{
        margin-top:12px;
        font-size:14px;
        color:#6B7280;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">

    <div class="footer-title">
    AI-enabled Kenyan Social Media Comment Moderation System
    </div>

    <div>
    Powered by Scikit-Learn and Hugging Face Transformers
    </div>

    <div class="footer-devs">
    Developed by 
    Stella Kiarie • Doris Mutie • Kumati Dapash • Morvine Otieno
    </div>

    <div class="footer-copy">
    © 2026 All Rights Reserved.
    </div>

    </div>
    """, unsafe_allow_html=True)