#!/bin/bash

DUPLICATES=$(ls /root | grep -E 'GPT_monitoring(_old|hold|copy|backup|v2)')

if [ ! -z "$DUPLICATES" ]; then
    echo "❌ Виявлено дублікат директорії: $DUPLICATES"
    echo "$(date '+%Y-%m-%d %H:%M:%S') - DUPLICATE FOLDER DETECTED: $DUPLICATES" >> /root/GPT_monitoring/security.log
    /root/GPT_monitoring/alert_to_telegram.sh "⚠️ <b>Захист GPT:</b> виявлено дублікат <code>$DUPLICATES</code> на сервері. Бот НЕ запущено. Перевір вручну."
    exit 1
fi
