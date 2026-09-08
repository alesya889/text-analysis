from domain.types import TextStats, AnalysisResult, Languages_Used, Polarity
from domain.interfaces import SyllableCounter, SentimentAnalyzer
import re

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