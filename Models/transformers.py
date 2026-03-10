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


class TransformerLanguageClassifier:

    def __init__(
        self,
        model_name="distilbert-base-multilingual-cased",
        epochs=2,
        batch_size=8,
        max_length=128
    ):
        self.model_name = model_name
        self.epochs = epochs
        self.batch_size = batch_size
        self.max_length = max_length

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.label_encoder = LabelEncoder()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def prepare_data(self, texts, labels):

        labels_encoded = self.label_encoder.fit_transform(labels)

        X_train, X_test, y_train, y_test = train_test_split(
            texts,
            labels_encoded,
            test_size=0.2,
            stratify=labels_encoded,
            random_state=42
        )

        train_dataset = Dataset.from_dict({
            "text": list(X_train),
            "label": list(y_train)
        })

        test_dataset = Dataset.from_dict({
            "text": list(X_test),
            "label": list(y_test)
        })

        def tokenize(batch):
            return self.tokenizer(
                batch["text"],
                truncation=True,
                padding="max_length",
                max_length=self.max_length
            )

        train_dataset = train_dataset.map(tokenize, batched=True)
        test_dataset = test_dataset.map(tokenize, batched=True)

        train_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])
        test_dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])

        return train_dataset, test_dataset

    def train(self, texts, labels):

        train_dataset, test_dataset = self.prepare_data(texts, labels)

        num_labels = len(set(labels))

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=num_labels
        ).to(self.device)

        training_args = TrainingArguments(
        output_dir="./language_results",
        num_train_epochs=self.epochs,
        per_device_train_batch_size=self.batch_size,
        per_device_eval_batch_size=self.batch_size,
        evaluation_strategy="epoch",
        save_strategy="no",
        logging_strategy="steps",
        logging_steps=100,
        load_best_model_at_end=False,
        fp16=False,
        dataloader_num_workers=0,   # VERY IMPORTANT on Windows
        disable_tqdm=False
        )

        def compute_metrics(eval_pred):
            logits, labels = eval_pred
            predictions = np.argmax(logits, axis=1)
            return {
                "weighted_f1": f1_score(labels, predictions, average="weighted"),
                "macro_f1": f1_score(labels, predictions, average="macro")
            }

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=test_dataset,
            compute_metrics=compute_metrics
        )

        trainer.train()

        predictions = trainer.predict(test_dataset)
        y_pred = np.argmax(predictions.predictions, axis=1)
        y_true = predictions.label_ids

        print("\nClassification Report:\n")
        print(classification_report(
            y_true,
            y_pred,
            target_names=self.label_encoder.classes_
        ))

        print("Weighted F1:",
              f1_score(y_true, y_pred, average="weighted"))

        print("Macro F1:",
              f1_score(y_true, y_pred, average="macro"))

        return self

    def predict(self, text):

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=self.max_length
        ).to(self.device)

        outputs = self.model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()

        return self.label_encoder.inverse_transform([prediction])[0]