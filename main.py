import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to the Video Compressor Bot!\n📩 Just send me a video and I'll compress it!")

async def compress_video(file_path, output_path, crf=28):
    cmd = ['ffmpeg', '-i', file_path, '-vcodec', 'libx264', '-crf', str(crf), output_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    file = await video.get_file()

    await update.message.reply_text("⏬ Downloading your video...")

    input_path = "input.mp4"
    output_path = "output.mp4"

    await file.download_to_drive(input_path)

    await update.message.reply_text("⚙️ Compressing... Please wait.")
    await compress_video(input_path, output_path)

    await update.message.reply_video(video=open(output_path, 'rb'), caption="✅ Compressed Video!")

    os.remove(input_path)
    os.remove(output_path)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO, handle_video))

app.run_polling()
