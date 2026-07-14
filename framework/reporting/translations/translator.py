"""
Translation helper for the reporting system.
"""

from typing import Any

from framework.reporting.translations.zh import ZH


TRANSLATIONS = {
    "zh": ZH,
    "zh-cn": ZH,
    "cn": ZH,
}


def translate(
    key: str,
    language: str = "zh",
    default: str | None = None,
    **kwargs: Any,
) -> str:
    """
    Return translated text for a resource key.

    Parameters
    ----------
    key:
        Translation resource key.

    language:
        Language code. Currently supports:
        - zh
        - zh-cn
        - cn

    default:
        Fallback text when the key is unavailable.
        If omitted, the key itself is returned.

    **kwargs:
        Optional values used with str.format().

    Examples
    --------
    translate("CHAPTER_1")
    translate("AUTHOR")
    translate(
        "RESEARCH_PERIOD_TEMPLATE",
        start="2026-01-02",
        end="2026-06-10",
    )
    """
    normalized_language = str(language).strip().lower()

    resources = TRANSLATIONS.get(normalized_language)

    if resources is None:
        text = default if default is not None else key
    else:
        text = resources.get(
            key,
            default if default is not None else key,
        )

    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, ValueError) as exc:
            raise ValueError(
                f"Unable to format translation key '{key}': {exc}"
            ) from exc

    return str(text)


def tr(
    key: str,
    default: str | None = None,
    **kwargs: Any,
) -> str:
    """
    Chinese translation shortcut.

    Examples
    --------
    tr("CHAPTER_4")
    tr("FIG_4_1_TITLE")
    """
    return translate(
        key=key,
        language="zh",
        default=default,
        **kwargs,
    )


def has_translation(
    key: str,
    language: str = "zh",
) -> bool:
    """
    Return True when a translation key exists.
    """
    normalized_language = str(language).strip().lower()
    resources = TRANSLATIONS.get(normalized_language, {})

    return key in resources


def validate_translation_keys(
    keys: list[str],
    language: str = "zh",
) -> list[str]:
    """
    Return translation keys that are missing from the resource file.
    """
    return [
        key
        for key in keys
        if not has_translation(key, language=language)
    ]