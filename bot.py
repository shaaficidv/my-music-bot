import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from yt_dlp import YoutubeDL

# --- XOGTAADA ---
API_ID = 36986727
API_HASH = "77510f5c8c8b92a41acd17188595b484"
SESSION = "BAI0X2cAGBHSaplNfNaalwuXE7OjUQlfDKA2qUpogBLwwHe4jjGFYm6dsgIjCAdKI2-4Ucfwdi8Gom1_JjfUpDypOilWx_cp2Ky7anTCuf1iLm2ku6vXwvd6FSa4rw_6FA8ZvRqgGiF5VHdEvXr-GMvTLuZXeAAiKTfFbgz8Dqcny5163u64CGkHklkZtdbd4oW6dc8yGNd1GtxUkxNCGi-tpk9oBn19fanO2z2PtWPv6TGMHhmcqHYI1IcmeXwVaIa0Ep_CvGQU5GzZwYiCKskRcMeiG1J-0FH5_7hzS-ZI4jvR2WwVt5MSTJTF2mjGoS0oBykjllQ5GfeAEUtG4XYZmA5DAgAAAAHmy7A"
BOT_TOKEN = "8524748895:AAEBw7opAvIB-PMGaVdjZ-0u1XTbFjAO8DU"

app = Client("user_acc", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
bot = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@bot.on_message(filters.command("play") & filters.group)
async def play_audio(client, message):
    if len(message.command) < 2: return await message.reply("❌ Qor magaca heesta!")
    query = " ".join(message.command[1:])
    m = await message.reply(f"🔎 Raadinayaa: **{query}**...")
    try:
        with YoutubeDL({'format': 'bestaudio/best', 'quiet': True}) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['url']
        await call_py.play(message.chat.id, MediaStream(url))
        await m.edit(f"🎶 **Hadda waxaa socota:**\n└ {info['title']}")
    except Exception as e: await m.edit(f"❌ Khalad: {e}")

@bot.on_message(filters.command("stop") & filters.group)
async def stop_audio(client, message):
    try:
        await call_py.leave_call(message.chat.id)
        await message.reply("⏹ Waa la joojiyay.")
    except: pass

async def main():
    await app.start()
    await bot.start()
    await call_py.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
    
