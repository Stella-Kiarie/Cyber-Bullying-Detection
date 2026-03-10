import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, f1_score
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from datasets import Dataset


class SentimentClassifier:

    def __init__(
        self,
        model_name="distilbert-base-multilingual-cased",
        epochs=1,
        batch_size=4,
        max_length=64
    ):
        self.model_name = model_name
        self.epochs = epochs
        self.batch_size = batch_size
        self.max_length = max_length

        self.label_encoder = LabelEncoder()
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    # ---------------------------------------
    # Prepare Dataset
    # ---------------------------------------
    def _prepare_dataset(self, texts, labels):

        encoded_labels = self.label_encoder.fit_transform(labels)

        train_texts, test_texts, train_labels, test_labels = train_test_split(
            texts,
            encoded_labels,
            test_size=0.2,
            stratify=encoded_labels,
            random_state=42
        )

        train_dataset = Dataset.from_dict({
            "text": train_texts.tolist(),
            "label": train_labels.tolist()
        })

        test_dataset = Dataset.from_dict({
            "text": test_texts.tolist(),
            "label": test_labels.tolist()
        })

        def tokenize(batch):
            return self.tokenizer(
                batch["text"],
                padding="max_length",
                truncation=True,
                max_length=self.max_length
            )

        train_dataset = train_dataset.map(tokenize, batched=True)
        test_dataset = test_dataset.map(tokenize, batched=True)

        train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
        test_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

        return train_dataset, test_dataset

    # ---------------------------------------
    # Train Model
    # ---------------------------------------
    def train(self, texts, labels):

        train_dataset, test_dataset = self._prepare_dataset(texts, labels)

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=len(np.unique(labels))
        )

        training_args = TrainingArguments(
            output_dir="./sentiment_results",
            num_train_epochs=self.epochs,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            eval_strategy="epoch",   
            save_strategy="no",
            logging_steps=100,
            fp16=False,
            dataloader_num_workers=0
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset
        )

        trainer.train()

        predictions = trainer.predict(test_dataset)
        preds = np.argmax(predictions.predictions, axis=1)

        print("\nClassification Report:\n")
        print(classification_report(test_dataset["label"], preds))

        print("Weighted F1:",
              f1_score(test_dataset["label"], preds, average="weighted"))

        print("Macro F1:",
              f1_score(test_dataset["label"], preds, average="macro"))

        return self