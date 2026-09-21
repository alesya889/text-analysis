from unittest.mock import patch


from domain.types import Polarity
from infrastructure.sentiment import analyzeSentiment


def test_analyzeSentiment_positive():
    # Проверяет положительную полярность текста.
    polarity, _ = analyzeSentiment("I love this t-shirt!")
    assert polarity == Polarity.Positive


def test_analyzeSentiment_negative():
    # Проверяет отрицательную полярность текста.
    polarity, _ = analyzeSentiment("I hate this t-shirt!")
    assert polarity == Polarity.Negative


def test_analyzeSentiment_neutral():
    # Проверяет нейтральную полярность текста.
    polarity, _ = analyzeSentiment("It is a mark.")
    assert polarity == Polarity.Neutral


@patch("infrastructure.sentiment.GoogleTranslator")
def test_analyzeSentiment_russian_mock(mock_translator):
    # Проверяет полярность русского текста с замоканным переводчиком.
    mock_translator.return_value.translate.return_value = "I hate this day!"
    polarity, _ = analyzeSentiment("Я ненавижу этот день!")
    assert polarity == Polarity.Negative


@patch("infrastructure.sentiment.GoogleTranslator")
def test_analyzeSentiment_german_mock(mock_translator):
    # Проверяет полярность немецкого текста с замоканным переводчиком.
    mock_translator.return_value.translate.return_value = (
        "I hate this product, it is absolutely useless and a total disappointment."
    )
    polarity, _ = analyzeSentiment(
        "Ich hasse dieses Produkt, es ist absolut nutzlos und eine totale Enttäuschung."
    )
    assert polarity == Polarity.Negative
