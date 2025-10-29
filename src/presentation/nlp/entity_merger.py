from typing import Dict
from src.config import NLPConfig, EntityConfig


class EntityMerger:
    @staticmethod
    def merge(
        regex_ent: Dict,
        ner_ent: Dict,
        regex_conf: Dict,
        ner_conf: Dict
    ) -> Dict:
        merged = {}
        all_keys = set(regex_ent.keys()) | set(ner_ent.keys())

        for key in all_keys:
            r_val = regex_ent.get(key)
            n_val = ner_ent.get(key)

            if not r_val and not n_val:
                continue
            elif r_val and not n_val:
                merged[key] = r_val
            elif n_val and not r_val:
                merged[key] = n_val
            else:
                r_conf = regex_conf.get(key, EntityConfig.DEFAULT_REGEX_CONFIDENCE if r_val else 0.0)
                n_conf = ner_conf.get(key, EntityConfig.DEFAULT_NER_CONFIDENCE if n_val else 0.0)

                conf_diff = abs(r_conf - n_conf)

                if conf_diff > NLPConfig.CONFIDENCE_OVERRIDE_THRESHOLD:
                    merged[key] = r_val if r_conf > n_conf else n_val
                elif key in EntityConfig.REGEX_PREFERRED_FIELDS:
                    merged[key] = r_val
                elif key in EntityConfig.NER_PREFERRED_FIELDS:
                    merged[key] = n_val
                else:
                    merged[key] = r_val if r_conf >= n_conf else n_val

        return merged
