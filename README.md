# 🇰🇪 VibeCheck Kenya

### AI-Powered Cyberbullying Detection for Kenyan Social Media

---

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Machine%20Learning-NLP-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" />
</p>

---

## 🌍 Live Demo

👉 **Try it here:**
https://vibe-check-kenya.streamlit.app/

---

## 📸 Application Preview

### 🏠 Home Page
![Home](Images/homepage.png)

### 📊 Comment Analysis
![Analysis](Images/analysis.png)
### 📂 Batch Processing

*(Add screenshot here)*

---

## 🚀 Overview

**VibeCheck Kenya** is an AI-powered moderation system designed to detect cyberbullying in Kenyan social media.

It understands **English, Kiswahili, and Sheng**, making it effective for real-world Kenyan online conversations.

---

## 🎯 Problem

Traditional moderation tools:

* Focus only on English
* Fail to detect Sheng/slang
* Miss harmful content in Kenyan conversations

---

## 💡 Solution

A **hierarchical AI pipeline** that:

* Detects language
* Analyzes sentiment
* Classifies comments
* Identifies cyberbullying types

---

## 🧠 System Workflow

<p align="center">

<pre>
      Input Comment
            ↓
   Language Detection
            ↓
   Sentiment Analysis
            ↓
  Category Classification
            ↓
 Subcategory Detection
            ↓
        Final Output
</pre>

</p>

---

## 🛠 Key Features

* 🔍 Real-time comment analysis
* 📂 Batch moderation (CSV upload)
* 🤖 AI assistant for explanations
* 📊 Interactive analytics dashboard
* ⚡ Toxicity scoring system

---

## 📊 Model Architecture

| Component               | Model              |
| ----------------------- | ------------------ |
| Language Detection      | LinearSVC          |
| Sentiment Analysis      | LinearSVC          |
| Category Classification | XLM-RoBERTa        |
| Subcategory Detection   | Transformer Models |

---

## 🌐 Supported Languages

* English
* Kiswahili
* Kenyan Sheng

---

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **ML:** Scikit-learn
* **DL:** Hugging Face Transformers
* **Visualization:** Plotly
* **Data:** Pandas

---

## 📦 Installation

```bash
git clone https://github.com/your-username/vibecheck-kenya.git
cd vibecheck-kenya
pip install -r requirements.txt
```

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```text
├── app.py
├── inference/
├── models/
├── data/
├── notebooks/
├── requirements.txt
└── README.md
```

---

## 👥 Team

| Name           | Role                        |
| -------------- | --------------------------- |
| Stella Kiarie  | Project Lead & ML Developer |
| Kumati Dapash  | Machine Learning Engineer   |
| Morvine Otieno | Data Analyst                |
| Doris Mutie    | Deployment & UI Developer   |

---

## 🚀 Future Improvements

* End-to-end automated ML pipeline
* Improved sarcasm detection
* Cross-platform integration (TikTok, X)
* Real-time moderation API

---

## 📜 License

Educational use only

---

## 🙌 Acknowledgements

* Moringa School
* Hugging Face
* YouTube Data API

---

