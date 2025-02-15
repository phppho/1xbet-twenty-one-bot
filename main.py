import os
import openai
import deepseek
from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import logging

# تحميل مفاتيح API من المتغيرات البيئية
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

openai.api_key = OPENAI_API_KEY
deepseek.api_key = DEEPSEEK_API_KEY

app = Flask(__name__)

# تهيئة Telegram Bot
from telegram import Bot
bot = Bot(TOKEN)
dp = Dispatcher(bot, None, workers=0)

# وظائف الذكاء الاصطناعي
def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def chat_with_deepseek(prompt):
    response = deepseek.Completion.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# أوامر البوت
def start(update: Update, context):
    update.message.reply_text("مرحبًا! أرسل لي أي سؤال وسأجيب باستخدام الذكاء الاصطناعي.")

def handle_message(update: Update, context):
    user_input = update.message.text
    response = chat_with_gpt(user_input)  # استخدم chat_with_deepseek() إذا أردت
    update.message.reply_text(response)

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """معالجة طلبات تيليجرام"""
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))