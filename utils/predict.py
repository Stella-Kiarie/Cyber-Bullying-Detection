import torch
import joblib
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from Data_prep.preprocesssing import TextPreprocessor

# -------------------------------------------------
# DEVICE
# -------------------------------------------------

device = "cpu"


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
# LOAD MODELS (CACHE FOR STREAMLIT)
# -------------------------------------------------

@st.cache_resource
def load_models():

    preprocessor = TextPreprocessor()

    # -----------------------------
    # Classical models
    # -----------------------------

    language_bundle = joblib.load("Models/language_model.pkl")
    sentiment_bundle = joblib.load("Models/sentiment_model.pkl")

    language_model = language_bundle["model"]
    language_fe = language_bundle["feature_engineer"]

    sentiment_model = sentiment_bundle["model"]
    sentiment_fe = sentiment_bundle["feature_engineer"]

    # -----------------------------
    # Tokenizer
    # -----------------------------

    tokenizer = AutoTokenizer.from_pretrained(
        "Models/category_tokenizer"
    )

    # -----------------------------
    # Category models
    # -----------------------------

    neutral_category_model = AutoModelForSequenceClassification.from_pretrained(
        "Models/neutral_category_model"
    )

    negative_category_model = AutoModelForSequenceClassification.from_pretrained(
        "Models/negative_category_model"
    )

    # -----------------------------
    # Subcategory models
    # -----------------------------

    subcategory_models = {

        "Cyberbullying":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Cyberbullying_sub_model"
            ),

        "Offensive":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Offensive_sub_model"
            ),

        "Harmful":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Harmful_sub_model"
            ),

        "Constructive":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Constructive_sub_model"
            ),

        "Others":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Others_sub_model"
            ),

        "Irony":
            AutoModelForSequenceClassification.from_pretrained(
                "Models/Irony_sub_model"
            )
    }

    # -----------------------------
    # Label encoders
    # -----------------------------

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

    with torch.no_grad():
        outputs = model(**inputs)

    pred_id = torch.argmax(outputs.logits).item()

    label = model.config.id2label.get(pred_id, f"LABEL_{pred_id}")

    return label


# -------------------------------------------------
# CATEGORY PREDICTION
# -------------------------------------------------

def predict_category(text, sentiment):

    if sentiment == "Positive":
        return "Constructive"

    elif sentiment == "Neutral":

        label = predict_transformer(
            neutral_category_model,
            text
        )

        return category_mapping.get(label, "Others")

    else:

        label = predict_transformer(
            negative_category_model,
            text
        )

        return category_mapping.get(label, "Cyberbullying")


# -------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------

def analyze_comment(text):

    try:

        text = preprocessor.clean(text)

        # ---------------------------------
        # Language prediction
        # ---------------------------------

        lang_features = language_fe.transform([text])
        language = language_model.predict(lang_features)[0]

        # ---------------------------------
        # Sentiment prediction
        # ---------------------------------

        sent_features = sentiment_fe.transform([text])
        sentiment = sentiment_model.predict(sent_features)[0]

        # ---------------------------------
        # Category prediction
        # ---------------------------------

        category = predict_category(text, sentiment)

        # ---------------------------------
        # Subcategory prediction
        # ---------------------------------

        sub_model = subcategory_models.get(category)

        if sub_model is None:
            return {
                "language": language,
                "sentiment": sentiment,
                "category": category,
                "subcategory": "Unknown"
            }

        sub_encoder = subcategory_encoders[category]

        sub_label = predict_transformer(sub_model, text)

        try:
            sub_id = int(sub_label.replace("LABEL_", ""))
            subcategory = sub_encoder.inverse_transform([sub_id])[0]
        except:
            subcategory = "Unknown"

        return {
            "language": language,
            "sentiment": sentiment,
            "category": category,
            "subcategory": subcategory
        }

    except Exception as e:

        return {
            "language": "Unknown",
            "sentiment": "Unknown",
            "category": "Unknown",
            "subcategory": "Unknown"
        }