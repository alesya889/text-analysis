const API_URL = 'http://127.0.0.1:8000';

document.addEventListener('DOMContentLoaded', function() {
  const textInput = document.getElementById('textInput');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const clearBtn = document.getElementById('clearBtn');
  const exampleBtn = document.getElementById('exampleBtn');
  const resultDiv = document.getElementById('result');
  const resultContent = document.getElementById('resultContent');
  const loadingDiv = document.getElementById('loading');

  // Примеры текстов
  const examples = [
  'Ты не бойся ночи, ведь я рядом. Я ангелом буду твоим навсегда.',
  'Donnez-moi une suite au Ritz, je nen veux pas! Des bijoux de chez Chanel, je nen veux pas!',
  'The quick brown fox jumps over the lazy dog. This is a test sentence. Six seven.',
  'Она танцует под Шаде, танцы прямо во тьме. Я знаю что ты не в себе.',
  'Eins. Hier kommt die Sonne. Zwei. Hier kommt die Sonne. Drei. Sie ist der hellste Stern von allen. Vier. Hier kommt die Sonne'
  ];

  // Кнопка "Пример"
  exampleBtn.addEventListener('click', function() {
    const randomExample = examples[Math.floor(Math.random() * examples.length)];
    textInput.value = randomExample;
    resultDiv.style.display = 'none';
  });

  // Кнопка "Очистить"
  clearBtn.addEventListener('click', function() {
    textInput.value = '';
    resultDiv.style.display = 'none';
  });

  // Кнопка "Анализировать"
  analyzeBtn.addEventListener('click', function() {
    const text = textInput.value.trim();
    if (!text) {
      alert('Введите текст!');
      return;
    }

    // Показываем загрузку
    loadingDiv.style.display = 'block';
    resultDiv.style.display = 'none';
    analyzeBtn.disabled = true;

    // Отправляем запрос
    fetch(API_URL + '/analyze', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text: text})
    })
    .then(response => response.json())
    .then(data => {
      loadingDiv.style.display = 'none';
      analyzeBtn.disabled = false;

      if (data.status === 'success') {
        showResult(data.result, data.cached, data.processing_time);
      } else {
        alert('Ошибка: ' + JSON.stringify(data));
      }
    })
    .catch(error => {
      loadingDiv.style.display = 'none';
      analyzeBtn.disabled = false;
      alert('Ошибка: ' + error.message);
    });
  });

  // Показываем результат
  function showResult(result, fromCache, time) {
    resultDiv.style.display = 'block';

    // Информация о кэше
    const cacheInfo = fromCache ? 'Анализ из кэша' : 'Новый анализ';

    resultContent.innerHTML = `
            <p><strong>Язык:</strong> ${result.language}</p>
            <p><strong>Тональность:</strong> ${result.polarity}</p>
            <p><strong>Субъективность:</strong> ${(result.subjectivity * 100).toFixed(1)}%</p>
            <p><strong>Индекс Флеша:</strong> ${result.flesch_index.toFixed(2)}</p>
            <p><strong>Уровень сложности:</strong> ${result.interpretation}</p>
            <p><strong>Лексическое разнообразие:</strong> ${(result.lexical_diversity * 100).toFixed(1)}%</p>
            <p><strong>Время обработки:</strong> ${time.toFixed(2)} сек</p>
            <p><strong>${cacheInfo}</strong></p>
            <hr>
            <h4>Статистика:</h4>
            <div class="stat-grid">
                <div class="stat-card">
                    <h4>Предложения</h4>
                    <p>${result.stats.sentence_count}</p>
                </div>
                <div class="stat-card">
                    <h4>Слова</h4>
                    <p>${result.stats.word_count}</p>
                </div>
                <div class="stat-card">
                    <h4>Слоги</h4>
                    <p>${result.stats.syllable_count}</p>
                </div>
                <div class="stat-card">
                    <h4>Средняя длина</h4>
                    <p>${result.stats.avg_sentence_length.toFixed(2)} слов в предложении</p>
                </div>
            </div>
        `;
    }
});