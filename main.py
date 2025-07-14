from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Привіт, хто ти?"}]
)

print("\n✅ GPT ВІДПОВІДЬ:")
print(response.choices[0].message.content)
