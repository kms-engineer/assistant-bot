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
    AutoModelForTokenClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
    DataCollatorForTokenClassification
)
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report


# Entity labels (IOB2 format)
ENTITY_LABELS = [
    "O",              # Outside (not an entity)
    "B-NAME",         # Beginning of name
    "I-NAME",         # Inside name (continuation)
    "B-PHONE",        # Beginning of phone
    "I-PHONE",        # Inside phone
    "B-OLD_PHONE",    # Beginning of old phone (edit_phone)
    "I-OLD_PHONE",    # Inside old phone
    "B-NEW_PHONE",    # Beginning of new phone (edit_phone)
    "I-NEW_PHONE",    # Inside new phone
    "B-EMAIL",        # Beginning of email
    "I-EMAIL",        # Inside email
    "B-ADDRESS",      # Beginning of address
    "I-ADDRESS",      # Inside address
    "B-BIRTHDAY",     # Beginning of birthday
    "I-BIRTHDAY",     # Inside birthday
    "B-TAG",          # Beginning of tag
    "I-TAG",          # Inside tag
    "B-NOTE_TEXT",    # Beginning of note text
    "I-NOTE_TEXT",    # Inside note text
    "B-ID",           # Beginning of ID
    "I-ID",           # Inside ID
    "B-DAYS",         # Beginning of days/period
    "I-DAYS",         # Inside days/period
]

# Label mappings
LABEL2ID = {label: idx for idx, label in enumerate(ENTITY_LABELS)}
ID2LABEL = {idx: label for label, idx in LABEL2ID.items()}


class NERDataset(Dataset):

    def __init__(
        self,
        texts: List[str],
        tokens_list: List[List[str]],
        tags_list: List[List[str]],
        tokenizer,
        max_length: int = 128
    ):
        self.texts = texts
        self.tokens_list = tokens_list
        self.tags_list = tags_list
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        tokens = self.tokens_list[idx]
        tags = self.tags_list[idx]

        # Tokenize with word-level alignment
        encoding = self.tokenizer(
            tokens,
            is_split_into_words=True,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )

        # Align labels with tokenized inputs
        labels = []
        word_ids = encoding.word_ids(batch_index=0)

        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                # Special tokens (CLS, SEP, PAD)
                labels.append(-100)  # PyTorch ignore_index
            elif word_idx != previous_word_idx:
                # First subword of a word
                label = tags[word_idx]
                labels.append(LABEL2ID[label])
            else:
                # Continuation subword - use same label or convert B- to I-
                label = tags[word_idx]
                if label.startswith('B-'):
                    # Convert B- to I- for subword tokens
                    label = 'I-' + label[2:]
                labels.append(LABEL2ID.get(label, LABEL2ID['O']))

            previous_word_idx = word_idx

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(labels, dtype=torch.long)
        }


def load_ner_dataset(dataset_path: str) -> Tuple[List[str], List[List[str]], List[List[str]]]:
    print(f"Loading NER dataset from {dataset_path}")

    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    texts = []
    tokens_list = []
    tags_list = []

    for example in data.get('examples', []):
        texts.append(example['text'])
        tokens_list.append(example['tokens'])
        tags_list.append(example.get('ner_tags', example.get('tags', [])))

    print(f"Loaded {len(texts)} examples")

    # Print label distribution
    tag_counts = {}
    for tags in tags_list:
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    print("\nLabel distribution:")
    for tag, count in sorted(tag_counts.items()):
        print(f"  {tag}: {count}")

    return texts, tokens_list, tags_list


def compute_metrics(pred):
    predictions = pred.predictions
    labels = pred.label_ids

    # Get predictions (argmax)
    predictions = np.argmax(predictions, axis=2)

    # Flatten and filter out ignored labels (-100)
    true_labels = []
    pred_labels = []

    for pred_seq, label_seq in zip(predictions, labels):
        for pred_label, true_label in zip(pred_seq, label_seq):
            if true_label != -100:  # Ignore padding and special tokens
                true_labels.append(ID2LABEL[true_label])
                pred_labels.append(ID2LABEL[pred_label])

    # Calculate metrics
    accuracy = accuracy_score(true_labels, pred_labels)
    precision, recall, f1, _ = precision_recall_fscore_support(
        true_labels,
        pred_labels,
        average='weighted',
        zero_division=0
    )

    # Entity-level metrics (exclude 'O')
    entity_labels = [label for label in true_labels if label != 'O']
    entity_preds = [pred for pred, true in zip(pred_labels, true_labels) if true != 'O']

    entity_accuracy = accuracy_score(entity_labels, entity_preds) if entity_labels else 0.0

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'entity_accuracy': entity_accuracy
    }


def train_ner_model(
    dataset_path: str,
    output_dir: str,
    model_name: str = "roberta-base",
    num_epochs: int = 10,
    batch_size: int = 16,
    learning_rate: float = 3e-5,
    test_size: float = 0.2
):

    # Load dataset
    texts, tokens_list, tags_list = load_ner_dataset(dataset_path)

    # Split into train and validation sets
    train_texts, val_texts, train_tokens, val_tokens, train_tags, val_tags = train_test_split(
        texts, tokens_list, tags_list,
        test_size=test_size,
        random_state=42
    )

    print(f"\nTrain set: {len(train_texts)} examples")
    print(f"Validation set: {len(val_texts)} examples")

    # Load tokenizer and model
    print(f"\nLoading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name, add_prefix_space=True)
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        num_labels=len(ENTITY_LABELS),
        id2label=ID2LABEL,
        label2id=LABEL2ID
    )

    # Create datasets
    train_dataset = NERDataset(train_texts, train_tokens, train_tags, tokenizer)
    val_dataset = NERDataset(val_texts, val_tokens, val_tags, tokenizer)

    # Data collator
    data_collator = DataCollatorForTokenClassification(tokenizer)

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
        eval_strategy="epoch",
        save_strategy="epoch",
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        report_to="none",  # Disable wandb/tensorboard
        fp16=torch.cuda.is_available(),  # Use mixed precision if GPU available
    )

    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        data_collator=data_collator,
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
        json.dump(ID2LABEL, f, indent=2, ensure_ascii=False)

    print(f"Label mapping saved to {label_map_path}")
    print("\nTraining complete!")

    return results


def main():
    parser = argparse.ArgumentParser(description="Train NER Model (RoBERTa)")
    parser.add_argument(
        "--dataset",
        type=str,
        default="datasets/assistant-bot-ner-dataset/dataset.json",
        help="Path to NER dataset JSON file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="models/assistant-bot-ner-model",
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
        default=3e-5,
        help="Learning rate (3e-5 recommended for NER)"
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
    train_ner_model(
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
