"""
Translation resources for the reporting system.
"""

from framework.reporting.translations.translator import (
    has_translation,
    tr,
    translate,
    validate_translation_keys,
)


__all__ = [
    "tr",
    "translate",
    "has_translation",
    "validate_translation_keys",
]