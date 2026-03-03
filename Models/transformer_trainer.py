import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score, classification_report
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
from datasets import Dataset


class TransformerTrainer:
    def __init__(
        self,
        model_name="distilbert-base-multilingual-cased",
        test_size=0.2,
        random_state=42,
        epochs=3,
        batch_size=8
    ):
        self.model_name = model_name
        self.test_size = test_size
        self.random_state = random_state
        self.epochs = epochs
        self.batch_size = batch_size

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.label_encoder = LabelEncoder()

    def prepare_data(self, texts, labels):
        # Encode labels
        labels_encoded = self.label_encoder.fit_transform(labels)
        self.num_labels = len(self.label_encoder.classes_)

        # Split
        train_texts, test_texts, train_labels, test_labels = train_test_split(
            texts,
            labels_encoded,
            test_size=self.test_size,
            stratify=labels_encoded,
            random_state=self.random_state
        )

        # Tokenize
        train_encodings = self.tokenizer(
            list(train_texts),
            truncation=True,
            padding=True,
            max_length=128
        )

        test_encodings = self.tokenizer(
            list(test_texts),
            truncation=True,
            padding=True,
            max_length=128
        )

        train_dataset = Dataset.from_dict({
            **train_encodings,
            "labels": train_labels.tolist()
        })

        test_dataset = Dataset.from_dict({
            **test_encodings,
            "labels": test_labels.tolist()
        })

        return train_dataset, test_dataset

    def compute_metrics(self, eval_pred):
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)

        weighted_f1 = f1_score(labels, predictions, average="weighted")
        macro_f1 = f1_score(labels, predictions, average="macro")

        return {
            "weighted_f1": weighted_f1,
            "macro_f1": macro_f1
        }

    def train(self, texts, labels):
        train_dataset, test_dataset = self.prepare_data(texts, labels)

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=self.num_labels
        )

        training_args = TrainingArguments(
            output_dir="./results",
            evaluation_strategy="epoch",
            save_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=self.batch_size,
            per_device_eval_batch_size=self.batch_size,
            num_train_epochs=self.epochs,
            weight_decay=0.01,
            logging_dir="./logs",
            load_best_model_at_end=True
        )

        self.trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
            tokenizer=self.tokenizer,
            compute_metrics=self.compute_metrics
        )

        self.trainer.train()

        metrics = self.trainer.evaluate()
        return metrics