import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
from datetime import datetime
from discord.ext import tasks

# เพิ่ม import สำหรับ Flask และ threading
from flask import Flask
from threading import Thread

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True  # เพิ่มนี้เพื่อใช้ on_voice_state_update

bot = commands.Bot(command_prefix='!', intents=intents)

user_join_status = {}

def create_daily_game_embed(user: discord.Member) -> discord.Embed:
    embed = discord.Embed(
        title="🎮 Daily Activity Reminder",
        description=f"สวัสดี {user.mention}!\nอย่าลืมทำกิจกรรมประจำวันในเกมต่อไปนี้นะครับ:",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )
    
    # Wuthering Wave Section
    embed.add_field(
        name="🌬️ Wuthering Wave",
        value=(
            "- เควสประจำวัน: ทำให้ครบ\n"
            "- ลงดันเจี้ยน Daily Dungeon\n"
            "- เก็บวัตถุดิบสำคัญ\n"
            "- เช็คกิจกรรมเวลาจำกัด"
        ),
        inline=False
    )
    
    # LOL Section
    embed.add_field(
        name="⚔️ League of Legends",
        value=(
            "- เล่นโหมด ARAM หรือ Ranked\n"
            "- เคลียร์ภารกิจรายวัน\n"
            "- ฝึกซ้อมการเล่นแชมเปี้ยนใหม่\n"
            "- ตรวจสอบรางวัลและกิจกรรม"
        ),
        inline=False
    )
    
    # รูปเกม (ใส่ URL รูปจริงที่ต้องการ)
    embed.set_image(url="https://gamicsoft.sgp1.digitaloceanspaces.com/28581/conversions/QQ%E6%88%AA%E5%9B%BE20230415192317-big_thumb.jpg")
    
    embed.set_footer(text="อย่าลืมสนุกและพักผ่อนด้วยนะครับ 😊")
    embed.set_thumbnail(url=user.avatar.url if user.avatar else "")
    
    return embed

@bot.event
async def on_voice_state_update(user: discord.Member, before, after):
    if before.channel is None and after.channel is not None:
        user_id = user.id
        
        if user_id not in user_join_status:
            user_join_status[user_id] = True
            await user.send(embed=create_daily_game_embed(user))

@tasks.loop(hours=24)
async def reset_join_status():
    user_join_status.clear()
    print(f"[{datetime.utcnow()}] ล้าง user_join_status เรียบร้อยแล้ว")
            
@bot.event
async def on_ready():
    print(f"Bot is ready: {bot.user.name}")

# --- โค้ด Flask เว็บเซิร์ฟเวอร์เล็กๆ เพื่อ uptime ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# เรียกก่อน bot.run()
keep_alive()

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
