from domain.types import TextStats, AnalysisResult, Languages_Used, Polarity, Difficulty_Level
from domain.interfaces import SyllableCounter, SentimentAnalyzer
import re
import infrastructure.flesch_calculators

def split_sentences(text: str) -> list[str]:
    import re
    return re.split(r'[.!?]', text)

def split_words(text: str) -> list[str]:
    return re.findall(r'\b\w+\b', text)

def compute_stats(text: str, syllable_counter: SyllableCounter) -> TextStats:

    sentences = split_sentences(text)
    cnt_sentences = len(sentences)
    words = split_words(text)
    cnt_words = len(words)

    total_syllables = sum(syllable_counter(w) for w in words)
    avg_sentence_length =  cnt_words / cnt_sentences if cnt_sentences > 0 else 0
    avg_word_syllables = total_syllables / cnt_words if cnt_words > 0 else 0

    return TextStats(
        sentence_count=cnt_sentences,
        word_count=cnt_words,
        syllable_count=total_syllables,
        avg_sentence_length=avg_sentence_length,
        avg_word_syllables=avg_word_syllables
    )

def interpret_flesch(score: float, lang: Languages_Used) -> str:
    if lang == Languages_Used.ENGLISH:
        if 100 >= score >= 90:
            return Difficulty_Level.Very_Easy.value
        elif 90 > score >= 60:
            return Difficulty_Level.Easy.value
        elif 60 > score >= 30:
            return Difficulty_Level.Hard.value
        elif 30 > score >= 0:
            return Difficulty_Level.Very_Hard.value

    if lang == Languages_Used.RUSSIAN:
        if 100 >= score >= 80:
            return Difficulty_Level.Very_Easy.value
        elif 80 > score >= 60:
            return Difficulty_Level.Easy.value
        elif 60 > score >= 30:
            return Difficulty_Level.Hard.value
        elif 30 > score >= 0:
            return Difficulty_Level.Very_Hard.value

    if lang == Languages_Used.GERMAN:
        if 100 >= score >= 80:
            return Difficulty_Level.Very_Easy.value
        elif 80 > score >= 60:
            return Difficulty_Level.Easy.value
        elif 60 > score >= 40:
            return Difficulty_Level.Hard.value
        elif 40 > score >= 0:
            return Difficulty_Level.Very_Hard.value

    if lang == Languages_Used.FRANCE:
        if 100 >= score >= 80:
            return Difficulty_Level.Very_Easy.value
        elif 80 > score >= 60:
            return Difficulty_Level.Easy.value
        elif 60 > score >= 40:
            return Difficulty_Level.Hard.value
        elif 40 > score >= 0:
            return Difficulty_Level.Very_Hard.value





