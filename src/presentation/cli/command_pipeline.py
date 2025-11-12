from typing import Dict, List, Any

from src.config import IntentConfig
from ...application.services.contact_service import ContactService
from ...application.services.note_service import NoteService


class CommandPipeline:
    # Get pipeline definitions from config
    PIPELINE_DEFINITIONS = IntentConfig.PIPELINE_DEFINITIONS

    def __init__(self, contact_service: ContactService, note_service: NoteService):
        self.contact_service = contact_service
        self.note_service = note_service

    def should_use_pipeline(self, intent: str, entities: Dict) -> bool:
        if intent not in self.PIPELINE_DEFINITIONS:
            return False

        pipeline_def = self.PIPELINE_DEFINITIONS[intent]

        # Check if any pipeline step has entities available
        for step in pipeline_def["pipeline"]:
            step_entities = step["entities"]
            if any(entity in entities for entity in step_entities):
                return True

        return False

    def build_pipeline(
        self, intent: str, entities: Dict
    ) -> list[tuple[Any, list[str], str] | tuple[Any, list[str], str, dict[str, Any]]]:
        if intent not in self.PIPELINE_DEFINITIONS:
            return []

        pipeline_def = self.PIPELINE_DEFINITIONS[intent]
        commands : list[tuple[Any, list[str], str] | tuple[Any, list[str], str, dict[str, Any]]] = []

        # Add primary command
        primary_command = pipeline_def["primary_command"]
        primary_args = self._build_args_for_intent(
            entities, pipeline_def["primary_required"]
        )
        commands.append((primary_command, primary_args, "primary"))

        # Add pipeline steps
        for step in pipeline_def["pipeline"]:
            step_entities = step["entities"]
            min_entities = step.get("min_entities", 1)

            # Check if we have enough entities for this step
            available_entities = [
                e for e in step_entities if e in entities and entities[e]
            ]
            if len(available_entities) >= min_entities:
                step_command = step["command"]
                step_args = self._build_args_for_pipeline_step(
                    step_command, entities, step_entities, primary_args
                )
                condition = step.get("condition", None)
                note_id_from_primary = step.get("note_id_from_primary", False)

                commands.append(
                    (
                        step_command,
                        step_args,
                        "pipeline",
                        {
                            "condition": condition,
                            "note_id_from_primary": note_id_from_primary,
                        },
                    )
                )

        return commands

    @staticmethod
    def _build_args_for_intent(
        entities: Dict, required_entities: List[str]
    ) -> List[str]:
        args = []

        # For primary commands, use required entities in order
        for entity in required_entities:
            if entity in entities and entities[entity]:
                args.append(entities[entity])

        return args

    @staticmethod
    def _build_args_for_pipeline_step(
        command: str, entities: Dict, step_entities: List[str], primary_args: List[str]
    ) -> List[str]:
        args = []

        # Most pipeline commands need the contact name first
        if command in [
            "add-email",
            "add-address",
            "add-birthday",
            "edit-email",
            "edit-address",
        ]:
            # Get name from primary args (first arg is usually name)
            if primary_args:
                args.append(primary_args[0])

        # Add the step-specific entities
        for entity in step_entities:
            if entity in entities and entities[entity]:
                args.append(entities[entity])

        return args

    def get_pipeline_summary(self, intent: str, entities: Dict) -> str | None:
        pipeline = self.build_pipeline(intent, entities)

        if len(pipeline) <= 1:
            return None

        steps = []
        for i, item in enumerate(pipeline):
            if len(item) >= 3:
                command, args, step_type = item[:3]
                if step_type == "primary":
                    steps.append(f"1. {command} {' '.join(args)}")
                else:
                    steps.append(f"{i + 1}. {command} {' '.join(args)}")

        return "Pipeline:\n" + "\n".join(steps)

    @staticmethod
    def extract_note_id_from_result(result: str) -> str | None:
        # Example: "Note added with ID: 45f9ae2b-93b6-4e5d-bf62-dbe8af1e0f11"
        # Result may contain ANSI color codes, so we need to strip them first
        import re

        # Remove ANSI color codes
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        clean_result = ansi_escape.sub("", result)

        # Match UUID format (8-4-4-4-12 hex characters) or simple numeric ID
        match = re.search(
            r"ID:\s*([a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12}|\d+)",
            clean_result,
        )
        if match:
            return match.group(1)
        return None
