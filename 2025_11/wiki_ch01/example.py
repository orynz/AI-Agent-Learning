import pandas as pd

# 인덱스 값 지정된 시리즈 생성:
patient_weight = pd.Series ([48, 89, 50, 72, 88, 84, 90, 101, 103, 60] ,
index = ['환자1', '환자2', '환자3', '환자4', '환자5', '환자6', '환자7', '환자8', '환자9', '환자10'])
print (patient_weight)
