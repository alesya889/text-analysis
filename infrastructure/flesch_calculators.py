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


def flesch_kincaid(stats: TextStats, lang: Languages_Used) -> float:
    """Calculate Flesch's Kincaid Index"""

    if lang == Languages_Used.ENGLISH:
        return 0.39 * stats.avg_sentence_length + 11.8 * stats.avg_word_syllables - 15.59

    elif lang == Languages_Used.RUSSIAN:
        return 206.863 - (1.52 * stats.avg_sentence_length) - (65.14 * stats.avg_word_syllables)

    elif lang == Languages_Used.GERMAN:
        return 0.39 * stats.avg_sentence_length + 11.8 * stats.avg_word_syllables - 15.59

    elif lang == Languages_Used.FRANCE:
        return 0.39 * stats.avg_sentence_length + 11.8 * stats.avg_word_syllables - 15.59


