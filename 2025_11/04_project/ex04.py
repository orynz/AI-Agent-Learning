from google.colab import drive
from google.colab import files

# Colab에서 로컬 파일을 업로드할 수 있는 창을 띄움
uploaded = files.upload()

import io, pandas as pd

# 업로드된 파일 이름(key)을 하나 가져옴 (첫 번째 파일 사용)
key = list(uploaded.keys())[0]

# 업로드된 바이너리 데이터를 판다스로 읽기 위해 BytesIO로 변환
df2 = pd.read_csv(io.BytesIO(uploaded[key]))

# 데이터의 앞부분 5행을 미리보기
df2.head()