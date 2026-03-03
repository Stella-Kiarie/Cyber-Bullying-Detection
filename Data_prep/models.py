from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, f1_score
import pandas as pd


class ModelComparison:
    def __init__(self):
        """
        Initialize multiple models for comparison.
        """
        self.models = {
            "Logistic Regression": LogisticRegression(
                class_weight="balanced",
                max_iter=1000
            ),
            "Linear SVM": LinearSVC(
                class_weight="balanced"
            ),
            "Naive Bayes": MultinomialNB()
        }

        self.results = {}

    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        """
        Train each model and evaluate performance.
        """
        for name, model in self.models.items():
            print(f"\nTraining {name}...")

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            weighted_f1 = f1_score(y_test, y_pred, average="weighted")
            macro_f1 = f1_score(y_test, y_pred, average="macro")

            self.results[name] = {
                "weighted_f1": weighted_f1,
                "macro_f1": macro_f1,
                "classification_report": classification_report(y_test, y_pred)
            }

        return self.results

    def get_summary(self):
        """
        Return summary DataFrame of model performance.
        """
        summary = []

        for name, metrics in self.results.items():
            summary.append({
                "Model": name,
                "Weighted F1": metrics["weighted_f1"],
                "Macro F1": metrics["macro_f1"]
            })

        return pd.DataFrame(summary).sort_values(
            by="Weighted F1",
            ascending=False
        )