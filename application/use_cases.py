from domain.types import TextStats, AnalysisResult, Languages_Used, Polarity, Difficulty_Level
from domain.interfaces import SyllableCounter, SentimentAnalyzer, LanguageDetector
import re
from infrastructure.flesch_calculators import fleschIndex, fleschKincaid
from infrastructure.syllable_counters import getSyllableCounter


def splitSentences(text: str) -> list[str]:
    list_of_possibilities = re.split(r'[.!?]', text)
    true_list = []

    for i in list_of_possibilities:
        if i == '' or i.isspace():
            continue
        else:
            true_list.append(i)

    return true_list

def splitWords(text: str) -> list[str]:
    text = text.replace("'", '')
    return re.findall(r'\b\w+\b', text)

def computeStats(text: str, syllable_counter: SyllableCounter) -> TextStats:

    sentences = splitSentences(text)
    cnt_sentences = len(sentences)
    words = splitWords(text)
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

def interpretFlesch(score: float, lang: Languages_Used) -> str:
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


def analyzeTextService(text: str,
                lang_detector: LanguageDetector,
                syllable_counter: SyllableCounter,
                sentiment_analyzer: SentimentAnalyzer) -> AnalysisResult:
    lang = lang_detector(text)
    stats = computeStats(text, syllable_counter)
    flesch = fleschIndex(stats, lang)
    kincaid = fleschKincaid(stats, lang)
    polarity, subj = sentiment_analyzer(text)
    # ... diversity, rare density
    return AnalysisResult(...)

def analyzeBatchService(texts: list[str], **deps) -> list[AnalysisResult]:
    return [analyzeText(t, **deps) for t in texts]





