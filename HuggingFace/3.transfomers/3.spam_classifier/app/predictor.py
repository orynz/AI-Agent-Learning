import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "spam_model.pkl")


class SpamPredictor:
    def __init__(self):
        path = os.path.abspath(MODEL_PATH)
        if not os.path.exists(path):
            raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {path}\n'python run_pipeline.py' 를 먼저 실행하세요.")
        self.model, self.vectorizer = joblib.load(path)

    def predict(self, text: str) -> dict:
        vec          = self.vectorizer.transform([text])
        pred         = int(self.model.predict(vec)[0])
        proba        = self.model.predict_proba(vec)[0]
        spam_prob    = float(proba[1])
        class_prob   = float(proba[pred])

        label    = "spam" if pred == 1 else "ham"
        label_ko = "스팸" if pred == 1 else "정상"

        if spam_prob >= 0.75:
            risk = "높음"
        elif spam_prob >= 0.4:
            risk = "중간"
        else:
            risk = "낮음"

        return {
            "label":            label,
            "label_ko":         label_ko,
            "probability":      class_prob,
            "spam_probability": spam_prob,
            "risk_level":       risk,
        }


# 싱글톤
predictor = SpamPredictor()