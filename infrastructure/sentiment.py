from domain.types import Polarity, Languages_Used
from textblob import TextBlob
from infrastructure.language_detector import detect_language


def analyzeSentiment(text: str) -> tuple[Polarity, float]:
    lang = detect_language(text)

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if lang != Languages_Used.ENGLISH:
        try:
            translated = blob.translate(to='en')
            if translated and str(translated).strip():
                blob = TextBlob(str(translated))
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
        except:
            pass

    if polarity > 0.1:
        p = Polarity.Positive

    elif polarity < -0.1:
        p = Polarity.Negative

    else:
        p = Polarity.Neutral

    return p, subjectivity
