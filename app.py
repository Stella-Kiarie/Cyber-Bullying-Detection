import streamlit as st
import joblib
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

st.title("Multilingual Cyberbullying Detection")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("category_tokenizer")

# Load sklearn models
language_data = joblib.load("Models/language_model.pkl")
sentiment_data = joblib.load("Models/sentiment_model.pkl")

language_model = language_data["model"]
language_fe = language_data["feature_engineer"]

sentiment_model = sentiment_data["model"]
sentiment_fe = sentiment_data["feature_engineer"]

# Load transformer models
neutral_model = AutoModelForSequenceClassification.from_pretrained(
    "models/neutral_category_model"
)

negative_model = AutoModelForSequenceClassification.from_pretrained(
    "models/negative_category_model"
)

def predict_language(text):

    X = language_fe.transform([text])
    return language_model.predict(X)[0]


def predict_sentiment(text):

    X = sentiment_fe.transform([text])
    return sentiment_model.predict(X)[0]

def predict_transformer(model, text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    with torch.no_grad():
        outputs = model(**inputs)

    pred = torch.argmax(outputs.logits).item()

    return pred

sentiment_labels = {
    0: "Positive",
    1: "Neutral",
    2: "Negative"
}

neutral_labels = {
    0: "Others",
    1: "Misinformation"
}

negative_labels = {
    0: "Cyberbullying",
    1: "Offensive",
    2: "Harmful",
    3: "Irony"
}
text = st.text_area("Enter a comment")

if st.button("Analyze Comment"):

    # Step 1 — Language
    language = predict_language(text)

    # Step 2 — Sentiment
    sentiment = predict_sentiment(text)

    # Step 3 — Category routing
    language = predict_language(text)

    sentiment = predict_sentiment(text)

    if sentiment == "Positive":

        category = "Constructive"

    elif sentiment == "Neutral":

        cat_pred = predict_transformer(neutral_model, text)
        category = neutral_labels[cat_pred]

    else:

        cat_pred = predict_transformer(negative_model, text)
        category = negative_labels[cat_pred]

    st.subheader("Prediction Results")

    st.write("Language:", language)
    st.write("Sentiment:", sentiment)
    st.write("Category:", category)