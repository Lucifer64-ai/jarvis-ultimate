"""
ML-движок JARVIS для распознавания команд
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline


class MLEngine:
    """ML для классификации голосовых команд."""

    def __init__(self, brain):
        self.brain = brain
        self.model_path = Path("models/command_classifier.joblib")
        self.model: Optional[Pipeline] = None
        self.classes: List[str] = []
        
        # Загрузка модели если существует
        if self.model_path.exists():
            self._load_model()
        else:
            self._train_default_model()

    def _train_default_model(self):
        """Обучение базовой модели на примерах."""
        # Примеры команд и их категории
        training_data = {
            "system_shutdown": ["выключи компьютер", "выключи пк", "заверши работу"],
            "system_restart": ["перезагрузи компьютер", "перезагрузи пк", "рестарт"],
            "system_lock": ["заблокируй экран", "заблокируй компьютер", "лок"],
            "info_time": ["который час", "сколько времени", "время"],
            "info_date": ["какая дата", "какое сегодня число", "дата"],
            "info_weather": ["какая погода", "погода на сегодня", "прогноз погоды"],
            "app_notepad": ["открой блокнот", "запусти notepad", "открой заметки"],
            "app_calculator": ["открой калькулятор", "запусти калькулятор"],
            "app_youtube": ["открой ютуб", "открой youtube", "запусти ютуб"],
            "control_volume": ["громкость", "сделай громче", "сделай тише"],
            "control_mute": ["без звука", "выключи звук", "mute"],
            "control_minimize": ["сверни все окна", "покажи рабочий стол", "минимизировать"],
            "network_speed": ["тест скорости", "скорость интернета", "проверь интернет"],
            "network_ip": ["какой ip адрес", "мой ip", "айпи адрес"],
        }
        
        X = []
        y = []
        
        for category, examples in training_data.items():
            for example in examples:
                X.append(example)
                y.append(category)
        
        # Создание pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 5))),
            ('svm', SVC(kernel='linear', probability=True))
        ])
        
        # Обучение
        self.model.fit(X, y)
        self.classes = self.model.classes_.tolist()
        
        # Сохранение модели
        self._save_model()
        self.brain.logger.info(f"ML модель обучена на {len(X)} примерах")

    def _save_model(self):
        """Сохранение модели."""
        self.model_path.parent.mkdir(exist_ok=True)
        joblib.dump({
            'model': self.model,
            'classes': self.classes
        }, self.model_path)

    def _load_model(self):
        """Загрузка модели."""
        try:
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.classes = data['classes']
            self.brain.logger.info("ML модель загружена")
        except Exception as e:
            self.brain.logger.error(f"Ошибка загрузки ML модели: {e}")
            self._train_default_model()

    def predict(self, text: str) -> Dict:
        """Предсказание категории команды."""
        if not self.model:
            return {"status": "error", "message": "Модель не загружена"}
        
        try:
            prediction = self.model.predict([text])[0]
            probabilities = self.model.predict_proba([text])[0]
            confidence = float(np.max(probabilities))
            
            return {
                "status": "ok",
                "category": prediction,
                "confidence": round(confidence, 3),
                "text": text
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def add_training_data(self, category: str, examples: List[str]):
        """Добавление данных для переобучения."""
        # В реальной реализации нужно сохранять в файл и переобучать
        self.brain.logger.info(f"Добавлено {len(examples)} примеров для категории {category}")
