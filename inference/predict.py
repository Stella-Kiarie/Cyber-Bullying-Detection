import torch
import joblib
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from inference.preprocesssing import TextPreprocessor


# -------------------------------------------------
# DEVICE
# -------------------------------------------------

device = torch.device("cpu")


# -------------------------------------------------
# CATEGORY LABEL FIX
# -------------------------------------------------

category_mapping = {
    "LABEL_0": "Constructive",
    "LABEL_1": "Cyberbullying",
    "LABEL_2": "Harmful",
    "LABEL_3": "Irony",
    "LABEL_4": "Offensive",
    "LABEL_5": "Others"
}


# -------------------------------------------------
# LOAD MODELS
# -------------------------------------------------

@st.cache_resource
def load_models():

    preprocessor = TextPreprocessor()

    # Classical ML models
    language_bundle = joblib.load("Models/language_model.pkl")
    sentiment_bundle = joblib.load("Models/sentiment_model.pkl")

    language_model = language_bundle["model"]
    language_fe = language_bundle["feature_engineer"]

    sentiment_model = sentiment_bundle["model"]
    sentiment_fe = sentiment_bundle["feature_engineer"]

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("Models/category_tokenizer")

    # Category models
    neutral_category_model = AutoModelForSequenceClassification.from_pretrained(
        "Models/neutral_category_model"
    ).to(device)

    negative_category_model = AutoModelForSequenceClassification.from_pretrained(
        "Models/negative_category_model"
    ).to(device)

    neutral_category_model.eval()
    negative_category_model.eval()

    # Subcategory models
    subcategory_models = {

        "Cyberbullying":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Cyberbullying_sub_model"
            ).to(device),

        "Offensive":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Offensive_sub_model"
            ).to(device),

        "Harmful":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Harmful_sub_model"
            ).to(device),

        "Constructive":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Constructive_sub_model"
            ).to(device),

        "Others":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Others_sub_model"
            ).to(device),

        "Irony":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Irony_sub_model"
            ).to(device)
    }

    for m in subcategory_models.values():
        m.eval()

    # Label encoders
    subcategory_encoders = {

        "Cyberbullying":
            joblib.load("Models/Cyberbullying_sub_model/label_encoder.pkl"),

        "Offensive":
            joblib.load("Models/Offensive_sub_model/label_encoder.pkl"),

        "Harmful":
            joblib.load("Models/Harmful_sub_model/label_encoder.pkl"),

        "Constructive":
            joblib.load("Models/Constructive_sub_model/label_encoder.pkl"),

        "Others":
            joblib.load("Models/Others_sub_model/label_encoder.pkl"),

        "Irony":
            joblib.load("Models/Irony_sub_model/label_encoder.pkl")
    }

    return (
        preprocessor,
        language_model,
        language_fe,
        sentiment_model,
        sentiment_fe,
        tokenizer,
        neutral_category_model,
        negative_category_model,
        subcategory_models,
        subcategory_encoders
    )


(
    preprocessor,
    language_model,
    language_fe,
    sentiment_model,
    sentiment_fe,
    tokenizer,
    neutral_category_model,
    negative_category_model,
    subcategory_models,
    subcategory_encoders
) = load_models()


# -------------------------------------------------
# TRANSFORMER PREDICTION
# -------------------------------------------------

def predict_transformer(model, text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    )

    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probs = torch.softmax(logits, dim=1)

    pred_id = torch.argmax(probs).item()
    confidence = probs[0][pred_id].item()

    label = model.config.id2label.get(pred_id, f"LABEL_{pred_id}")

    return label, confidence


# -------------------------------------------------
# CATEGORY PREDICTION
# -------------------------------------------------

def predict_category(text, sentiment):

    if sentiment == "Positive":
        return "Constructive", 1.0

    elif sentiment == "Neutral":

        label, conf = predict_transformer(
            neutral_category_model,
            text
        )

        return category_mapping.get(label, "Others"), conf

    else:

        label, conf = predict_transformer(
            negative_category_model,
            text
        )

        return category_mapping.get(label, "Cyberbullying"), conf


# -------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------

def analyze_comment(text):

    try:

        text = preprocessor.clean(text)

        # Language prediction
        lang_features = language_fe.transform([text])
        language = language_model.predict(lang_features)[0]

        # Sentiment prediction
        sent_features = sentiment_fe.transform([text])
        sentiment = sentiment_model.predict(sent_features)[0]

        # Category prediction
        category, confidence = predict_category(text, sentiment)

        # Subcategory prediction
        sub_model = subcategory_models.get(category)
        encoder = subcategory_encoders.get(category)

        subcategory = "Unknown"

        if sub_model and encoder:

            sub_label, _ = predict_transformer(sub_model, text)

            try:
                sub_id = int(sub_label.replace("LABEL_", ""))
                subcategory = encoder.inverse_transform([sub_id])[0]
            except:
                subcategory = "Unknown"

        return {
            "language": language,
            "sentiment": sentiment,
            "category": category,
            "subcategory": subcategory,
            "confidence": round(confidence, 3)
        }

    except Exception:

        return {
            "language": "Unknown",
            "sentiment": "Unknown",
            "category": "Unknown",
            "subcategory": "Unknown",
            "confidence": 0
        }