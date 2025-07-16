#!/bin/bash

CHAT_ID="313868501"
BOT_TOKEN="8108237988:AAEa3aj8WOuLMwk11DPmRc_eqFt-WKP1NY8"

MESSAGE="$1"

curl -s -X POST https://api.telegram.org/bot$BOT_TOKEN/sendMessage \
     -d chat_id="$CHAT_ID" \
     -d parse_mode="HTML" \
     -d text="$MESSAGE"
