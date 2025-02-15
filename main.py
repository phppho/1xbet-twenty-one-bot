import os
import openai
import deepseek
from flask import Flask, request
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Dispatcher
import logging

TOKEN = "8012337385:AAEYzT0bhdV2TRCHsLqO4gB4k2_Ze-_yTas"
OPENAI_API_KEY = "svcacct-rVJuHoBu5IUtdvv1hIebC6uWn0EDWxMXetKWL_PiGCKCwjR6BnQpMM1xdfTsO9bT3BlbkFJadJbK2kiWEMkLj3T-wA7UTTlMJ0ezFN3uu6wFdjAzhyzDz9osrREx9tznYjOXAA"
DEEPSEEK_API_KEY = "sk-1afd336e74d240a1ae23fe7ddbc2fa95
"

openai.api_key = OPENAI_API_KEY
deepseek.api_key = DEEPSEEK_API_KEY

app = Flask(__name__)

def chat_with_gpt(prompt):
    """يتعامل مع API الخاصة بـ OpenAI"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def chat_with_deepseek(prompt):
    """يتعامل مع API الخاصة بـ DeepSeek"""
    response = deepseek.Completion.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحبًا! أرسل لي أي سؤال وسأجيب باستخدام الذكاء الاصطناعي.")

def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text
    response = chat_with_gpt(user_input)  # يمكنك استبدالها بـ chat_with_deepseek(user_input)
    update.message.reply_text(response)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """يتعامل مع طلبات تيليجرام"""
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"

if __name__ == "__main__":
    from telegram import Bot
    from telegram.ext import Updater

    bot = Bot(TOKEN)
    dp = Dispatcher(bot, None, workers=0)
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))    