#!/bin/bash

cd /root/telegram-bot || exit 1

echo "🔴 Зупиняю старого бота (якщо запущено)..."
pkill -f "python3 main.py"

echo "🚀 Запускаю нового бота у фоновому режимі..."
nohup python3 main.py > nohup.out 2>&1 &

sleep 1

echo "✅ Бот запущено. Останні рядки журналу:"
tail -n 20 nohup.out
