import re
from domain.types import TextStats, AnalysisResult, Languages_Used, Polarity, Difficulty_Level
from domain.interfaces import SyllableCounter, SentimentAnalyzer, LanguageDetector
from infrastructure.flesch_calculators import fleschIndex, fleschKincaid
from infrastructure.language_detector import detectLanguage
from infrastructure.syllable_counters import getSyllableCounter
from infrastructure.dictionaries import rareDictRu, rareDictEn, rareDictFr, rareDictDe


def validateText(text: str) -> None:
    # Проверяет валидность текста, основываясь на длине, допустимых символах

    allowedPattern = re.compile(
        r'^['
        r'А-Яа-яЁё'
        r'A-Za-z'
        r'ÄÖÜäöüß'
        r'ÀÂÆÇÉÈÊËÎÏÔŒÙÛÜŸàâæçéèêëîïôœùûüÿ'
        r'0-9'
        r'\s'
        r'.,!?;:—–\-\'"«»…()\[\]{}'
        r']+$'
    )

    if not text or not text.strip():
        raise ValueError('The text cannot be empty')

    if len(text) > 100_000:
        raise ValueError('Text is too long')

    if not re.search(r'[A-Za-zА-Яа-яЁёÄÖÜäöüßÀÂÆÇÉÈÊËÎÏÔŒÙÛÜŸàâæçéèêëîïôœùûüÿ]', text):
        raise ValueError('Text should contain only letters, numbers, punctuation')

    if not allowedPattern.match(text):
        for ch in text:
            if not allowedPattern.match(ch):
                raise ValueError(f'Not allowed symbol {ch!r}')
        raise ValueError("Text doesn't have allowed symbols")

def splitSentences(text: str) -> list[str]:
    # Разделяет строку на список строк-предложений

    listOfPossibilities = re.split(r'[.!?]', text)
    trueList = []

    for i in listOfPossibilities:
        if i == '' or i.isspace():
            continue
        else:
            trueList.append(i)

    return trueList

def splitWords(text: str) -> list[str]:
    # Разделяет строку на отдельные слова, собирая их в список

    text = text.replace("'", '')
    return re.findall(r'\b\w+\b', text)

def computeStats(text: str, syllableCounter: SyllableCounter) -> TextStats:
    # Собирает все технические параметры о тексте, используя отдельные функции


    sentences = splitSentences(text)
    cntSentences = len(sentences)
    words = splitWords(text)
    cntWords = len(words)

    totalSyllables = sum(syllableCounter(w) for w in words)
    avgSentenceLength =  cntWords / cntSentences if cntSentences > 0 else 0
    avgWordSyllables = totalSyllables / cntWords if cntWords > 0 else 0

    return TextStats(
        sentence_count=cntSentences,
        word_count=cntWords,
        syllable_count=totalSyllables,
        avg_sentence_length=avgSentenceLength,
        avg_word_syllables=avgWordSyllables
    )

def interpretFlesch(score: float, lang: Languages_Used) -> str:
    # Интерпретирует результаты индекса Флеша в зависимости от языка, адаптирует невалидные баллы

    score = max(0, min(100, score))
    if lang == Languages_Used.ENGLISH:
        if 100 >= score >= 90:
            return Difficulty_Level.Very_Easy.value
        elif 90 > score >= 60:
            return Difficulty_Level.Easy.value
        elif 60 > score >= 30:
            return Difficulty_Level.Hard.value
        elif 30 > score >= 0:
            return Difficulty_Level.Very_Hard.value

    elif lang == Languages_Used.RUSSIAN:
        if 100 >= score >= 80:
            return Difficulty_Level.Very_Easy.value
        elif 80 > score >= 60:
            return Difficulty_Level.Easy.value
        elif 60 > score >= 30:
            return Difficulty_Level.Hard.value
        elif 30 > score >= 0:
            return Difficulty_Level.Very_Hard.value

    elif lang == Languages_Used.GERMAN:
        if 100 >= score >= 80:
            return Difficulty_Level.Very_Easy.value
        elif 80 > score >= 60:
            return Difficulty_Level.Easy.value
        elif 60 > score >= 40:
            return Difficulty_Level.Hard.value
        elif 40 > score >= 0:
            return Difficulty_Level.Very_Hard.value

    elif lang == Languages_Used.FRANCE:
        if 100 >= score >= 80:
            return Difficulty_Level.Very_Easy.value
        elif 80 > score >= 60:
            return Difficulty_Level.Easy.value
        elif 60 > score >= 40:
            return Difficulty_Level.Hard.value
        elif 40 > score >= 0:
            return Difficulty_Level.Very_Hard.value

    else:
        return 'Unknown'

def lexicalDiversity(text: str) -> float:
    # Вычисляет долю уникальных слов в тексте

    words = splitWords(text.lower())
    uniqueWords = set(words)

    if len(words) == 0:
        return 0
    return len(uniqueWords) / len(words)

def rareWordDensity(text: str, freqDict: dict) -> float:
    # Вычисляет долю редких слов в тексте, ссылаясь на собранные словари

    words = splitWords(text.lower())
    rareWord = 0

    if not words:
        return 0

    for word in words:
        if word in freqDict:
            rareWord += 1

    return rareWord / len(words)

def analyzeTextService(text: str,
                       langDetector: LanguageDetector,
                       syllableCounter: SyllableCounter,
                       sentimentAnalyzer: SentimentAnalyzer) -> AnalysisResult:
    # Итоговая функция полностью анализирующая текст с помощью переданных ей параметров

    validateText(text)
    lang = langDetector(text)
    stats = computeStats(text, syllableCounter)
    flesch = fleschIndex(stats, lang)
    kincaid = fleschKincaid(stats, lang)
    interpretationFl = interpretFlesch(flesch, lang)
    polarity, subj = sentimentAnalyzer(text)
    diversity = lexicalDiversity(text)

    if lang == Languages_Used.ENGLISH:
        freqDict = rareDictEn
    elif lang == Languages_Used.RUSSIAN:
        freqDict = rareDictRu
    elif lang == Languages_Used.GERMAN:
        freqDict = rareDictDe
    elif lang == Languages_Used.FRANCE:
        freqDict = rareDictFr
    else:
        freqDict = rareDictEn
    rareDensity = rareWordDensity(text, freqDict)

    return AnalysisResult(
        language=lang,
        flesch_index=flesch,
        flesch_kincaid=kincaid,
        interpretation=interpretationFl,
        polarity=polarity,
        subjectivity=subj,
        lexical_diversity=diversity,
        rare_word_density=rareDensity,
        stats=stats
    )

def analyzeBatchService(texts: list[str], **deps) -> list[AnalysisResult]:
    # Итоговая функция для большего массива текстов
    return [analyzeTextService(t, **deps) for t in texts]





