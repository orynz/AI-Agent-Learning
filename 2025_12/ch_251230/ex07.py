import urllib.request
import time
from datetime import datetime

url = "https://mimgnews.pstatic.net/image/origin/015/2025/07/03/5153123.jpg"

start = time.time()
path = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_"test.jpg"'

urllib.request.urlretrieve(url, path)
print(time.time() - start)