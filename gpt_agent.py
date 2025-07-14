import os
import openai
from agent_reader import read_memory
from agent_writer import write_memory

# Завантаження OpenAI API ключа
with open('.env', 'r') as f:
    for line in f:
        if line.startswith('OPENAI_API_KEY'):
            openai.api_key = line.strip().split('=')[1]

def run_conversation(user_prompt):
    system_log = read_memory()

    messages = [
        {"role": "system", "content": "Ти GPT-помічник, що працює у Telegram-боті."},
        {"role": "user", "content": user_prompt}
    ]

    if system_log:
        messages.insert(1, {"role": "system", "content": "Контекст памʼяті GPT:\n" + system_log})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.5,
            max_tokens=1000
        )
        reply = response['choices'][0]['message']['content'].strip()
        log_entry = f"\n\n🔹 Запит: {user_prompt}\n🔸 Відповідь: {reply}"
        write_memory(log_entry)
        return reply
    except Exception as e:
        return f"[X] Помилка при зверненні до GPT: {e}"

if __name__ == "__main__":
    user_input = input("Введи запит до GPT: ")
    answer = run_conversation(user_input)
    print("\n🤖 GPT ВІДПОВІДЬ:")
    print(answer)
