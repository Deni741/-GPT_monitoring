from telegram.ext import ApplicationBuilder
from part2_handlers import add_handlers
import os

with open("bot_token.txt", "r") as f:
    TOKEN = f.read().strip()

application = ApplicationBuilder().token(TOKEN).build()
add_handlers(application)