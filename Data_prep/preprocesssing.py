import re
import emoji
from Data_prep.kenyannames import KENYAN_NAMES


class TextPreprocessor:
    def __init__(self):
        # Prepare Kenyan names pattern (longest first)
        clean_names = sorted(
            [
                re.escape(str(n))
                for n in KENYAN_NAMES
                if n and len(str(n)) > 2
            ],
            key=len,
            reverse=True
        )

        self.kenyan_name_pattern = re.compile(
            r"\b(" + "|".join(clean_names) + r")\b",
            flags=re.IGNORECASE
        )

    # Mask curated Kenyan names
    def mask_kenyan_names(self, text):
        return self.kenyan_name_pattern.sub("<PERSON>", text)

    # Mask social media mentions
    def mask_mentions(self, text):
        return re.sub(r"@\w+", "<PERSON>", text)

    # Remove URLs
    def remove_urls(self, text):
        return re.sub(r"https?://\S+|www\.\S+", "", text)

    # Keep emoji underscores and < >
    def remove_special_characters(self, text):
        return re.sub(r"[^a-zA-Z0-9\s!?.,<>:_]", "", text)

    def clean(self, text):
        if not isinstance(text, str) or text.strip() == "":
            return ""

        text = self.mask_kenyan_names(text)
        text = self.mask_mentions(text)
        text = self.remove_urls(text)

        text = emoji.demojize(text, delimiters=(" ", " "))
        text = re.sub(r"(.)\1{2,}", r"\1\1", text)

        text = text.lower()
        text = self.remove_special_characters(text)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def transform(self, df, column="Text"):
        df = df.copy()
        df["clean_text"] = df[column].astype(str).apply(self.clean)
        return df