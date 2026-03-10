import joblib
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, f1_score, confusion_matrix
from Models.Feature_engineering import FeatureEngineer


class LanguageClassifier:

    def __init__(self, test_size=0.2, random_state=42):

        self.feature_engineer = FeatureEngineer(
            test_size=test_size,
            random_state=random_state
        )

        self.model = LinearSVC(
            class_weight="balanced",
            max_iter=30000
        )

    # -----------------------------------
    # Train
    # -----------------------------------
    def train(self, texts, labels):

        X_train_text, X_test_text, y_train, y_test = \
            self.feature_engineer.split(texts, labels)

        X_train = self.feature_engineer.fit_transform(X_train_text)
        X_test = self.feature_engineer.transform(X_test_text)

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        print("\nClassification Report:\n")
        print(classification_report(y_test, y_pred))

        print("Macro F1:",
              f1_score(y_test, y_pred, average="macro"))

        print("Weighted F1:",
              f1_score(y_test, y_pred, average="weighted"))

        print("\nConfusion Matrix:\n")
        print(confusion_matrix(y_test, y_pred))

        return self

    # -----------------------------------
    # Predict
    # -----------------------------------
    def predict(self, text):

        X = self.feature_engineer.transform([text])
        prediction = self.model.predict(X)[0]

        return prediction