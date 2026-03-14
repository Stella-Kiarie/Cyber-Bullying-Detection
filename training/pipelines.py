# Models/pipelines.py
import numpy as np
from scipy.sparse import hstack
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import classification_report, f1_score, confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------
# Linguistic Features
# -----------------------------
class LinguisticFeatures(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, texts):
        features = []
        for text in texts:
            words = text.split()
            total_words = len(words)
            unique_words = len(set(words))
            lexical_diversity = unique_words / total_words if total_words else 0
            avg_word_length = np.mean([len(w) for w in words]) if total_words else 0
            vowel_ratio = sum(c in "aeiou" for c in text.lower()) / len(text) if len(text) else 0
            features.append([total_words, lexical_diversity, avg_word_length, vowel_ratio])
        return np.array(features)

# -----------------------------
# Feature Engineer
# -----------------------------
class FeatureEngineer:
    def __init__(self, test_size=0.2, random_state=42, max_word_features=8000, max_char_features=20000, scale_numeric=True):
        self.test_size = test_size
        self.random_state = random_state
        self.scale_numeric = scale_numeric

        self.word_vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            max_features=max_word_features,
            min_df=2,
            max_df=0.95
        )
        self.char_vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            max_features=max_char_features,
            min_df=2
        )
        self.linguistic_features = LinguisticFeatures()
        self.scaler = StandardScaler()

    def split(self, texts, labels):
        return train_test_split(
        texts,
        labels,
        test_size=self.test_size,
        random_state=self.random_state,
        # stratify removed
    )

    def fit_transform(self, X_train_text):
        word_features = self.word_vectorizer.fit_transform(X_train_text)
        char_features = self.char_vectorizer.fit_transform(X_train_text)
        linguistic = self.linguistic_features.fit_transform(X_train_text)
        linguistic_scaled = self.scaler.fit_transform(linguistic) if self.scale_numeric else linguistic
        return hstack([word_features, char_features, linguistic_scaled])

    def transform(self, X_test_text):
        word_features = self.word_vectorizer.transform(X_test_text)
        char_features = self.char_vectorizer.transform(X_test_text)
        linguistic = self.linguistic_features.transform(X_test_text)
        linguistic_scaled = self.scaler.transform(linguistic) if self.scale_numeric else linguistic
        return hstack([word_features, char_features, linguistic_scaled])

# -----------------------------
# Generic Pipeline Base Class
# -----------------------------
class BasePipeline:
    def __init__(self, model_type="svc", **kwargs):
        self.fe = FeatureEngineer(**kwargs)
        if model_type.lower() == "svc":
            self.model = LinearSVC(class_weight="balanced", max_iter=30000)
        elif model_type.lower() == "rf":
            self.model = RandomForestClassifier(n_estimators=200, max_depth=None, class_weight="balanced", n_jobs=-1, random_state=kwargs.get("random_state", 42))
        else:
            raise ValueError("model_type must be 'svc' or 'rf'")
        self.label_encoder = LabelEncoder()

    def train(self, texts, labels):
        y_encoded = self.label_encoder.fit_transform(labels)
        X_train_text, X_test_text, y_train, y_test = self.fe.split(texts, y_encoded)
        X_train = self.fe.fit_transform(X_train_text)
        X_test = self.fe.transform(X_test_text)
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        print("\nClassification Report:\n")
        print(classification_report(y_test, y_pred, target_names=self.label_encoder.classes_))
        print("Weighted F1:", f1_score(y_test, y_pred, average="weighted"))
        print("Macro F1:", f1_score(y_test, y_pred, average="macro"))
        print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
        return self

    def predict(self, texts):
        X = self.fe.transform(texts if isinstance(texts, list) else [texts])
        preds = self.model.predict(X)
        return self.label_encoder.inverse_transform(preds)

# -----------------------------
# Specific Pipelines
# -----------------------------
class LanguagePipeline(BasePipeline):
    def __init__(self, model_type="svc", **kwargs):
        super().__init__(model_type=model_type, **kwargs)

class SentimentPipeline(BasePipeline):
    def __init__(self, model_type="rf", **kwargs):
        super().__init__(model_type=model_type, **kwargs)

class CategoryPipeline(BasePipeline):
    def __init__(self, model_type="rf", **kwargs):
        super().__init__(model_type=model_type, **kwargs)

class SubcategoryPipeline(BasePipeline):
    def __init__(self, model_type="rf", **kwargs):
        super().__init__(model_type=model_type, **kwargs)