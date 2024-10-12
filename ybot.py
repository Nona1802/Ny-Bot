my_token = '7941600017:AAFS2UHRVItCeAX5J36UqbZDy09CNDX54eo'

import yt_dlp
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

def download_youtube_video(youtube_url, output_dir="downloads"):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            audio_file = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        
        return audio_file

    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Please send me the YouTube link of the song you want to download.")

async def download_song_from_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    youtube_url = update.message.text

    await update.message.reply_text(f"Downloading song from the provided link: {youtube_url}...")

    downloaded_file = download_youtube_video(youtube_url)
    
    if downloaded_file:
        song_title = os.path.splitext(os.path.basename(downloaded_file))[0]  

        with open(downloaded_file, 'rb') as f:
            await update.message.reply_audio(audio=f, title=song_title)  

        os.remove(downloaded_file)

        await update.message.reply_text("Download complete! You can send another YouTube link if you'd like.")

    else:
        await update.message.reply_text("Failed to download the song. Please try again later.")

if __name__ == '__main__':
    app = Application.builder().token(my_token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_song_from_link))  

    print('Bot started...')
    app.run_polling()
