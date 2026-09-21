from infrastructure.language_detector import detectLanguage
from infrastructure.sentiment import analyzeSentiment

#Функции-поставщики (Providers).
def get_language_detector():
  return detectLanguage

def get_sentiment_analyzer():
  return analyzeSentiment