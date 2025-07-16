#!/bin/bash

BOT_PID_FILE="/root/GPT_monitoring/bot.pid"
ALERT_SCRIPT="/root/GPT_monitoring/alert_to_telegram.sh"

# 🔒 Перевірка на активний процес
if [ -f "$BOT_PID_FILE" ]; then
  EXISTING_PID=$(cat "$BOT_PID_FILE")
  if ps -p "$EXISTING_PID" > /dev/null 2>&1; then
    echo "🚫 Бот вже запущений із PID $EXISTING_PID. Зупинено запуск."
    $ALERT_SCRIPT "<b>🚫 Захист GPT:</b> бот вже запущений з PID <code>$EXISTING_PID</code>. Повторний запуск заборонено."
    exit 1
  else
    echo "⚠️ Старий PID знайдено, але процесу немає. Видаляємо PID файл..."
    rm -f "$BOT_PID_FILE"
  fi
fi

echo "🔁 Перехід у директорію GPT_monitoring..."
cd /root/GPT_monitoring || exit 1

echo "🛑 Зупинка старого процесу (якщо запущений)..."
pkill -f main.py

echo "🚀 Запуск нового процесу..."
nohup python3 main.py > bot.log 2>&1 &

# 🔐 Збереження нового PID
echo $! > "$BOT_PID_FILE"

# 🧾 Показ журналу
sleep 2
echo "📋 Бот запущено. Останні рядки з журналу:"
tail -n 5 bot.log
