# accuracy_score.py
from utils import path_mgr
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd

y_true = [1, 0, 0, 1, 0, 1, 0, 0, 1, 1]  # 실제 정답 (1: 스팸, 0: 정상)
y_pred = [1, 0, 0, 0, 0, 1, 1, 0, 1, 1]  # AI가 예측한 값


accuracy = accuracy_score(y_true, y_pred)
print(f"모델 정확도: {accuracy * 100}%")

report = classification_report(y_true, y_pred, target_names=["정상", "스팸"])
print("\n----- 상세 평가 보고서 -----")
print(report)

conf_matrix = confusion_matrix(y_true, y_pred)
df_conf = pd.DataFrame(
    conf_matrix, 
    columns=['예측_정상', '예측_스팸'],
    index=['실제_정상', '실제_스팸']
)
print("\n ----- 혼동행렬 -----")
print(df_conf)