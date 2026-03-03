from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, f1_score


class ModelTrainer:
    def __init__(self, model_type="logistic"):
        """
        model_type: "logistic" or "svm"
        """
        if model_type == "logistic":
            self.model = LogisticRegression(
                class_weight="balanced",
                max_iter=1000
            )
        elif model_type == "svm":
            self.model = LinearSVC(
                class_weight="balanced"
            )
        else:
            raise ValueError("model_type must be 'logistic' or 'svm'")

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def evaluate(self, y_test, y_pred):
        report = classification_report(y_test, y_pred)
        weighted_f1 = f1_score(y_test, y_pred, average="weighted")

        return {
            "classification_report": report,
            "weighted_f1": weighted_f1
        }