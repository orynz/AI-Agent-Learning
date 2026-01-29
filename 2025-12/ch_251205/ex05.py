phonebook = {
    "p_list": [
        {"no": 1, "name": "user01", "phone": "010-1231-1234"},
        {"no": 1, "name": "user01", "phone": "010-1231-1234"},
        {"no": 1, "name": "user01", "phone": "010-1231-1234"},
        {"no": 1, "name": "user01", "phone": "010-1231-1234"}
    ]
}


import json

with open("phonebook.json", "w", encoding="utf-8") as f:
    json.dump(phonebook, f, ensure_ascii=False, indent=4)
    
with open("phonebook.json", "r", encoding="utf-8") as f:
    loaded_data = json.load(f)

print(loaded_data)