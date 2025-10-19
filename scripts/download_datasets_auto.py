#!/usr/bin/env python3
import sys
from pathlib import Path


def download_dataset_from_hf(repo_id: str, local_dir: str):
    try:
        from huggingface_hub import snapshot_download

        print(f"Downloading {repo_id}...")
        print(f"   → {local_dir}")

        snapshot_download(
            repo_id=repo_id,
            repo_type="dataset",
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            ignore_patterns=[".git*"]
        )

        print(f"Downloaded {repo_id}\n")
        return True

    except ImportError:
        print("Error: huggingface_hub not installed!")
        print("Install it with: pip install huggingface_hub")
        return False
    except Exception as e:
        print(f"Error downloading {repo_id}: {e}")
        return False


def check_and_download_datasets():

    # Get project root (parent of scripts folder)
    project_root = Path(__file__).parent.parent
    datasets_dir = project_root / "datasets"

    # Dataset configurations
    datasets = {
        "intent_dataset": {
            "path": datasets_dir / "assistant-bot-intent-dataset",
            "repo_id": "kms-engineer/assistant-bot-intent-dataset",
            "description": "Intent Classification Dataset",
            "files": ["data.jsonl", "train.jsonl", "test.jsonl", "README.md"]
        },
        "ner_dataset": {
            "path": datasets_dir / "assistant-bot-ner-dataset",
            "repo_id": "kms-engineer/assistant-bot-ner-dataset",
            "description": "NER Dataset",
            "files": ["data.jsonl", "train.jsonl", "test.jsonl", "README.md"]
        }
    }

    print("=" * 70)
    print("Assistant Bot - Dataset Checker")
    print("=" * 70)
    print()

    # Check each dataset
    datasets_to_download = []
    all_exist = True

    for dataset_name, config in datasets.items():
        dataset_path = config["path"]
        # Check if directory exists and has required files
        exists = (
            dataset_path.exists()
            and any((dataset_path / file).exists() for file in config["files"])
        )

        status = "Found" if exists else "Missing"
        print(f"{status}: {config['description']}")
        print(f"         Path: {dataset_path}")

        if not exists:
            datasets_to_download.append((dataset_name, config))
            all_exist = False

        print()

    # If all datasets exist, we're done
    if all_exist:
        print("All datasets are ready!")
        print("=" * 70)
        return True

    # Download missing datasets
    print("=" * 70)
    print(f"Downloading {len(datasets_to_download)} missing dataset(s)...")
    print("=" * 70)
    print()

    success = True
    for dataset_name, config in datasets_to_download:
        dataset_path = config["path"]
        repo_id = config["repo_id"]

        # Create datasets directory if it doesn't exist
        dataset_path.parent.mkdir(parents=True, exist_ok=True)

        # Download dataset
        if not download_dataset_from_hf(repo_id, str(dataset_path)):
            success = False

    # Summary
    print("=" * 70)
    if success:
        print("All datasets downloaded successfully!")
        print("\nDatasets are ready to use!")
    else:
        print("Some datasets failed to download.")
        print("\nYou can manually download them from:")
        for dataset_name, config in datasets_to_download:
            print(f"   - https://huggingface.co/datasets/{config['repo_id']}")
    print("=" * 70)

    return success


def main():
    try:
        success = check_and_download_datasets()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
