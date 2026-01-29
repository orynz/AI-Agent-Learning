from openai import OpenAI
from prompt_templates import AD_PROMPT, SNS_PROMPT, YOUTUBE_PROMPT
import os, json

client = OpenAI()
def generate_content(product: str, message: str) -> dict:
    
    contents = {}
    
    def ask(prompt: str) -> str:
        resp = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content":prompt}
            ]
        )
        result = resp.choices[0].message.content or ""
        
        tokens = f"입력: {resp.usage.prompt_tokens}\n" + f"출력: {resp.usage.completion_tokens}\n" + f"총 사용량: {resp.usage.total_tokens}"
        return f"{result}\n\n-----토큰 사용량-----:\n{tokens}"
    
    ad_prompt = AD_PROMPT.format(product=product, message=message)
    sns_prompt = SNS_PROMPT.format(product=product, message=message)
    youtube_prompt = YOUTUBE_PROMPT.format(product=product, message=message)
    
    contents['ad'] = ask(ad_prompt)
    contents['sns'] = ask(sns_prompt)
    contents['youtube'] = ask(youtube_prompt)
    return contents


def save_as_text(contents: dict, base_name: str = "content_output") -> None:
    os.makedirs("outputs", exist_ok=True)
    
    with open (os.path.join("outputs", f"{base_name}_ad.txt"), "w", encoding="utf-8") as f:
        f.write(contents['ad'])
    with open (os.path.join("outputs", f"{base_name}_youtube.txt"), "w", encoding="utf-8") as f:
        f.write(contents['youtube'])
    with open (os.path.join("outputs", f"{base_name}_sns.txt"), "w", encoding="utf-8") as f:
        f.write(contents['sns'])

def save_as_json(contents: dict, base_name: str = "content_output") -> None:
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", f"{base_name}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(contents, f, ensure_ascii=False, indent=2)
    
    
if __name__ == "__main__":
    
    product = input("제품/서비스 이름을 입력하세요: ")
    message = input("핵심 메시지를 입력하세요: ")
    
    result = generate_content(product=product, message=message)
    save_as_text(result, base_name=product)
    save_as_json(result, product)
    
    print("광고문구 ***************************")
    print(result['ad'])
    print()
    print("SNS 게시글 ***************************")
    print(result['sns'])
    print()
    print("유튜브 스크립트 ***************************")
    print(result['youtube'])


