import discord
from discord.ext import commands, tasks
import random
import os
from datetime import datetime

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Your Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1487798305189662840/OAaDjhmK4YlCJNR_9KbV8dJ5KFEakLk0sE5wMTPW3MrOZ04FTdmCJytEc3qAOyZSvHz8"

# Brainrot data (OG & Drag)
BRAINROTS = {
    "Strawberry Elephant": {"base": 750, "interval": 7200, "last": 0, "color": 0xFF69B4},
    "Meowl": {"base": 650, "interval": 5400, "last": 0, "color": 0xFFA500},
    "Skibidi Toilet": {"base": 450, "interval": 2700, "last": 0, "color": 0x808080},
    "Headless Horseman": {"base": 550, "interval": 14400, "last": 0, "color": 0x800080},
    "Dragon Cannelloni": {"base": 250, "interval": 900, "last": 0, "color": 0xFF0000}
}

# Extra brainrots (base to 3B)
EXTRA_BRAINROTS = [
    {"name": "Frograma & Chocrama", "base": 100, "maxCap": 3000},
    {"name": "Capitano Moby", "base": 165, "maxCap": 3000},
    {"name": "Hydra Bunny", "base": 185, "maxCap": 3000}
]

# Real mutations from wiki
MUTATIONS = {
    "Cyber": 11.0,
    "Divine": 10.0,
    "Rainbow": 10.0,
    "Cursed": 9.0,
    "Radioactive": 8.5,
    "Yin Yang": 7.5,
    "Galaxy": 7.0,
    "Lava": 6.0,
    "Candy": 4.0,
    "Diamond": 1.5,
    "Gold": 1.25,
    "Normal": 1.0
}

# Real traits from wiki
TRAITS = {
    "Strawberry": 8.0,
    "Meowl": 7.0,
    "Skibidi": 6.5,
    "Nyan Cat": 6.0,
    "Firework": 6.0,
    "Brazil": 6.0,
    "Lightning": 6.0,
    "Chicleteira": 6.0,
    "Tie": 4.75,
    "Spider": 4.5,
    "Asteroid": 4.0,
    "Galactic": 4.0,
    "Crab Rave": 4.0,
    "Bubblegum": 4.0,
    "Extinct": 4.0,
    "Matteo Hat": 4.0,
    "Bombardiro": 3.0,
    "Starfall": 3.5,
    "Shark": 3.0,
    "UFO": 3.0,
    "Snow": 3.0,
    "Taco": 3.0,
    "Rain": 2.5
}

def calculate_price(base_value, mutation, trait):
    mutation_mult = MUTATIONS.get(mutation, 1.0)
    trait_mult = TRAITS.get(trait, 1.0)
    
    variance = 0.8 + (random.random() * 0.4)
    final_value = base_value * mutation_mult * trait_mult * variance
    
    max_cap = 15000 if base_value >= 200 else 3000
    final_value = max(base_value, min(max_cap, final_value))
    
    return final_value

def format_price(millions):
    if millions >= 1000:
        return f"${millions/1000:.2f}B"
    return f"${millions:.0f}M"

def get_random_mutation():
    mutations_list = ["Normal"] * 50 + ["Gold"] * 20 + ["Diamond"] * 10 + ["Candy", "Lava"] * 8 + ["Galaxy", "Yin Yang", "Radioactive"] * 6 + ["Rainbow", "Divine", "Cursed", "Cyber"] * 2
    return random.choice(mutations_list)

def get_random_trait():
    if random.random() < 0.3:
        return random.choice(list(TRAITS.keys()))
    return None

async def send_webhook_embed(name, price, mutation, trait, players, maxpl, job_id):
    price_formatted = format_price(price)
    
    if price >= 10000:
        color = 0xFF0000
    elif price >= 5000:
        color = 0xFF6600
    elif price >= 2000:
        color = 0xFFFF00
    else:
        color = 0x00FF00
    
    embed = discord.Embed(
        title="🎯 NEW BRAINROT DETECTED",
        description=f"**{name}** has been detected!",
        color=color,
        timestamp=datetime.now()
    )
    
    embed.add_field(name="💰 Estimated Value", value=price_formatted, inline=True)
    embed.add_field(name="🧬 Mutation", value=mutation, inline=True)
    if trait:
        embed.add_field(name="✨ Trait", value=trait, inline=True)
    embed.add_field(name="👥 Players", value=f"{players}/{maxpl}", inline=True)
    if job_id:
        embed.add_field(name="🔗 Job ID", value=f"`{job_id[:12]}...`", inline=False)
    
    embed.set_footer(text="GrimHub AJ • 24/7 Detection")
    
    webhook = discord.SyncWebhook.from_url(WEBHOOK_URL)
    webhook.send(embed=embed)

@tasks.loop(seconds=30)
async def check_schedules():
    now = datetime.now().timestamp()
    
    for name, data in BRAINROTS.items():
        if now - data["last"] >= data["interval"]:
            mutation = get_random_mutation()
            trait = get_random_trait()
            price = calculate_price(data["base"], mutation, trait)
            players = random.randint(1, 8)
            job_id = f"grimhub_{int(now)}_{random.randint(1000,9999)}"
            
            await send_webhook_embed(name, price, mutation, trait, players, 8, job_id)
            BRAINROTS[name]["last"] = now
            print(f"Sent: {name} at {datetime.now()}")
    
    if random.random() < 0.3:
        extra = random.choice(EXTRA_BRAINROTS)
        mutation = get_random_mutation()
        trait = get_random_trait()
        price = calculate_price(extra["base"], mutation, trait)
        players = random.randint(1, 8)
        job_id = f"extra_{int(now)}_{random.randint(1000,9999)}"
        
        await send_webhook_embed(extra["name"], price, mutation, trait, players, 8, job_id)
        print(f"Sent extra: {extra['name']} at {datetime.now()}")

@bot.event
async def on_ready():
    print(f"✅ GrimHub AJ Bot is online!")
    print(f"Logged in as {bot.user}")
    print(f"Started at {datetime.now()}")
    check_schedules.start()

@bot.command()
async def status(ctx):
    await ctx.send("✅ GrimHub AJ Bot is running 24/7!")

@bot.command()
async def test(ctx):
    await send_webhook_embed("Test Brainrot", 500, "Rainbow", "Divine", 4, 8, "test_123")
    await ctx.send("Test sent!")

@bot.command()
async def next(ctx):
    now = datetime.now().timestamp()
    msg = "**Next Scheduled Brainrots:**\n"
    for name, data in BRAINROTS.items():
        remaining = data["interval"] - (now - data["last"])
        if remaining > 0:
            minutes = int(remaining // 60)
            seconds = int(remaining % 60)
            msg += f"• {name}: {minutes}m {seconds}s\n"
        else:
            msg += f"• {name}: **NOW!**\n"
    await ctx.send(msg)

# ============================================
# REPLACE THIS WITH YOUR ACTUAL TOKEN
# ============================================
TOKEN = "MTQ5NjQ2NDM4ODI4OTQ2NjQ2OQ.GmI63x.a7mliJZTHOMqMNpCffw0EZCP5MLKW50IUfBB2w"

bot.run(TOKEN)
