#!/usr/bin/env python3
import sys
from pathlib import Path

def download_model_from_hf(repo_id: str, local_dir: str):
    try:
        from huggingface_hub import snapshot_download

        print(f"Downloading {repo_id}...")
        print(f"   → {local_dir}")

        snapshot_download(
            repo_id=repo_id,
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            ignore_patterns=[".git*"]  # Skip checkpoints and git to save space
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


def check_and_download_models():

    # Get project root (parent of scripts folder)
    project_root = Path(__file__).parent.parent
    models_dir = project_root / "models"

    # Model configurations
    models = {
        "intent_classifier": {
            "path": models_dir / "assistant-bot-intent-classifier",
            "repo_id": "kms-engineer/assistant-bot-intent-classifier",
            "description": "Intent Classification Model"
        },
        "ner_model": {
            "path": models_dir / "assistant-bot-ner-model",
            "repo_id": "kms-engineer/assistant-bot-ner-model",
            "description": "NER Model"
        }
    }

    print("=" * 70)
    print("Assistant Bot - Model Checker")
    print("=" * 70)
    print()

    # Check each model
    models_to_download = []
    all_exist = True

    for model_name, config in models.items():
        model_path = config["path"]
        exists = model_path.exists() and (model_path / "model.safetensors").exists()

        status = "Found" if exists else "Missing"
        print(f"{status}: {config['description']}")
        print(f"         Path: {model_path}")

        if not exists:
            models_to_download.append((model_name, config))
            all_exist = False

        print()

    # If all models exist, we're done
    if all_exist:
        print("All models are ready!")
        print("=" * 70)
        return True

    # Download missing models
    print("=" * 70)
    print(f"Downloading {len(models_to_download)} missing model(s)...")
    print("=" * 70)
    print()

    success = True
    for model_name, config in models_to_download:
        model_path = config["path"]
        repo_id = config["repo_id"]

        # Create models directory if it doesn't exist
        model_path.parent.mkdir(parents=True, exist_ok=True)

        # Download model
        if not download_model_from_hf(repo_id, str(model_path)):
            success = False

    # Summary
    print("=" * 70)
    if success:
        print("All models downloaded successfully!")
        print("\n Models are ready to use!")
    else:
        print("Some models failed to download.")
        print("\n You can manually download them from:")
        for model_name, config in models_to_download:
            print(f"   - https://huggingface.co/{config['repo_id']}")
    print("=" * 70)

    return success


def main():
    try:
        success = check_and_download_models()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
