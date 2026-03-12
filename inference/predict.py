import torch
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import hf_hub_download

from inference.preprocesssing import TextPreprocessor


# -------------------------------------------------
# DEVICE
# -------------------------------------------------

device = torch.device("cpu")


# -------------------------------------------------
# HUGGING FACE REPO
# -------------------------------------------------

HF_REPO = "ste-pp/kenyan-cyberbullying-models"


# -------------------------------------------------
# CATEGORY LABEL MAPPING
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
# LOAD CLASSICAL MODELS
# -------------------------------------------------

def load_classical_models():

    preprocessor = TextPreprocessor()

    language_path = hf_hub_download(
        repo_id=HF_REPO,
        filename="language_model.pkl"
    )

    sentiment_path = hf_hub_download(
        repo_id=HF_REPO,
        filename="sentiment_model.pkl"
    )

    language_bundle = joblib.load(language_path)
    sentiment_bundle = joblib.load(sentiment_path)

    language_model = language_bundle["model"]
    language_fe = language_bundle["feature_engineer"]

    sentiment_model = sentiment_bundle["model"]
    sentiment_fe = sentiment_bundle["feature_engineer"]

    return (
        preprocessor,
        language_model,
        language_fe,
        sentiment_model,
        sentiment_fe
    )


# -------------------------------------------------
# LOAD CATEGORY MODELS
# -------------------------------------------------
def load_category_models():

    tokenizer = AutoTokenizer.from_pretrained(
        HF_REPO,
        subfolder="category_tokenizer"
    )

    neutral_category_model = AutoModelForSequenceClassification.from_pretrained(
        HF_REPO,
        subfolder="neutral_category_model"
    ).to(device)

    negative_category_model = AutoModelForSequenceClassification.from_pretrained(
        HF_REPO,
        subfolder="negative_category_model"
    ).to(device)

    neutral_category_model.eval()
    negative_category_model.eval()

    return tokenizer, neutral_category_model, negative_category_model


# -------------------------------------------------
# LOAD SUBCATEGORY MODELS + ENCODERS
# -------------------------------------------------

def load_subcategory_models():

    sub_models = {}
    sub_encoders = {}

    categories = [
        "Constructive",
        "Cyberbullying",
        "Harmful",
        "Irony",
        "Offensive",
        "Others"
    ]

    for cat in categories:

        model = AutoModelForSequenceClassification.from_pretrained(
            HF_REPO,
            subfolder=f"{cat}_sub_model"
        ).to(device)

        model.eval()

        encoder_path = hf_hub_download(
            repo_id=HF_REPO,
            filename=f"{cat}_sub_model/label_encoder.pkl"
        )

        encoder = joblib.load(encoder_path)

        sub_models[cat] = model
        sub_encoders[cat] = encoder

    return sub_models, sub_encoders


# -------------------------------------------------
# INITIALIZE MODELS
# -------------------------------------------------

(
    preprocessor,
    language_model,
    language_fe,
    sentiment_model,
    sentiment_fe
) = load_classical_models()

tokenizer, neutral_category_model, negative_category_model = load_category_models()

subcategory_models, subcategory_encoders = load_subcategory_models()


# -------------------------------------------------
# TRANSFORMER PREDICTION
# -------------------------------------------------

def predict_transformer(model, tokenizer, text):

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

    label = f"LABEL_{pred_id}"

    return label, confidence


# -------------------------------------------------
# PREPROCESS TEXT
# -------------------------------------------------

def preprocess_text(text):

    return preprocessor.clean(text)


# -------------------------------------------------
# LANGUAGE PREDICTION
# -------------------------------------------------

def predict_language(text):

    features = language_fe.transform([text])

    return language_model.predict(features)[0]


# -------------------------------------------------
# SENTIMENT PREDICTION
# -------------------------------------------------

def predict_sentiment(text):

    features = sentiment_fe.transform([text])

    return sentiment_model.predict(features)[0]


# -------------------------------------------------
# CATEGORY PREDICTION
# -------------------------------------------------

def predict_category(text, sentiment):

    if sentiment == "Positive":
        return "Constructive", 1.0

    if sentiment == "Neutral":

        label, conf = predict_transformer(
            neutral_category_model,
            tokenizer,
            text
        )

    else:

        label, conf = predict_transformer(
            negative_category_model,
            tokenizer,
            text
        )

    category = category_mapping.get(label, "Others")

    return category, conf


# -------------------------------------------------
# SUBCATEGORY PREDICTION
# -------------------------------------------------

def predict_subcategory(text, category):

    model = subcategory_models.get(category)
    encoder = subcategory_encoders.get(category)

    if model is None or encoder is None:
        return "Unknown"

    label, _ = predict_transformer(model, tokenizer, text)

    sub_id = int(label.replace("LABEL_", ""))

    subcategory = encoder.inverse_transform([sub_id])[0]

    return subcategory


# -------------------------------------------------
# MAIN PIPELINE
# -------------------------------------------------

def analyze_comment(text):

    text = preprocess_text(text)

    language = predict_language(text)

    sentiment = predict_sentiment(text)

    category, confidence = predict_category(text, sentiment)

    subcategory = predict_subcategory(text, category)

    return {
        "language": language,
        "sentiment": sentiment,
        "category": category,
        "subcategory": subcategory,
        "confidence": round(confidence, 3)
    }


# -------------------------------------------------
# TEST PIPELINE
# -------------------------------------------------

if __name__ == "__main__":

    test_text = "You are stupid"

    result = analyze_comment(test_text)

    print(result)