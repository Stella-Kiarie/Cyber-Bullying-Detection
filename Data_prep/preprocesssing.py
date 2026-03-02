import re
import spacy
import emoji
# Ensure the import path matches your folder structure
from Data_prep.kenyannames import KENYAN_NAMES 

class TextPreprocessor:
    def __init__(self):
        # 1. Load spaCy: NER needs tok2vec and ner
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "lemmatizer"])
        except OSError:
            raise OSError("Run 'python -m spacy download en_core_web_sm' in your terminal")

        # 2. Prepare Kenyan Names Regex
        # Sort by length descending so "toxic lyrikali" matches before "toxic"
        clean_names = sorted([re.escape(str(n)) for n in KENYAN_NAMES if n], key=len, reverse=True)
        
        self.name_pattern = re.compile(
            r"\b(" + "|".join(clean_names) + r")\b",
            flags=re.IGNORECASE
        )

    def mask_spacy_names(self, text):
        doc = self.nlp(text)
        # Using a list comprehension is faster for large dataframes
        return " ".join(["<NAME>" if t.ent_type_ == "PERSON" else t.text for t in doc])

    def mask_kenyan_names(self, text):
        return self.name_pattern.sub("<NAME>", text)

    def mask_mentions(self, text):
        return re.sub(r"@\w+", "<NAME>", text)

    def remove_urls(self, text):
        return re.sub(r"https?://\S+|www\.\S+", "", text)

    def remove_special_characters(self, text):
        # ADDED < and > so your <NAME> tag isn't destroyed!
        return re.sub(r"[^a-zA-Z0-9\s!?.,<>]", "", text)

    def clean(self, text):
        if not isinstance(text, str) or text.strip() == "":
            return ""

        # Pipeline execution
        text = self.mask_spacy_names(text)
        text = self.mask_kenyan_names(text)
        text = self.mask_mentions(text)
        text = self.remove_urls(text)
        text = emoji.demojize(text)
        
        # Normalize repetition (waaaah -> waah)
        text = re.sub(r"(.)\1{2,}", r"\1\1", text)
        
        text = text.lower()
        text = self.remove_special_characters(text)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def transform(self, df, column="Text"):
        df = df.copy()
        df["clean_text"] = df[column].astype(str).apply(self.clean)
        return df