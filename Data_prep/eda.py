import pandas as pd
import plotly.express as px
from collections import Counter
import re


class EDA:
    """
    Exploratory Data Analysis Module
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.data = dataframe

    # 1️⃣ Dataset Overview
    def dataset_overview(self):
        print("\n📊 DATASET OVERVIEW")
        print("=" * 60)
        print(f"Shape: {self.data.shape}")
        print("\nColumns:")
        print(self.data.columns.tolist())
        print("\nData Types:")
        print(self.data.dtypes)
        print("\nMissing Values:")
        print(self.data.isnull().sum())

    # 2️⃣ Target Distribution (Category or Sentiment)
    def target_distribution(self, column_name="category"):
        if column_name not in self.data.columns:
            print(f"{column_name} not found.")
            return

        counts = self.data[column_name].value_counts().reset_index()
        counts.columns = [column_name, "count"]

        fig = px.bar(
            counts,
            x=column_name,
            y="count",
            title=f"Distribution of {column_name}"
        )
        fig.show()

        print("\nClass Percentages:")
        print((self.data[column_name].value_counts(normalize=True) * 100).round(2))

    # 3️⃣ Subcategory Analysis
    def subcategory_analysis(self):
        if "subcategory" not in self.data.columns:
            print("subcategory column not found.")
            return

        counts = self.data["subcategory"].value_counts().reset_index()
        counts.columns = ["subcategory", "count"]

        fig = px.bar(
            counts,
            x="subcategory",
            y="count",
            title="Subcategory Distribution"
        )
        fig.show()

    # 4️⃣ Text Length Analysis
    def text_length_analysis(self, text_column="text"):
        if text_column not in self.data.columns:
            print(f"{text_column} not found.")
            return

        self.data["text_length"] = self.data[text_column].astype(str).apply(len)

        fig = px.histogram(
            self.data,
            x="text_length",
            nbins=50,
            title="Text Length Distribution"
        )
        fig.show()

        print("\nText Length Summary:")
        print(self.data["text_length"].describe())

    # 5️⃣ Word Frequency Analysis
    def word_frequency_analysis(self, text_column="text", top_n=20):
        if text_column not in self.data.columns:
            print(f"{text_column} not found.")
            return

        text_series = self.data[text_column].dropna().astype(str)

        words = []
        for text in text_series:
            text = re.sub(r"[^a-zA-Z\s]", "", text.lower())
            words.extend(text.split())

        word_counts = Counter(words)
        common_words = word_counts.most_common(top_n)

        df_words = pd.DataFrame(common_words, columns=["word", "count"])

        fig = px.bar(
            df_words,
            x="word",
            y="count",
            title=f"Top {top_n} Most Frequent Words"
        )
        fig.show()

        return df_words

    # 6️⃣ Linguistic Feature Exploration
    def linguistic_features(self, text_column="text"):
        if text_column not in self.data.columns:
            print(f"{text_column} not found.")
            return

        self.data["word_count"] = self.data[text_column].astype(str).apply(lambda x: len(x.split()))
        self.data["avg_word_length"] = self.data[text_column].astype(str).apply(
            lambda x: sum(len(word) for word in x.split()) / len(x.split()) if len(x.split()) > 0 else 0
        )

        print("\n📚 Linguistic Feature Summary")
        print("=" * 60)
        print(self.data[["word_count", "avg_word_length"]].describe())

    # 7️⃣ Engagement Insights (Likes Only)
    def engagement_insights(self):
        if "likes" not in self.data.columns:
            print("No engagement column found.")
            return

        print("\n📈 Engagement Insights (Likes)")
        print("=" * 60)
        print(self.data["likes"].describe())

        fig = px.histogram(
            self.data,
            x="likes",
            nbins=40,
            title="Likes Distribution"
        )
        fig.show()

    # 8️⃣ Language Insights
    def language_insights(self):
        if "language" not in self.data.columns:
            print("language column not found.")
            return

        counts = self.data["language"].value_counts().reset_index()
        counts.columns = ["language", "count"]

        fig = px.pie(
            counts,
            names="language",
            values="count",
            title="Language Distribution"
        )
        fig.show()

        print("\nLanguage Percentages:")
        print((self.data["language"].value_counts(normalize=True) * 100).round(2))

    # 9️⃣ Key Findings Summary
    def key_findings(self):
        print("\n🔎 KEY FINDINGS SUMMARY")
        print("=" * 60)

        print(f"Total Samples: {len(self.data)}")

        if "category" in self.data.columns:
            print("\nTop Category:")
            print(self.data["category"].value_counts().idxmax())

        if "sentiment" in self.data.columns:
            print("\nTop Sentiment:")
            print(self.data["sentiment"].value_counts().idxmax())

        if "language" in self.data.columns:
            print("\nMost Common Language:")
            print(self.data["language"].value_counts().idxmax())

        if "text" in self.data.columns:
            avg_length = self.data["text"].astype(str).apply(len).mean()
            print(f"\nAverage Text Length: {avg_length:.2f} characters")