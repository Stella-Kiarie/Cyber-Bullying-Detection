from Data_prep.loader import DataLoader
from Data_prep.preprocesssing import TextPreprocessor
from Data_prep.Feature_engineering import FeatureEngineer
from Data_prep.modelling import ModelTrainer


def main():

    # 1️⃣ Load Data
    print("Loading data...")
    loader=DataLoader('Notebooks/Labelled_data.csv')
    data= loader.load_data()

    # 2️⃣ Preprocess
    print("Preprocessing text...")
    preprocessor = TextPreprocessor()
    df = preprocessor.transform(data, column="Text")

    # 3️⃣ Feature Engineering
    print("Running feature engineering...")
    fe = FeatureEngineer()

    X_train_text, X_test_text, y_train, y_test = fe.split(
        df["clean_text"],
        df["category"]
    )

    X_train = fe.fit_transform(X_train_text)
    X_test = fe.transform(X_test_text)

    print("Train shape:", X_train.shape)
    print("Test shape:", X_test.shape)

    # 4️⃣ Train Model
    print("Training model...")
    trainer = ModelTrainer(model_type="logistic")
    trainer.train(X_train, y_train)

    # 5️⃣ Predict
    print("Evaluating model...")
    y_pred = trainer.predict(X_test)

    results = trainer.evaluate(y_test, y_pred)

    print("\nClassification Report:\n")
    print(results["classification_report"])
    print("Weighted F1:", results["weighted_f1"])


if __name__ == "__main__":
    main()