#!/usr/bin/env python3
import argparse
import json
import os
from typing import List, Dict, Tuple
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


class IntentDataset(Dataset):

    def __init__(self, texts: List[str], labels: List[int], tokenizer, max_length: int = 128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


def load_dataset(dataset_path: str) -> Tuple[List[str], List[str], Dict[str, int]]:
    print(f"Loading dataset from {dataset_path}")

    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    texts = []
    labels = []
    intent_list = []

    # Build intent list
    for intent_obj in data['intents']:
        intent = intent_obj['intent']
        if intent not in intent_list:
            intent_list.append(intent)

        # Add all examples for this intent
        for example in intent_obj['examples']:
            texts.append(example['text'])
            labels.append(intent)

    # Create label mapping
    label2id = {label: idx for idx, label in enumerate(intent_list)}
    id2label = {idx: label for label, idx in label2id.items()}

    # Convert labels to IDs
    label_ids = [label2id[label] for label in labels]

    print(f"Loaded {len(texts)} examples across {len(intent_list)} intents")
    print(f"Intents: {intent_list}")

    return texts, label_ids, label2id, id2label


def compute_metrics(pred):
    """Compute evaluation metrics."""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)

    accuracy = accuracy_score(labels, preds)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')

    return {
        'accuracy': accuracy,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }


def train_intent_classifier(
    dataset_path: str,
    output_dir: str,
    model_name: str = "roberta-base",
    num_epochs: int = 10,
    batch_size: int = 16,
    learning_rate: float = 2e-5,
    test_size: float = 0.2
):

    # Load dataset
    texts, labels, label2id, id2label = load_dataset(dataset_path)

    # Split into train and validation sets
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=test_size, random_state=42, stratify=labels
    )

    print(f"\nTrain set: {len(train_texts)} examples")
    print(f"Validation set: {len(val_texts)} examples")

    # Load tokenizer and model
    print(f"\nLoading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id
    )

    # Create datasets
    train_dataset = IntentDataset(train_texts, train_labels, tokenizer)
    val_dataset = IntentDataset(val_texts, val_labels, tokenizer)

    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        learning_rate=learning_rate,
        weight_decay=0.01,
        warmup_steps=100,
        logging_dir=f"{output_dir}/logs",
        logging_steps=10,
        eval_strategy="epoch",  # Changed from evaluation_strategy
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        report_to="none"  # Disable wandb/tensorboard
    )

    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )

    # Train
    print("\nStarting training...")
    trainer.train()

    # Evaluate
    print("\nEvaluating on validation set...")
    results = trainer.evaluate()
    print(f"Results: {results}")

    # Save model
    print(f"\nSaving model to {output_dir}")
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)

    # Save label mapping
    label_map_path = os.path.join(output_dir, "label_map.json")
    with open(label_map_path, 'w', encoding='utf-8') as f:
        json.dump(id2label, f, indent=2, ensure_ascii=False)

    print(f"Label mapping saved to {label_map_path}")
    print("\nTraining complete!")


def main():
    parser = argparse.ArgumentParser(description="Train Intent Classifier")
    parser.add_argument(
        "--dataset",
        type=str,
        default="datasets/assistant-bot-intent-dataset/dataset.json",
        help="Path to dataset JSON file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models/assistant-bot-intent-classifier",
        help="Output directory for trained model"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="roberta-base",
        help="Base model to fine-tune (roberta-base recommended)"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=10,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=16,
        help="Training batch size"
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=2e-5,
        help="Learning rate"
    )
    parser.add_argument(
        "--test_size",
        type=float,
        default=0.2,
        help="Validation set size (fraction)"
    )

    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.output, exist_ok=True)

    # Train
    train_intent_classifier(
        dataset_path=args.dataset,
        output_dir=args.output,
        model_name=args.model,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        test_size=args.test_size
    )


if __name__ == "__main__":
    main()
