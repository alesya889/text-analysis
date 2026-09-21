from domain.types import Polarity
import pytest
from unittest.mock import patch
from infrastructure.sentiment import analyzeSentiment


def test_analyzeSentiment_positive():
  polarity, _ = analyzeSentiment("I love this t-shirt!")
  assert polarity == Polarity.Positive


def test_analyzeSentiment_negative():
  polarity, _ = analyzeSentiment("I hate this t-shirt!")
  assert polarity == Polarity.Negative


def test_analyzeSentiment_neutral():
  polarity, _ = analyzeSentiment("It is a mark.")
  assert polarity == Polarity.Neutral


@patch('infrastructure.sentiment.GoogleTranslator')
def test_analyzeSentiment_russian_mock(mock_translator):
  mock_translator.return_value.translate.return_value = "I hate this day!"
  polarity, _ = analyzeSentiment("Я ненавижу этот день!")
  assert polarity == Polarity.Negative


@patch('infrastructure.sentiment.GoogleTranslator')
def test_analyzeSentiment_german_mock(mock_translator):
  mock_translator.return_value.translate.return_value = (
    "I hate this product, it is absolutely useless and a total disappointment."
  )
  polarity, _ = analyzeSentiment(
    "Ich hasse dieses Produkt, es ist absolut nutzlos und eine totale Enttäuschung."
  )
  assert polarity == Polarity.Negative
