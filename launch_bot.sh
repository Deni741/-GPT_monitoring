#!/bin/bash

echo "📁 Перехід у директорію GPT_monitoring..."
cd /root/GPT_monitoring || {
  echo "❌ Помилка: директорія GPT_monitoring не знайдена."
  exit 1
}

echo "🛑 Зупинка старого процесу (якщо запущений)..."
pkill -f "python3 main.py"

echo "🚀 Запуск нового процесу..."
nohup python3 main.py > nohup.out 2>&1 &

sleep 1
echo "📋 Бот запущено. Останні рядки з журналу:"
tail -n 20 nohup.out
