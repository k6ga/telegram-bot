import asyncio, aiohttp, os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("TOKEN")

async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as r:
            return r.status
    except:
        return None

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = update.message.text.split("\n")
    msg = await update.message.reply_text("⏳...")

    async with aiohttp.ClientSession() as session:
        result = ""
        for u in users:
            ig = await fetch(session, f"https://instagram.com/{u}") == 404
            tt = await fetch(session, f"https://tiktok.com/@{u}") == 404
            result += f"{u} IG:{'✅' if ig else '❌'} TT:{'✅' if tt else '❌'}\n"

    await msg.edit_text(result)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, check))
app.run_polling()
