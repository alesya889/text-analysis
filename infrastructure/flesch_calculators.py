from domain.types import Languages_Used
from domain.types import TextStats, AnalysisResult
from domain.interfaces import SyllableCounter
from application.use_cases import compute_stats


def flesch_index(stats: TextStats, lang: Languages_Used) -> float:
    """Calculate Flesch's Index."""

    if lang == Languages_Used.ENGLISH:
        return 206.835 - 1.015 * stats.avg_sentence_length - 84.6 * stats.avg_word_syllables

    elif lang == Languages_Used.RUSSIAN:
        return 206.835 - 1.3 * stats.avg_sentence_length - 60.1 * stats.avg_word_syllables

    elif lang == Languages_Used.GERMAN:
        return 206.835 - 1.015 * stats.avg_sentence_length - 84.6 * stats.avg_word_syllables

    elif lang == Languages_Used.FRANCE:
        return 206.835 - 1.015 * stats.avg_sentence_length - 84.6 * stats.avg_word_syllables

