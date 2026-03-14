from training.language_model import LanguageClassifier
from training.sentiment_model import SentimentClassifier


def main():

    print("Training Language Model...")

    lang_model = LanguageClassifier()

    lang_model.train("Data/Data.csv")

    lang_model.save()

    print("\nTraining Sentiment Model...")

    sentiment_model = SentimentClassifier()

    sentiment_model.train("Data/Data.csv")

    sentiment_model.save()


if __name__ == "__main__":
    main()