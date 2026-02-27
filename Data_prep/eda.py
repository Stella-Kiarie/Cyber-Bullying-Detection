import pandas as pd
import plotly.express as px
import re


class EDA:
    """
    Exploratory Data Analysis Module
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.data = dataframe.copy()

    # --------------------------------------------------
    # 1️⃣ Dataset Overview
    # --------------------------------------------------
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

    # --------------------------------------------------
    # 2️⃣ Target Distribution
    # --------------------------------------------------
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
            title=f"Distribution of {column_name}",
            text="count"
        )
        fig.show()

        print("\nClass Percentages:")
        print((self.data[column_name].value_counts(normalize=True) * 100).round(2))

    # --------------------------------------------------
    # 3️⃣ Subcategory Analysis
    # --------------------------------------------------
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
            title="Subcategory Distribution",
            text="count"
        )
        fig.show()

    # --------------------------------------------------
    # 4️⃣ Text Length Analysis
    # --------------------------------------------------
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

    # --------------------------------------------------
    # 5️⃣ Language Insights
    # --------------------------------------------------
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

    # --------------------------------------------------
    # 6️⃣ Peak Posting Time Analysis (Kenyan Context)
    # --------------------------------------------------
    def peak_posting_times(self, date_column="published_at"):
        """
        Analyze peak posting times in Kenyan context (EAT - UTC+3).
        """

        if date_column not in self.data.columns:
            print(f"{date_column} column not found.")
            return

        # Convert to datetime safely
        self.data[date_column] = pd.to_datetime(
            self.data[date_column], errors="coerce"
        )

        df = self.data.dropna(subset=[date_column]).copy()

        # Handle timezone conversion
        if df[date_column].dt.tz is None:
            df[date_column] = (
                df[date_column]
                .dt.tz_localize("UTC")
                .dt.tz_convert("Africa/Nairobi")
            )
        else:
            df[date_column] = df[date_column].dt.tz_convert("Africa/Nairobi")

        # Extract hour
        df["hour"] = df[date_column].dt.hour

        # Count posts per hour
        hour_counts = df["hour"].value_counts().sort_index()

        # Plot
        fig = px.line(
            x=hour_counts.index,
            y=hour_counts.values,
            title="Peak Posting Hours (Kenyan Time - EAT)",
            labels={"x": "Hour of Day (24h)", "y": "Number of Posts"}
        )

        fig.update_traces(mode="lines+markers")
        fig.show()

        print("\n🕒 Posting Activity by Hour")
        print("=" * 60)
        print(hour_counts)

        print("\n🔥 Peak Posting Hour:")
        print(f"{hour_counts.idxmax()}:00")

        # Weekend vs Weekday comparison
        df["day_name"] = df[date_column].dt.day_name()
        df["is_weekend"] = df["day_name"].isin(["Saturday", "Sunday"])

        weekend_counts = df.groupby("is_weekend")["hour"].count()

        print("\n📅 Weekend vs Weekday Activity")
        print("=" * 60)
        print(weekend_counts)

        return hour_counts

    # --------------------------------------------------
    # 7️⃣ Key Findings Summary
    # --------------------------------------------------
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