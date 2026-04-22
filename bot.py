import discord
from discord.ext import commands, tasks
import random
import os
import requests
from datetime import datetime

# Bot setup
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
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
        description=f"**{
