from infrastructure.syllable_counters import countSyllablesEn, countSyllablesRu, countSyllablesGe, countSyllablesFr, getSyllableCounter
from domain.types import Languages_Used

def test_countSyllablesEn_1():
    assert countSyllablesEn('cat') == 1

def test_countSyllablesEn_2():
    assert countSyllablesEn('water') == 2

def test_countSyllablesEn_3():
    assert countSyllablesEn('beautiful') == 3

def test_countSyllablesEn_capitalized():
    assert countSyllablesEn('BANANA') == 3

def test_countSyllablesEn_empty():
    assert countSyllablesEn('') == 0

def test_countSyllablesEn_without_vowels():
    assert countSyllablesEn('tsk') == 0

def test_countSyllablesEn_diphthongs():
    assert countSyllablesEn('coin') == 1

def test_countSyllablesEn_with_silent_vowels():
    assert countSyllablesEn('cake') == 1

def test_countSyllablesRu_1():
    assert countSyllablesRu('кот') == 1

def test_countSyllablesRu_2():
    assert countSyllablesRu('мама') == 2

def test_countSyllablesRu_3():
    assert countSyllablesRu('яблоко') == 3

def test_countSyllablesRu_yo():
    assert countSyllablesRu('ёжик') == 2

def test_countSyllablesRu_without_vowels():
    assert countSyllablesRu('брр') == 0

def test_countSyllablesRu_capitalized():
    assert countSyllablesRu('МАМА') == 2

def test_countSyllablesRu_empty():
    assert countSyllablesRu('') == 0

def test_countSyllablesRu_ya():
    assert countSyllablesRu('яма') == 2

def test_countSyllablesRu_yu():
    assert countSyllablesRu('юла') == 2

def test_countSyllablesRu_ye():
    assert countSyllablesRu('ель') == 1

def test_countSyllablesRu_all_yotated():
    assert countSyllablesRu('яюеё') == 4

def test_countSyllablesRu_long_word():
    assert countSyllablesRu('достопримечательность') == 7

def test_countSyllablesRu_hyphen():
    assert countSyllablesRu('кто-то') == 2

def test_countSyllablesGe_1():
    assert countSyllablesGe('haus') == 1

def test_countSyllablesGe_2():
    assert countSyllablesGe('katze') == 2

def test_countSyllablesGe_3():
    assert countSyllablesGe('computer') == 3

def test_countSyllablesGe_long_word():
    assert countSyllablesGe('universität') == 4

def test_countSyllablesGe_empty():
    assert countSyllablesGe('') == 0

def test_countSyllablesGe_umlaut():
    assert countSyllablesGe('Bücher') == 2

def test_countSyllablesGe_eszett():
    assert countSyllablesGe('Straße') == 2

def test_countSyllablesGe_feuer():
    assert countSyllablesGe('feuer') == 2

def test_countSyllablesGe_compound_long():
    assert countSyllablesGe('Autobahn') == 3

def test_countSyllablesGe_capitalized():
    assert countSyllablesGe('HAUS') == 1

def test_countSyllablesFr_1():
    assert countSyllablesFr('chien') == 1

def test_countSyllablesFr_2():
    assert countSyllablesFr('bonjour') == 2

def test_countSyllablesFr_3():
    assert countSyllablesFr('liberté') == 3

def test_countSyllablesFr_long_word():
    assert countSyllablesFr('ordinateur') == 4

def test_countSyllablesFr_cedille():
    assert countSyllablesFr('français') == 2

def test_countSyllablesFr_empty():
    assert countSyllablesFr('') == 0

def test_countSyllablesFr_apostrophe():
    assert countSyllablesFr("aujourd'hui") == 3

def test_getSyllableCounter_english():
    assert getSyllableCounter(Languages_Used.ENGLISH) is countSyllablesEn

def test_getSyllableCounter_russian():
    assert getSyllableCounter(Languages_Used.RUSSIAN) is countSyllablesRu

def test_getSyllableCounter_german():
    assert getSyllableCounter(Languages_Used.GERMAN) is countSyllablesGe

def test_getSyllableCounter_french():
    assert getSyllableCounter(Languages_Used.FRANCE) is countSyllablesFr

def test_getSyllableCounter_english_behavior():
    counter = getSyllableCounter(Languages_Used.ENGLISH)
    assert counter('cat') == 1
    assert counter('water') == 2

def test_getSyllableCounter_russian_behavior():
    counter = getSyllableCounter(Languages_Used.RUSSIAN)
    assert counter('кот') == 1
    assert counter('мама') == 2

def test_getSyllableCounter_german_behavior():
    counter = getSyllableCounter(Languages_Used.GERMAN)
    assert counter('haus') == 1

def test_getSyllableCounter_french_behavior():
    counter = getSyllableCounter(Languages_Used.FRANCE)
    assert counter('liberté') == 3

def test_getSyllableCounter_all_languages():
    for lang in Languages_Used:
        counter = getSyllableCounter(lang)
        assert callable(counter), f"Нет счётчика для языка {lang}"
        assert isinstance(counter("test"), int)

def test_getSyllableCounter_unknown_language():
    for lang in Languages_Used:
        assert callable(getSyllableCounter(lang))
