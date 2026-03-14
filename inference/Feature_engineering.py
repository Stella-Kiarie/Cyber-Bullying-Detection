import numpy as np
import re

from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin


# --------------------------------------------------
# Custom Linguistic Feature Extractor
# --------------------------------------------------
class LinguisticFeatures(BaseEstimator, TransformerMixin):

    def __init__(self):

        # Swahili indicator words
        self.swahili_words = {
            "ni","hii","kwa","yako","wako","sana",
            "hapo","hiyo","huyu","kwani","lakini",
            "basi","ndio","hapana"
        }

        # Positive sentiment keywords
        self.positive_words = {
            "good","nice","great","love","awesome",
            "amazing","safi","poa","kali","noma",
            "fresh","clean","lit"
        }

        # Negative sentiment keywords
        self.negative_words = {
            "hate","bad","stupid","idiot","fala",
            "mjinga","useless","trash","bure",
            "nonsense","shenzi"
        }

        # Emoji sentiment
        self.positive_emojis = {"🔥","😂","🤣","😍","👏","💯","😁"}
        self.negative_emojis = {"😡","🤬","💔","👎","😤","😭"}

    def fit(self, X, y=None):
        return self

    def transform(self, texts):

        features = []

        for text in texts:

            if not isinstance(text, str):
                text = ""

            words = text.split()
            total_words = len(words)

            # lexical diversity
            unique_words = len(set(words))
            lexical_diversity = unique_words / (total_words + 1e-5)

            # average word length
            avg_word_length = (
                np.mean([len(w) for w in words])
                if total_words > 0 else 0
            )

            # vowel ratio (language signal)
            vowel_ratio = (
                sum(c in "aeiou" for c in text.lower()) /
                (len(text) + 1e-5)
            )

            # punctuation aggression signals
            exclamation_count = text.count("!")
            question_count = text.count("?")

            # uppercase aggression indicator
            uppercase_ratio = (
                sum(c.isupper() for c in text) /
                (len(text) + 1e-5)
            )

            # Swahili keyword ratio
            swahili_ratio = (
                sum(w.lower() in self.swahili_words for w in words) /
                (total_words + 1e-5)
            )

            # sentiment keyword ratios
            positive_ratio = (
                sum(w.lower() in self.positive_words for w in words) /
                (total_words + 1e-5)
            )

            negative_ratio = (
                sum(w.lower() in self.negative_words for w in words) /
                (total_words + 1e-5)
            )

            # emoji signals
            positive_emoji_count = sum(
                e in text for e in self.positive_emojis
            )

            negative_emoji_count = sum(
                e in text for e in self.negative_emojis
            )

            # elongated words (anger / emphasis)
            elongated_words = len(
                re.findall(r"(.)\1{2,}", text)
            )

            features.append([
                total_words,
                lexical_diversity,
                avg_word_length,
                vowel_ratio,
                exclamation_count,
                question_count,
                uppercase_ratio,
                swahili_ratio,
                positive_ratio,
                negative_ratio,
                positive_emoji_count,
                negative_emoji_count,
                elongated_words
            ])

        return np.array(features)


# --------------------------------------------------
# Main Feature Engineering Pipeline
# --------------------------------------------------
class FeatureEngineer:

    def __init__(
        self,
        test_size=0.2,
        random_state=42,
        max_word_features=15000,
        max_char_features=50000
    ):

        self.test_size = test_size
        self.random_state = random_state

        # Word-level TF-IDF
        self.word_vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1,3),
            max_features=max_word_features,
            min_df=2,
            max_df=0.9
        )

        # Character-level TF-IDF (excellent for Sheng)
        self.char_vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(3,6),
            max_features=max_char_features,
            min_df=2
        )

        self.linguistic_features = LinguisticFeatures()
        self.scaler = StandardScaler()

    # --------------------------------------------------
    # Train-Test Split
    # --------------------------------------------------
    def split(self, texts, labels):

        return train_test_split(
            texts,
            labels,
            test_size=self.test_size,
            stratify=labels,
            random_state=self.random_state
        )

    # --------------------------------------------------
    # Fit & Transform (Training)
    # --------------------------------------------------
    def fit_transform(self, X_train_text):

        word_features = self.word_vectorizer.fit_transform(X_train_text)

        char_features = self.char_vectorizer.fit_transform(X_train_text)

        linguistic = self.linguistic_features.fit_transform(X_train_text)

        linguistic_scaled = self.scaler.fit_transform(linguistic)

        return hstack([
            word_features,
            char_features,
            linguistic_scaled
        ])

    # --------------------------------------------------
    # Transform (Inference)
    # --------------------------------------------------
    def transform(self, X_test_text):

        word_features = self.word_vectorizer.transform(X_test_text)

        char_features = self.char_vectorizer.transform(X_test_text)

        linguistic = self.linguistic_features.transform(X_test_text)

        linguistic_scaled = self.scaler.transform(linguistic)

        return hstack([
            word_features,
            char_features,
            linguistic_scaled
        ])