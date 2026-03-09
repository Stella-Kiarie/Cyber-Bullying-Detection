# File: Models/feature_engineering_v2.py

import numpy as np
import re
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin


# --------------------------------------------
# Custom Linguistic Feature Extractor
# --------------------------------------------
class LinguisticFeatures(BaseEstimator, TransformerMixin):
    """
    Extracts numeric linguistic features:
    - total words
    - lexical diversity
    - avg word length
    - vowel ratio
    - consonant ratio
    - punctuation ratio
    - emoji count ratio
    """

    def __init__(self):
        # Regex to detect emojis
        self.emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags
                               "]+", flags=re.UNICODE)

    def fit(self, X, y=None):
        return self

    def transform(self, texts):
        features = []

        for text in texts:
            text = str(text).strip()
            words = text.split()
            total_words = len(words)
            unique_words = len(set(words))
            total_chars = len(text)

            lexical_diversity = unique_words / total_words if total_words > 0 else 0
            avg_word_length = np.mean([len(w) for w in words]) if total_words > 0 else 0
            vowel_ratio = sum(c in "aeiouAEIOU" for c in text) / total_chars if total_chars > 0 else 0
            consonant_ratio = sum(c.isalpha() and c.lower() not in "aeiou" for c in text) / total_chars if total_chars > 0 else 0
            punctuation_ratio = sum(c in ".,!?;:()" for c in text) / total_chars if total_chars > 0 else 0
            emoji_ratio = len(self.emoji_pattern.findall(text)) / total_chars if total_chars > 0 else 0

            features.append([
                total_words,
                lexical_diversity,
                avg_word_length,
                vowel_ratio,
                consonant_ratio,
                punctuation_ratio,
                emoji_ratio
            ])

        return np.array(features)


# --------------------------------------------
# Feature Engineering Module
# --------------------------------------------
class FeatureEngineer:

    def __init__(
        self,
        test_size=0.2,
        random_state=42,
        max_word_features=8000,
        max_char_features=20000,
        scale_numeric=True
    ):
        self.test_size = test_size
        self.random_state = random_state
        self.scale_numeric = scale_numeric

        # Word-level TF-IDF
        self.word_vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            max_features=max_word_features,
            min_df=2,
            max_df=0.95
        )

        # Char-level TF-IDF
        self.char_vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            max_features=max_char_features,
            min_df=2
        )

        # Linguistic features
        self.linguistic_features = LinguisticFeatures()
        self.scaler = StandardScaler() if scale_numeric else None

    # --------------------------------------------
    # Train-test split
    # --------------------------------------------
    def split(self, texts, labels):
        return train_test_split(
            texts,
            labels,
            test_size=self.test_size,
            stratify=labels,
            random_state=self.random_state
        )

    # --------------------------------------------
    # Fit & Transform
    # --------------------------------------------
    def fit_transform(self, X_train_text):
        word_features = self.word_vectorizer.fit_transform(X_train_text)
        char_features = self.char_vectorizer.fit_transform(X_train_text)

        linguistic = self.linguistic_features.fit_transform(X_train_text)
        if self.scale_numeric:
            linguistic = self.scaler.fit_transform(linguistic)

        return hstack([word_features, char_features, linguistic])

    # --------------------------------------------
    # Transform
    # --------------------------------------------
    def transform(self, X_test_text):
        word_features = self.word_vectorizer.transform(X_test_text)
        char_features = self.char_vectorizer.transform(X_test_text)

        linguistic = self.linguistic_features.transform(X_test_text)
        if self.scale_numeric:
            linguistic = self.scaler.transform(linguistic)

        return hstack([word_features, char_features, linguistic])