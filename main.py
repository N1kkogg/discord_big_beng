import interactions
from interactions.api.voice.audio import AudioVolume
import asyncio
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")
SOUND_PATH = os.getenv("SOUND_PATH")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = interactions.Client()

@interactions.listen()
async def on_startup():
    print("Bot is ready!")
    asyncio.create_task(execute_on_the_hour())  # Schedule the periodic task within the bot's event loop
    await bot.change_presence(interactions.Status.ONLINE, interactions.Activity("DENGG", interactions.ActivityType.LISTENING))

@interactions.slash_command("play")
async def play(ctx:interactions.SlashContext):
    await ctx.send("playing sound now...", ephemeral=True)
    await play_dong(ctx.author.voice.channel)

async def play_dong(channel):
    voice_state = await channel.connect()
    audio = AudioVolume(SOUND_PATH)
    await voice_state.play(audio)
    await channel.disconnect()

async def execute_on_the_hour():
    while True:
        now = datetime.now()
        next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        time_to_wait = (next_hour - now).total_seconds()
        print(f"Waiting {time_to_wait} seconds until the next hour...")
        await asyncio.sleep(time_to_wait)
        await play_dong(bot.get_channel(CHANNEL_ID))
        print("Executing function at", next_hour.strftime("%Y-%m-%d %H:%M:%S"))

bot.start(TOKEN)
