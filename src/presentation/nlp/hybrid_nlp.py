from typing import Dict, Tuple
from concurrent.futures import ThreadPoolExecutor
from .intent_classifier import IntentClassifier
from .span_extractor import SpanExtractor
from .ner_model import NERModel
from .entity_validator import EntityValidator
from .template_parser import TemplateParser
from .post_rules import PostProcessingRules
from src.config import NLPConfig, IntentConfig, EntityConfig


class HybridNLP:

    def __init__(
        self,
        intent_model_path: str = None,
        ner_model_path: str = None,
        use_pretrained: bool = True,
        default_region: str = "US",
        use_parallel: bool = True
    ):
        print("Initializing Hybrid NLP System")
        print("Architecture: Intent → NER → Validation → Regex (fallback) → Template Parser")
        if use_parallel:
            print("Parallel processing: ENABLED (Intent + NER)\n")
        else:
            print("Parallel processing: DISABLED\n")

        self.use_parallel = use_parallel
        # Thread pool for parallel execution (2 workers for Intent + NER)
        self.executor = ThreadPoolExecutor(max_workers=2) if use_parallel else None

        # Initialize components
        try:
            self.intent_classifier = IntentClassifier(
                model_path=intent_model_path,
                use_pretrained=use_pretrained
            )
            print("Intent Classifier loaded")
        except Exception as e:
            print(f"Intent Classifier failed: {e}")
            self.intent_classifier = None

        try:
            self.span_extractor = SpanExtractor(
                model_path=None,  # Regex-based, no model needed
                use_pretrained=use_pretrained
            )
            print("Span Extractor loaded")
        except Exception as e:
            print(f"Span Extractor failed: {e}")
            self.span_extractor = None

        try:
            self.ner_model = NERModel(
                model_path=ner_model_path,
                use_pretrained=use_pretrained
            )
            print("NER Model loaded")
        except Exception as e:
            print(f"NER Model failed: {e}")
            self.ner_model = None

        try:
            self.entity_validator = EntityValidator()
            print("Entity Validator loaded")
        except Exception as e:
            print(f"Entity Validator failed: {e}")
            self.entity_validator = None

        try:
            self.template_parser = TemplateParser(verbose=False)
            print("Template Parser loaded")
        except Exception as e:
            print(f"Template Parser failed: {e}")
            self.template_parser = None

        try:
            self.post_processor = PostProcessingRules(default_region=default_region)
            print("Post-Processing Rules loaded")
        except Exception as e:
            print(f"Post-Processing Rules failed: {e}")
            self.post_processor = None

        print("\nHybrid NLP System ready!\n")

    def __del__(self):
        if self.executor:
            self.executor.shutdown(wait=False)

    def shutdown(self):
        if self.executor:
            self.executor.shutdown(wait=True)
            self.executor = None

    def process(self, user_text: str, verbose: bool = False) -> Dict:
        if verbose:
            print(f"\nProcessing: '{user_text}'")
            print("=" * 60)

        # Step 1 & 2: Intent Classification + NER Entity Extraction (parallel if enabled)
        if self.use_parallel and self.executor:
            # Submit intent and NER tasks to thread pool
            intent_future = self.executor.submit(self._classify_intent, user_text, verbose)
            ner_future = self.executor.submit(self._extract_entities_ner, user_text, verbose)

            # Wait for both to complete
            intent, intent_confidence = intent_future.result()
            entities_ner, ner_confidences = ner_future.result()
        else:
            # Sequential execution (original behavior)
            intent, intent_confidence = self._classify_intent(user_text, verbose)
            entities_ner, ner_confidences = self._extract_entities_ner(user_text, verbose)

        # Step 3: Validation Check on NER results
        validation_result = self._validate_entities(entities_ner, intent, verbose)

        # Step 4: If NER is insufficient, try Regex as fallback
        entities = None
        source = "ner"

        if validation_result['needs_ner']:
            # NER didn't extract all required/optional fields - use Regex as fallback
            entities_regex, spans, entity_probs = self._extract_entities_regex(user_text, verbose)
            # Merge: prefer NER results, use regex to fill missing fields
            entities = self._merge_entities(
                entities_regex, entities_ner,
                entity_probs, ner_confidences,
                validation_result, verbose
            )
            source = "ner+regex"
        else:
            # NER extracted everything needed
            entities = entities_ner
            spans = []
            entity_probs = {}

        # Step 5: Final validation check - use template parser if still invalid
        final_validation = self._validate_entities(entities, intent, verbose=False)

        if final_validation['needs_ner'] and self._should_use_template_parser(intent, intent_confidence):
            if verbose:
                print("[Template Parser] Both regex and NER failed, using Template Parser")
            result = self._use_template_parser(user_text, intent, entities, verbose)
            source = "template"
        else:
            result = {
                "intent": intent,
                "confidence": intent_confidence,
                "entities": entities,
                "raw": {
                    "spans": spans,
                    "probs": entity_probs,
                    "source": source
                }
            }

        # Step 6: Post-Processing (normalization, validation, enrichment)
        result = self._post_process(result, user_text, verbose)

        if verbose:
            print("=" * 60)
            print(f"Final Result: {result['intent']} (confidence: {result['confidence']:.2f})")
            print(f"Entities: {result['entities']}")
            print(f"Source: {result['raw']['source']}")
            print(f"Valid: {result.get('validation', {}).get('valid', 'unknown')}")

        return result

    def _classify_intent(self, text: str, verbose: bool = False) -> Tuple[str, float]:
        if self.intent_classifier:
            intent, confidence = self.intent_classifier.predict(text)
            if verbose:
                print(f"[Intent] {intent} (confidence: {confidence:.2f})")
            return intent, confidence
        else:
            if verbose:
                print(f"[Intent] Classifier not available, using '{IntentConfig.DEFAULT_INTENT}'")
            return IntentConfig.DEFAULT_INTENT, IntentConfig.DEFAULT_INTENT_CONFIDENCE

    def _extract_entities_regex(self, text: str, verbose: bool = False) -> Tuple[Dict, list, Dict]:
        if self.span_extractor:
            entities, spans, probs = self.span_extractor.extract(text)
            if verbose:
                print(f"[Regex] Extracted: {entities}")
                if probs:
                    print(f"[Regex] Probabilities: {probs}")
            return entities, spans, probs
        else:
            if verbose:
                print("[Regex] Extractor not available")
            return {}, [], {}

    def _extract_entities_ner(self, text: str, verbose: bool = False) -> Tuple[Dict, Dict]:
        if self.ner_model:
            entities, confidences = self.ner_model.extract_entities(text, verbose=verbose)
            if verbose:
                print(f"[NER Model] Extracted: {entities}")
                print(f"[NER Model] Confidences: {confidences}")
            return entities, confidences
        else:
            if verbose:
                print("[NER Model] Not available")
            return {}, {}

    def _validate_entities(self, entities: Dict, intent: str, verbose: bool = False) -> Dict:
        if self.entity_validator:
            validation = self.entity_validator.validate(entities, intent)
            if verbose:
                print(f"[Validation] Result: {validation}")
            return validation
        else:
            # No validator, assume valid
            return {
                "valid": True,
                "missing_required": [],
                "optional_count": 0,
                "optional_needed": 0,
                "needs_ner": False,
                "reason": "No validator available"
            }

    def _merge_entities(
        self,
        entities_regex: Dict,
        entities_ner: Dict,
        regex_confidences: Dict,
        ner_confidences: Dict,
        validation_result: Dict,
        verbose: bool = False
    ) -> Dict:
        merged = {}

        # Get entity field preferences from config
        regex_preferred = EntityConfig.REGEX_PREFERRED_FIELDS
        ner_preferred = EntityConfig.NER_PREFERRED_FIELDS

        # Get all possible entity keys
        all_keys = set(entities_regex.keys()) | set(entities_ner.keys())

        for key in all_keys:
            regex_value = entities_regex.get(key)
            ner_value = entities_ner.get(key)

            # Get confidence scores (use defaults from config)
            regex_conf = regex_confidences.get(
                key,
                EntityConfig.DEFAULT_REGEX_CONFIDENCE if regex_value else EntityConfig.DEFAULT_REGEX_NO_MATCH_CONFIDENCE
            )
            ner_conf = ner_confidences.get(
                key,
                EntityConfig.DEFAULT_NER_CONFIDENCE if ner_value else EntityConfig.DEFAULT_NER_NO_MATCH_CONFIDENCE
            )

            # If only one source has the entity, use it
            if regex_value and not ner_value:
                merged[key] = regex_value
                if verbose:
                    print(f"[Merge] {key}: Using regex (only source) - '{regex_value}'")
                continue
            elif ner_value and not regex_value:
                merged[key] = ner_value
                if verbose:
                    print(f"[Merge] {key}: Using NER (only source) - '{ner_value}'")
                continue
            elif not regex_value and not ner_value:
                continue

            # Both sources have the entity - use confidence-based selection
            confidence_diff = abs(regex_conf - ner_conf)

            if confidence_diff > NLPConfig.CONFIDENCE_OVERRIDE_THRESHOLD:
                # Significant confidence difference - use higher confidence source
                if regex_conf > ner_conf:
                    merged[key] = regex_value
                    if verbose:
                        print(f"[Merge] {key}: Using regex (higher confidence {regex_conf:.2f} > {ner_conf:.2f}) - '{regex_value}'")
                else:
                    merged[key] = ner_value
                    if verbose:
                        print(f"[Merge] {key}: Using NER (higher confidence {ner_conf:.2f} > {regex_conf:.2f}) - '{ner_value}'")
            else:
                # Similar confidence - use preference-based selection
                if key in regex_preferred:
                    merged[key] = regex_value
                    if verbose:
                        print(f"[Merge] {key}: Using regex (preferred for structured data, conf={regex_conf:.2f}) - '{regex_value}'")
                elif key in ner_preferred:
                    merged[key] = ner_value
                    if verbose:
                        print(f"[Merge] {key}: Using NER (preferred for unstructured data, conf={ner_conf:.2f}) - '{ner_value}'")
                else:
                    # No preference - use higher confidence
                    if regex_conf >= ner_conf:
                        merged[key] = regex_value
                        if verbose:
                            print(f"[Merge] {key}: Using regex (conf={regex_conf:.2f} >= {ner_conf:.2f}) - '{regex_value}'")
                    else:
                        merged[key] = ner_value
                        if verbose:
                            print(f"[Merge] {key}: Using NER (conf={ner_conf:.2f} > {regex_conf:.2f}) - '{ner_value}'")

        if verbose:
            print(f"[Merge] Final merged: {merged}")

        return merged

    def _should_use_template_parser(self, intent: str, intent_confidence: float) -> bool:
        return intent_confidence < NLPConfig.INTENT_CONFIDENCE_THRESHOLD

    def _use_template_parser(
        self,
        text: str,
        intent_hint: str,
        entities_hint: Dict,
        verbose: bool = False
    ) -> Dict:
        if verbose:
            print("[Template Parser] Parsing with keyword matching and regex...")

        if self.template_parser:
            result = self.template_parser.generate_structured_output(
                text,
                intent_hint=intent_hint,
                entities_hint=entities_hint
            )
            result['raw']['source'] = 'template'

            # Handle conflict resolution: trust higher confidence
            if 'intent' in result and intent_hint:
                if result.get('confidence', 0) < EntityConfig.ENTITY_MERGE_THRESHOLD:
                    # If template parser has low confidence, keep original intent
                    result['intent'] = intent_hint
                    if verbose:
                        print(f"[Template Parser] Kept original intent '{intent_hint}' due to low parser confidence")

            return result
        else:
            # Template parser not available, use primary results
            if verbose:
                print("[Template Parser] Not available, using primary results")
            return {
                "intent": intent_hint,
                "confidence": EntityConfig.DEFAULT_ENTITY_CONFIDENCE,
                "entities": entities_hint,
                "raw": {"spans": [], "probs": {}, "source": "primary"}
            }

    def _post_process(self, result: Dict, original_text: str = None, verbose: bool = False) -> Dict:
        if verbose:
            print("[Post-Processing] Normalizing and validating...")

        if self.post_processor:
            # Process entities
            processed_entities = self.post_processor.process(
                result['entities'],
                result['intent'],
                original_text
            )
            result['entities'] = processed_entities

            # Validate entities for intent
            validation = self.post_processor.validate_entities_for_intent(
                processed_entities,
                result['intent']
            )

            # Add validation errors if any
            if '_validation_errors' in processed_entities:
                validation['errors'] = processed_entities['_validation_errors']
                # Remove from entities
                del processed_entities['_validation_errors']
            else:
                validation['errors'] = []

            result['validation'] = validation

            if verbose:
                if not validation['valid']:
                    print(f"[Post-Processing] Missing required entities: {validation['missing']}")
                if validation['errors']:
                    print(f"[Post-Processing] Validation errors: {validation['errors']}")
        else:
            result['validation'] = {
                'valid': True,
                'missing': [],
                'errors': []
            }

        return result

    def get_command_args(self, nlp_result: Dict) -> Tuple[str, list]:
        intent = nlp_result['intent']
        entities = nlp_result['entities']
        validation = nlp_result.get('validation', {})

        # Get intent to command mapping from config
        command = IntentConfig.INTENT_TO_COMMAND_MAP.get(intent, IntentConfig.DEFAULT_INTENT)

        # Check if should use pipeline
        # Pipeline is used when there are optional entities present
        # BUT skip pipeline for simple single-parameter optional intents
        skip_pipeline_intents = ['list_birthdays']
        if validation.get('has_optional', False) and intent not in skip_pipeline_intents:
            # Return special marker to indicate pipeline should be used
            return 'pipeline', nlp_result

        # Build args list based on intent (for non-pipeline commands)
        args = []

        if intent == 'add_contact':
            if 'name' in entities:
                args.append(entities['name'])
            if 'phone' in entities:
                args.append(entities['phone'])

        elif intent == 'edit_phone':
            if 'name' in entities:
                args.append(entities['name'])
            # Add old_phone and new_phone
            if 'old_phone' in entities:
                args.append(entities['old_phone'])
            if 'new_phone' in entities:
                args.append(entities['new_phone'])

        elif intent == 'edit_email':
            if 'name' in entities:
                args.append(entities['name'])
            if 'email' in entities:
                args.append(entities['email'])

        elif intent == 'edit_address':
            if 'name' in entities:
                args.append(entities['name'])
            if 'address' in entities:
                args.append(entities['address'])

        elif intent == 'delete_contact':
            if 'name' in entities:
                args.append(entities['name'])

        elif intent == 'search_contacts':
            if 'name' in entities:
                args.append(entities['name'])
            elif 'phone' in entities:
                args.append(entities['phone'])
            elif 'email' in entities:
                args.append(entities['email'])

        elif intent == 'add_birthday':
            if 'name' in entities:
                args.append(entities['name'])
            if 'birthday' in entities:
                args.append(entities['birthday'])

        elif intent == 'list_birthdays':
            # Use days from entities if present, otherwise default to 7
            days = entities.get('days', '7')
            args.append(str(days))

        elif intent == 'add_note':
            if 'note_text' in entities:
                args.append(entities['note_text'])

        elif intent == 'edit_note':
            if 'id' in entities:
                args.append(entities['id'])
            if 'note_text' in entities:
                args.append(entities['note_text'])

        elif intent in ['remove_note', 'delete_note']:
            if 'id' in entities:
                args.append(entities['id'])

        elif intent in ['add_note_tag', 'remove_note_tag']:
            if 'id' in entities:
                args.append(entities['id'])
            if 'tag' in entities:
                args.append(entities['tag'])

        elif intent == 'search_notes_text':
            if 'note_text' in entities:
                args.append(entities['note_text'])

        elif intent == 'search_notes_by_tag':
            if 'tag' in entities:
                args.append(entities['tag'])

        elif intent == 'add_email':
            if 'name' in entities:
                args.append(entities['name'])
            if 'email' in entities:
                args.append(entities['email'])

        elif intent == 'remove_email':
            if 'name' in entities:
                args.append(entities['name'])

        elif intent == 'add_address':
            if 'name' in entities:
                args.append(entities['name'])
            if 'address' in entities:
                args.append(entities['address'])

        elif intent == 'remove_address':
            if 'name' in entities:
                args.append(entities['name'])

        elif intent == 'show_phone':
            if 'name' in entities:
                args.append(entities['name'])

        elif intent == 'show_birthday':
            if 'name' in entities:
                args.append(entities['name'])

        return command, args
