"""
ÐÐ´Ð°Ð¿ÑÐ¸Ð²Ð½ÑÐ¹ ML-Ð´Ð²Ð¸Ð¶Ð¾Ðº JARVIS Ñ Ð¾Ð½Ð»Ð°Ð¹Ð½-Ð¾Ð±ÑÑÐµÐ½Ð¸ÐµÐ¼
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC


class AdaptiveMLEngine:
    """ML-Ð´Ð²Ð¸Ð¶Ð¾Ðº Ñ Ð²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ð¾ÑÑÑÑ Ð´Ð¾Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð½Ð° Ð½Ð¾Ð²ÑÑ Ð´Ð°Ð½Ð½ÑÑ."""

    def __init__(self, brain):
        self.brain = brain
        self.model_path = Path("models/adaptive_classifier.joblib")
        self.training_data_path = Path("data/training_data.json")
        self.confidence_threshold = 0.7

        self.model: Optional[Pipeline] = None
        self.training_data: Dict = self._load_training_data()
        self.classes: List[str] = []

        if self.model_path.exists():
            self._load_model()
        else:
            self._train_initial_model()

    def _build_model(self) -> Pipeline:
        """Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ pipeline Ð¼Ð¾Ð´ÐµÐ»Ð¸."""
        return Pipeline([
            ("tfidf", TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 5))),
            ("svm", SVC(kernel="linear", probability=True)),
        ])

    def _prepare_training_batch(self):
        """ÐÐ¾Ð´Ð³Ð¾ÑÐ¾Ð²ÐºÐ° X/y Ð¸Ð· Ð¾Ð±ÑÑÐ°ÑÑÐ¸Ñ Ð´Ð°Ð½Ð½ÑÑ, Ð¾ÑÐ±ÑÐ°ÑÑÐ²Ð°Ñ Ð½ÐµÐºÐ¾ÑÑÐµÐºÑÐ½ÑÐµ Ð·Ð°Ð¿Ð¸ÑÐ¸."""
        X = []
        y = []

        for category, examples in self.training_data.items():
            if not isinstance(category, str) or not isinstance(examples, list):
                continue
            for example in examples:
                if isinstance(example, str) and example.strip():
                    X.append(example.strip())
                    y.append(category)

        return X, y

    def _load_training_data(self) -> Dict:
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¾Ð±ÑÑÐ°ÑÑÐ¸Ñ Ð´Ð°Ð½Ð½ÑÑ."""
        if self.training_data_path.exists():
            with open(self.training_data_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, dict):
                return data
        return self._get_default_training_data()

    def _save_training_data(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð¾Ð±ÑÑÐ°ÑÑÐ¸Ñ Ð´Ð°Ð½Ð½ÑÑ."""
        self.training_data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.training_data_path, "w", encoding="utf-8") as file:
            json.dump(self.training_data, file, ensure_ascii=False, indent=2)

    def _get_default_training_data(self) -> Dict:
        """ÐÐ°ÑÐ°Ð»ÑÐ½ÑÐµ Ð¾Ð±ÑÑÐ°ÑÑÐ¸Ðµ Ð´Ð°Ð½Ð½ÑÐµ."""
        return {
            "system_shutdown": ["Ð²ÑÐºÐ»ÑÑÐ¸ ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑ", "Ð²ÑÐºÐ»ÑÑÐ¸ Ð¿Ðº", "Ð·Ð°Ð²ÐµÑÑÐ¸ ÑÐ°Ð±Ð¾ÑÑ"],
            "system_restart": ["Ð¿ÐµÑÐµÐ·Ð°Ð³ÑÑÐ·Ð¸ ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑ", "Ð¿ÐµÑÐµÐ·Ð°Ð³ÑÑÐ·Ð¸ Ð¿Ðº", "ÑÐµÑÑÐ°ÑÑ"],
            "system_lock": ["Ð·Ð°Ð±Ð»Ð¾ÐºÐ¸ÑÑÐ¹ ÑÐºÑÐ°Ð½", "Ð·Ð°Ð±Ð»Ð¾ÐºÐ¸ÑÑÐ¹ ÐºÐ¾Ð¼Ð¿ÑÑÑÐµÑ", "Ð»Ð¾Ðº"],
            "info_time": ["ÐºÐ¾ÑÐ¾ÑÑÐ¹ ÑÐ°Ñ", "ÑÐºÐ¾Ð»ÑÐºÐ¾ Ð²ÑÐµÐ¼ÐµÐ½Ð¸", "Ð²ÑÐµÐ¼Ñ"],
            "info_date": ["ÐºÐ°ÐºÐ°Ñ Ð´Ð°ÑÐ°", "ÐºÐ°ÐºÐ¾Ðµ ÑÐµÐ³Ð¾Ð´Ð½Ñ ÑÐ¸ÑÐ»Ð¾", "Ð´Ð°ÑÐ°"],
            "info_weather": ["ÐºÐ°ÐºÐ°Ñ Ð¿Ð¾Ð³Ð¾Ð´Ð°", "Ð¿Ð¾Ð³Ð¾Ð´Ð° Ð½Ð° ÑÐµÐ³Ð¾Ð´Ð½Ñ", "Ð¿ÑÐ¾Ð³Ð½Ð¾Ð· Ð¿Ð¾Ð³Ð¾Ð´Ñ"],
            "app_notepad": ["Ð¾ÑÐºÑÐ¾Ð¹ Ð±Ð»Ð¾ÐºÐ½Ð¾Ñ", "Ð·Ð°Ð¿ÑÑÑÐ¸ notepad", "Ð¾ÑÐºÑÐ¾Ð¹ Ð·Ð°Ð¼ÐµÑÐºÐ¸"],
            "app_calculator": ["Ð¾ÑÐºÑÐ¾Ð¹ ÐºÐ°Ð»ÑÐºÑÐ»ÑÑÐ¾Ñ", "Ð·Ð°Ð¿ÑÑÑÐ¸ ÐºÐ°Ð»ÑÐºÑÐ»ÑÑÐ¾Ñ"],
            "app_youtube": ["Ð¾ÑÐºÑÐ¾Ð¹ ÑÑÑÐ±", "Ð¾ÑÐºÑÐ¾Ð¹ youtube", "Ð·Ð°Ð¿ÑÑÑÐ¸ ÑÑÑÐ±"],
            "control_volume": ["Ð³ÑÐ¾Ð¼ÐºÐ¾ÑÑÑ", "ÑÐ´ÐµÐ»Ð°Ð¹ Ð³ÑÐ¾Ð¼ÑÐµ", "ÑÐ´ÐµÐ»Ð°Ð¹ ÑÐ¸ÑÐµ"],
            "control_mute": ["Ð±ÐµÐ· Ð·Ð²ÑÐºÐ°", "Ð²ÑÐºÐ»ÑÑÐ¸ Ð·Ð²ÑÐº", "mute"],
            "control_minimize": ["ÑÐ²ÐµÑÐ½Ð¸ Ð²ÑÐµ Ð¾ÐºÐ½Ð°", "Ð¿Ð¾ÐºÐ°Ð¶Ð¸ ÑÐ°Ð±Ð¾ÑÐ¸Ð¹ ÑÑÐ¾Ð»", "Ð¼Ð¸Ð½Ð¸Ð¼Ð¸Ð·Ð¸ÑÐ¾Ð²Ð°ÑÑ"],
            "network_speed": ["ÑÐµÑÑ ÑÐºÐ¾ÑÐ¾ÑÑÐ¸", "ÑÐºÐ¾ÑÐ¾ÑÑÑ Ð¸Ð½ÑÐµÑÐ½ÐµÑÐ°", "Ð¿ÑÐ¾Ð²ÐµÑÑ Ð¸Ð½ÑÐµÑÐ½ÐµÑ"],
            "network_ip": ["ÐºÐ°ÐºÐ¾Ð¹ ip Ð°Ð´ÑÐµÑ", "Ð¼Ð¾Ð¹ ip", "Ð°Ð¹Ð¿Ð¸ Ð°Ð´ÑÐµÑ"],
        }

    def _train_initial_model(self):
        """ÐÐ±ÑÑÐµÐ½Ð¸Ðµ Ð½Ð°ÑÐ°Ð»ÑÐ½Ð¾Ð¹ Ð¼Ð¾Ð´ÐµÐ»Ð¸."""
        X, y = self._prepare_training_batch()
        if len(set(y)) < 2:
            self.model = None
            self.classes = []
            self.brain.logger.warning("ÐÐµÐ´Ð¾ÑÑÐ°ÑÐ¾ÑÐ½Ð¾ ÐºÐ°ÑÐµÐ³Ð¾ÑÐ¸Ð¹ Ð´Ð»Ñ Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð°Ð´Ð°Ð¿ÑÐ¸Ð²Ð½Ð¾Ð¹ ML Ð¼Ð¾Ð´ÐµÐ»Ð¸")
            return

        model = self._build_model()
        model.fit(X, y)
        self.model = model
        self.classes = model.classes_.tolist()
        self._save_model()
        self.brain.logger.info(f"ÐÐ´Ð°Ð¿ÑÐ¸Ð²Ð½Ð°Ñ ML Ð¼Ð¾Ð´ÐµÐ»Ñ Ð¾Ð±ÑÑÐµÐ½Ð° Ð½Ð° {len(X)} Ð¿ÑÐ¸Ð¼ÐµÑÐ°Ñ")

    def _save_model(self):
        """Ð¡Ð¾ÑÑÐ°Ð½ÐµÐ½Ð¸Ðµ Ð¼Ð¾Ð´ÐµÐ»Ð¸."""
        if self.model is None:
            return
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({
            "model": self.model,
            "classes": self.classes,
            "training_data": self.training_data,
        }, self.model_path)

    def _load_model(self):
        """ÐÐ°Ð³ÑÑÐ·ÐºÐ° Ð¼Ð¾Ð´ÐµÐ»Ð¸."""
        try:
            data = joblib.load(self.model_path)
            model = data["model"]
            classes = data.get("classes", getattr(model, "classes_", [])).tolist()
            self.model = model
            self.classes = classes
            self.training_data = data.get("training_data", self.training_data)
            self.brain.logger.info("ÐÐ´Ð°Ð¿ÑÐ¸Ð²Ð½Ð°Ñ ML Ð¼Ð¾Ð´ÐµÐ»Ñ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ð°")
        except Exception as error:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð·Ð°Ð³ÑÑÐ·ÐºÐ¸ Ð¼Ð¾Ð´ÐµÐ»Ð¸: {error}")
            self._train_initial_model()

    def predict(self, text: str) -> Dict:
        """ÐÑÐµÐ´ÑÐºÐ°Ð·Ð°Ð½Ð¸Ðµ Ñ Ð¿ÑÐ¾Ð²ÐµÑÐºÐ¾Ð¹ ÑÐ²ÐµÑÐµÐ½Ð½Ð¾ÑÑÐ¸."""
        if self.model is None:
            return {"status": "error", "message": "ÐÐ¾Ð´ÐµÐ»Ñ Ð½Ðµ Ð·Ð°Ð³ÑÑÐ¶ÐµÐ½Ð°"}
        if not isinstance(text, str) or not text.strip():
            return {"status": "error", "message": "Ð¢ÐµÐºÑÑ ÐºÐ¾Ð¼Ð°Ð½Ð´Ñ Ð¿ÑÑÑ"}

        try:
            prediction = self.model.predict([text.strip()])[0]
            probabilities = self.model.predict_proba([text.strip()])[0]
            confidence = float(np.max(probabilities))
            result = {
                "status": "ok",
                "category": prediction,
                "confidence": round(confidence, 3),
                "text": text,
                "needs_learning": confidence < self.confidence_threshold,
            }
            if confidence < self.confidence_threshold:
                result["suggestion"] = f"Ð¯ Ð½Ðµ ÑÐ²ÐµÑÐµÐ½, ÑÑÐ¾ ÑÑÐ¾ '{prediction}'. Ð¥Ð¾ÑÐ¸ÑÐµ Ð½Ð°ÑÑÐ¸ÑÑ Ð¼ÐµÐ½Ñ?"
            return result
        except Exception as error:
            return {"status": "error", "message": str(error)}

    def add_training_example(self, text: str, category: str) -> Dict:
        """ÐÐ¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¸Ðµ Ð½Ð¾Ð²Ð¾Ð³Ð¾ Ð¿ÑÐ¸Ð¼ÐµÑÐ° Ð¸ Ð¿ÐµÑÐµÐ¾Ð±ÑÑÐµÐ½Ð¸Ðµ."""
        if not isinstance(text, str) or not text.strip() or not isinstance(category, str) or not category.strip():
            return {"status": "error", "message": "ÐÑÐ¶Ð½Ñ Ð½ÐµÐ¿ÑÑÑÑÐµ ÑÐµÐºÑÑ Ð¸ ÐºÐ°ÑÐµÐ³Ð¾ÑÐ¸Ñ"}

        text = text.strip()
        category = category.strip()
        examples = self.training_data.setdefault(category, [])
        if text in examples:
            return {"status": "ok", "message": "Ð­ÑÐ¾Ñ Ð¿ÑÐ¸Ð¼ÐµÑ ÑÐ¶Ðµ ÐµÑÑÑ"}

        examples.append(text)
        self._save_training_data()
        if not self._retrain_model():
            examples.remove(text)
            if not examples:
                del self.training_data[category]
            self._save_training_data()
            return {"status": "error", "message": "ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð¿ÐµÑÐµÐ¾Ð±ÑÑÐ¸ÑÑ Ð¼Ð¾Ð´ÐµÐ»Ñ; Ð´Ð°Ð½Ð½ÑÐµ Ð½Ðµ Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ñ"}

        self.brain.logger.info(f"ÐÐ¾Ð±Ð°Ð²Ð»ÐµÐ½ Ð¿ÑÐ¸Ð¼ÐµÑ '{text}' Ð² ÐºÐ°ÑÐµÐ³Ð¾ÑÐ¸Ñ '{category}'")
        return {
            "status": "ok",
            "message": f"ÐÐ±ÑÑÐµÐ½ Ð½Ð¾Ð²Ð¾Ð¹ ÐºÐ¾Ð¼Ð°Ð½Ð´Ðµ: '{text}' â {category}",
            "total_examples": len(self.training_data[category]),
        }

    def _retrain_model(self) -> bool:
        """ÐÐµÑÐµÐ¾Ð±ÑÑÐµÐ½Ð¸Ðµ Ð½Ð° Ð²ÑÐµÑ Ð´Ð°Ð½Ð½ÑÑ Ð±ÐµÐ· Ð·Ð°Ð¼ÐµÐ½Ñ ÑÐ°Ð±Ð¾ÑÐµÐ¹ Ð¼Ð¾Ð´ÐµÐ»Ð¸ Ð¿ÑÐ¸ Ð¾ÑÐ¸Ð±ÐºÐµ."""
        X, y = self._prepare_training_batch()
        if not X or len(set(y)) < 2:
            self.brain.logger.warning("ÐÐµÐ²Ð¾Ð·Ð¼Ð¾Ð¶Ð½Ð¾ Ð¿ÐµÑÐµÐ¾Ð±ÑÑÐ¸ÑÑ Ð¼Ð¾Ð´ÐµÐ»Ñ: Ð½ÑÐ¶Ð½Ñ Ð¿ÑÐ¸Ð¼ÐµÑÑ Ð¼Ð¸Ð½Ð¸Ð¼ÑÐ¼ Ð´Ð²ÑÑ ÐºÐ°ÑÐµÐ³Ð¾ÑÐ¸Ð¹")
            return False

        try:
            candidate = self._build_model()
            candidate.fit(X, y)
            self.model = candidate
            self.classes = candidate.classes_.tolist()
            self._save_model()
            self.brain.logger.info(f"ÐÐ¾Ð´ÐµÐ»Ñ Ð¿ÐµÑÐµÐ¾Ð±ÑÑÐµÐ½Ð° Ð½Ð° {len(X)} Ð¿ÑÐ¸Ð¼ÐµÑÐ°Ñ")
            return True
        except Exception as error:
            self.brain.logger.error(f"ÐÑÐ¸Ð±ÐºÐ° Ð¿ÐµÑÐµÐ¾Ð±ÑÑÐµÐ½Ð¸Ñ Ð¼Ð¾Ð´ÐµÐ»Ð¸: {error}")
            return False

    def create_new_category(self, category_name: str, examples: List[str]) -> Dict:
        """Ð¡Ð¾Ð·Ð´Ð°Ð½Ð¸Ðµ Ð½Ð¾Ð²Ð¾Ð¹ ÐºÐ°ÑÐµÐ³Ð¾ÑÐ¸Ð¸ ÐºÐ¾Ð¼Ð°Ð½Ð´."""
        if not isinstance(category_name, str) or not category_name.strip():
            return {"status": "error", "message": "ÐÐ°Ð·Ð²Ð°Ð½Ð¸Ðµ ÐºÐ°ÑÐµÐ³Ð¾ÑÐ¸Ð¸ Ð½Ðµ Ð´Ð¾Ð»Ð¶Ð½Ð¾ Ð±ÑÑÑ Ð¿ÑÑÑÑÐ¼"}
        category_name = category_name.strip()
        if category_name in self.training_data:
            return {"status": "error", "message": "ÐÐ°ÑÐµÐ³Ð¾ÑÐ¸Ñ ÑÐ¶Ðµ ÑÑÑÐµÑÑÐ²ÑÐµÑ"}
        if not isinstance(examples, list) or not any(isinstance(item, str) and item.strip() for item in examples):
            return {"status": "error", "message": "ÐÐ¾Ð±Ð°Ð²ÑÑÐµ ÑÐ¾ÑÑ Ð±Ñ Ð¾Ð´Ð¸Ð½ Ð½ÐµÐ¿ÑÑÑÐ¾Ð¹ Ð¿ÑÐ¸Ð¼ÐµÑ"}

        cleaned_examples = list(dict.fromkeys(item.strip() for item in examples if isinstance(item, str) and item.strip()))
        self.training_data[category_name] = cleaned_examples
        if not self._retrain_model():
            del self.training_data[category_name]
            return {"status": "error", "message": "ÐÐµ ÑÐ´Ð°Ð»Ð¾ÑÑ Ð¾Ð±ÑÑÐ¸ÑÑ Ð¼Ð¾Ð´ÐµÐ»Ñ Ð½Ð° Ð½Ð¾Ð²Ð¾Ð¹ ÐºÐ°ÑÐµÐ³Ð¾ÑÐ¸Ð¸"}
        self._save_training_data()
        return {
            "status": "ok",
            "message": f"Ð¡Ð¾Ð·Ð´Ð°Ð½Ð° Ð½Ð¾Ð²Ð°Ñ ÐºÐ°ÑÐµÐ³Ð¾ÑÐ¸Ñ '{category_name}' Ñ {len(cleaned_examples)} Ð¿ÑÐ¸Ð¼ÐµÑÐ°Ð¼Ð¸",
        }

    def get_training_stats(self) -> Dict:
        """Ð¡ÑÐ°ÑÐ¸ÑÑÐ¸ÐºÐ° Ð¾Ð±ÑÑÐµÐ½Ð¸Ñ."""
        total_examples = sum(len(examples) for examples in self.training_data.values() if isinstance(examples, list))
        return {
            "categories": len(self.training_data),
            "total_examples": total_examples,
            "categories_list": list(self.training_data.keys()),
            "confidence_threshold": self.confidence_threshold,
        }

    def set_confidence_threshold(self, threshold: float):
        """Ð£ÑÑÐ°Ð½Ð¾Ð²ÐºÐ° Ð¿Ð¾ÑÐ¾Ð³Ð° ÑÐ²ÐµÑÐµÐ½Ð½Ð¾ÑÑÐ¸."""
        self.confidence_threshold = max(0.1, min(1.0, threshold))
        self.brain.logger.info(f"ÐÐ¾ÑÐ¾Ð³ ÑÐ²ÐµÑÐµÐ½Ð½Ð¾ÑÑÐ¸ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½ Ð½Ð° {self.confidence_threshold}")
