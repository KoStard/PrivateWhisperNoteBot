import os
import uuid

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import dotenv
import logging
from openai import OpenAI
import io
from pydub import AudioSegment

import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

dotenv.load_dotenv()
client = OpenAI()

ALLOWED_USERS = json.loads(os.getenv("ALLOWED_USERS"))


async def authenticate(update: Update):
    if update.effective_user.id not in ALLOWED_USERS:
        await update.effective_message.reply_text("You are not allowed to use this bot.")
        raise Exception(
            f"User {update.effective_user.username} with id {update.effective_user.id} tried to use the bot.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await authenticate(update)
    print(update.effective_user.id)
    await update.message.reply_text(f'Hello {update.effective_user.first_name}, please send your audio messages here '
                                    f'to transcribe')


async def transcribe_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await authenticate(update)
    file = await update.message.voice.get_file()
    await _handle_audio_file(update, file)


async def transcribe_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await authenticate(update)
    file = await update.message.audio.get_file()
    await _handle_audio_file(update, file)


async def _handle_audio_file(update, file):
    file_format = file.file_path.split(".")[-1]
    path = await file.download_to_drive(f"/tmp/{uuid.uuid4()}.{file_format}")
    wav_io = io.BytesIO()
    AudioSegment.from_file(open(path, 'rb'), type=file_format).export(wav_io, format="wav")
    wav_io.seek(0)
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=("test.wav", wav_io.read())
    )
    await update.effective_message.reply_text(transcript.text)

async def text_message_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await authenticate(update)
    await update.message.reply_text("Please send audio messages to transcribe")


app = ApplicationBuilder().token(os.environ['TELEGRAM_BOT_API_KEY']).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VOICE, transcribe_voice))
app.add_handler(MessageHandler(filters.AUDIO, transcribe_audio))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_received))
app.run_polling()
