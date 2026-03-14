import re
import emoji
from Data_prep.kenyannames import KENYAN_NAMES


class TextPreprocessor:
    def __init__(self):
        """
        Prepares regex pattern for curated Kenyan names.
        Longest names first to prevent partial matching.
        """

        clean_names = sorted(
            [
                re.escape(str(name))
                for name in KENYAN_NAMES
                if name and len(str(name)) > 2
            ],
            key=len,
            reverse=True
        )

        if clean_names:
            self.name_pattern = re.compile(
                r"\b(" + "|".join(clean_names) + r")\b",
                flags=re.IGNORECASE
            )
        else:
            self.name_pattern = None

    # ----------------------------
    # Mask curated Kenyan names
    # ----------------------------
    def mask_names(self, text):
        if self.name_pattern:
            return self.name_pattern.sub("<PERSON>", text)
        return text

    # ----------------------------
    # Mask social media mentions
    # ----------------------------
    def mask_mentions(self, text):
        return re.sub(r"@\w+", "<PERSON>", text)

    # ----------------------------
    # Remove URLs
    # ----------------------------
    def remove_urls(self, text):
        return re.sub(r"https?://\S+|www\.\S+", "", text)

    # ----------------------------
    # Normalize repeated letters
    # mfanooooo → mfanooo
    # ----------------------------
    def normalize_repetition(self, text):
        return re.sub(r"(.)\1{3,}", r"\1\1", text)

    # ----------------------------
    # Remove unwanted characters
    # Keep letters, numbers, emoji tokens, and < >
    # ----------------------------
    def remove_special_characters(self, text):
        return re.sub(r"[^a-zA-Z0-9\s!?.,<>:_-]", "", text)

    # ----------------------------
    # Main cleaning pipeline
    # ----------------------------
    def clean(self, text):

        if not isinstance(text, str) or text.strip() == "":
            return ""

        # Mask sensitive info first
        text = self.mask_names(text)
        text = self.mask_mentions(text)

        # Remove URLs
        text = self.remove_urls(text)

        # Convert emojis to text
        text = emoji.demojize(text, delimiters=(" ", " "))

        # Normalize repeated characters
        text = self.normalize_repetition(text)

        # Lowercase after emoji conversion
        text = text.lower()

        # Remove unwanted characters
        text = self.remove_special_characters(text)

        # Normalize whitespace
        text = re.sub(r"\s+", " ", text).strip()

        return text

    # ----------------------------
    # Apply to dataframe
    # ----------------------------
    def transform(self, df, column="Text"):
        df = df.copy()
        df["clean_text"] = df[column].astype(str).apply(self.clean)
        return df