import datetime

def now() -> str:
    """현재 시간을 리턴한다."""
    return str(datetime.datetime.now())

def save(f_name, text):
    with open(f_name, "w", encoding="utf-8")  as f:
        f.write(now() + text)
        
def save(f_name, text):
    with open(f_name, "r", encoding="utf-8")  as f:
        f.write(text)

    