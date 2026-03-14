import pandas as pd
import joblib

from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score

from inference.Feature_engineering import FeatureEngineer


class SentimentClassifier:

    def __init__(self):

        self.feature_engineer = FeatureEngineer()

        self.model = LinearSVC(
            C=2.0,
            class_weight="balanced",
            max_iter=8000
        )

    def train(self, dataset_path):

        print("Loading sentiment dataset...")

        data = pd.read_csv(dataset_path)

        data = data.dropna()

        texts = data["text"]
        labels = data["sentiment"]

        # shuffle
        data = data.sample(frac=1, random_state=42)

        # split
        X_train, X_test, y_train, y_test = self.feature_engineer.split(
            texts,
            labels
        )

        print("Extracting features...")

        X_train_features = self.feature_engineer.fit_transform(X_train)

        X_test_features = self.feature_engineer.transform(X_test)

        print("Training sentiment model...")

        self.model.fit(X_train_features, y_train)

        preds = self.model.predict(X_test_features)

        acc = accuracy_score(y_test, preds)

        print("\nSentiment Model Accuracy:", acc)

        print("\nClassification Report:\n")
        print(classification_report(y_test, preds))

        return acc

    def save(self, path="Models/sentiment_model.pkl"):

        joblib.dump(
            {
                "model": self.model,
                "feature_engineer": self.feature_engineer
            },
            path
        )

        print(f"Sentiment model saved to: {path}")