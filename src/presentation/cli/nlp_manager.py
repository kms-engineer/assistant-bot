import subprocess
import sys
from pathlib import Path
from typing import Optional


class NLPManager:

    def __init__(self, project_root: Optional[str] = None):
        if project_root is None:
            # Auto-detect project root (4 levels up from this file)
            current_file = Path(__file__).resolve()
            self.project_root = current_file.parent.parent.parent.parent
        else:
            self.project_root = Path(project_root)

        self.models_dir = self.project_root / "models"
        self.intent_model_path = self.models_dir / "assistant-bot-intent-classifier"
        self.ner_model_path = self.models_dir / "assistant-bot-ner-model"
        self.nlp_processor = None

    def check_models_exist(self) -> tuple[bool, bool]:
        intent_exists = (
            self.intent_model_path.exists()
            and (self.intent_model_path / "model.safetensors").exists()
        )
        ner_exists = (
            self.ner_model_path.exists()
            and (self.ner_model_path / "model.safetensors").exists()
        )
        return intent_exists, ner_exists

    def download_models(self) -> bool:
        print("\nDownloading models from Hugging Face...")
        download_script = self.project_root / "scripts" / "download_models_auto.py"

        try:
            if not download_script.exists():
                print(f"Download script not found at {download_script}")
                return False

            subprocess.run(
                [sys.executable, str(download_script)],
                check=True,
                capture_output=False
            )
            print("Models downloaded successfully!\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to download models: {e}")
            print(f"Please run manually: python {download_script}\n")
            return False
        except Exception as e:
            print(f"Unexpected error during download: {e}\n")
            return False

    def initialize_nlp_processor(
        self,
        use_parallel: bool = True
    ) -> bool:
        print("\nInitializing NLP mode...")

        # Check if models exist
        intent_exists, ner_exists = self.check_models_exist()

        # Download if missing
        models_missing = not intent_exists or not ner_exists
        if models_missing:
            if not intent_exists:
                print(f"Intent classifier not found at {self.intent_model_path}")
            if not ner_exists:
                print(f"NER model not found at {self.ner_model_path}")

            if not self.download_models():
                print("ERROR: Models are required but download failed.")
                return False

        # Initialize HybridNLP with model paths
        try:
            from ..nlp.hybrid_nlp import HybridNLP

            self.nlp_processor = HybridNLP(
                intent_model_path=str(self.intent_model_path),
                ner_model_path=str(self.ner_model_path),
                use_parallel=use_parallel
            )
            print("NLP mode ready!\n")
            return True

        except Exception as e:
            print(f"Failed to initialize NLP mode: {e}")
            print("Falling back to regex-based matching only.\n")
            self.nlp_processor = None
            return False

    def process_input(self, user_input: str) -> Optional[dict]:
        if self.nlp_processor is None:
            return None

        try:
            return self.nlp_processor.process(user_input)
        except Exception as e:
            print(f"NLP processing error: {e}")
            return None

    def get_command_args(self, nlp_result: dict) -> tuple[str, list] | tuple[str, dict]:
        if self.nlp_processor is None:
            return "help", []

        return self.nlp_processor.get_command_args(nlp_result)

    def is_ready(self) -> bool:
        return self.nlp_processor is not None

    def shutdown(self):
        if self.nlp_processor and hasattr(self.nlp_processor, 'shutdown'):
            self.nlp_processor.shutdown()
