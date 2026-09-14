from fastapi import Depends
from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentiment

#Функции-поставщики (Providers).
#FastAPI вызовет их, чтобы получить реальную функцию/объект.
def get_language_detector():
    return detectLanguage

def get_sentiment_analyzer():
    return analyzeSentiment