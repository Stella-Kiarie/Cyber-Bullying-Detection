from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import FeatureUnion


class FeatureEngineer:
    def __init__(
        self,
        test_size=0.2,
        random_state=42,
        max_features=15000
    ):
        self.test_size = test_size
        self.random_state = random_state

        # Word-level TF-IDF
        self.word_vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            max_features=max_features,
            min_df=2,
            max_df=0.95
        )

        # Character-level TF-IDF
        self.char_vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            max_features=max_features
        )

        # Combine both
        self.vectorizer = FeatureUnion([
            ("word", self.word_vectorizer),
            ("char", self.char_vectorizer)
        ])

    def split(self, texts, labels):
        return train_test_split(
            texts,
            labels,
            test_size=self.test_size,
            stratify=labels,
            random_state=self.random_state
        )

    def fit_transform(self, X_train_text):
        return self.vectorizer.fit_transform(X_train_text)

    def transform(self, X_test_text):
        return self.vectorizer.transform(X_test_text)