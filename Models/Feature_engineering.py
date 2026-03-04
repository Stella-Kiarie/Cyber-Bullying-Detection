import numpy as np
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin


# --------------------------------------------
# Custom Linguistic Feature Extractor
# --------------------------------------------
class LinguisticFeatures(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, texts):

        features = []

        for text in texts:
            words = text.split()

            total_words = len(words)
            unique_words = len(set(words))

            lexical_diversity = (
                unique_words / total_words
                if total_words > 0 else 0
            )

            avg_word_length = (
                np.mean([len(w) for w in words])
                if total_words > 0 else 0
            )

            vowel_ratio = (
                sum(c in "aeiou" for c in text.lower())
                / len(text)
                if len(text) > 0 else 0
            )

            features.append([
                total_words,
                lexical_diversity,
                avg_word_length,
                vowel_ratio
            ])

        return np.array(features)


# --------------------------------------------
# Main Feature Engineer
# --------------------------------------------
class FeatureEngineer:

    def __init__(
        self,
        test_size=0.2,
        random_state=42,
        max_word_features=8000,
        max_char_features=20000
    ):

        self.test_size = test_size
        self.random_state = random_state

        # Word-level TF-IDF (clean + light)
        self.word_vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            max_features=max_word_features,
            min_df=2,
            max_df=0.95
        )

        # Character-level TF-IDF (VERY IMPORTANT for Sheng)
        self.char_vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(3, 5),
            max_features=max_char_features,
            min_df=2
        )

        self.linguistic_features = LinguisticFeatures()
        self.scaler = StandardScaler()

    # --------------------------------------------
    # Train-test split (Stratified)
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
        linguistic_scaled = self.scaler.fit_transform(linguistic)

        return hstack([word_features, char_features, linguistic_scaled])

    # --------------------------------------------
    # Transform
    # --------------------------------------------
    def transform(self, X_test_text):

        word_features = self.word_vectorizer.transform(X_test_text)
        char_features = self.char_vectorizer.transform(X_test_text)

        linguistic = self.linguistic_features.transform(X_test_text)
        linguistic_scaled = self.scaler.transform(linguistic)

        return hstack([word_features, char_features, linguistic_scaled])