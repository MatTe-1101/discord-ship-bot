"""
Discord Love Ship Bot ❤️ (versione avanzata)
Descrizione: un bot Discord scritto in Python (discord.py v2+) che genera "ship" amorose tra utenti con più funzioni.
Funzionalità:
 - !ship @utente1 @utente2 → genera compatibilità, descrizione, cuori e nome ship
 - /ship → versione slash del comando
 - Generazione nomi ship (mix dei nomi utente)
 - Immagini romantiche casuali o meme divertenti
 - Classifica delle coppie migliori (!leaderboard)
 - Memorizzazione temporanea delle coppie con punteggio

Istruzioni:
 1) pip install -U discord.py requests
 2) imposta il token in una variabile d'ambiente DISCORD_TOKEN
 3) python love_ship_bot.py

"""

import os
import random
import logging
import discord
import requests
from discord.ext import commands
from discord import app_commands

# ------------------------- Config & logging -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('love_ship_bot')

TOKEN = "MY_TOKEN"
PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
tree = bot.tree

# ------------------------- Dati e helper -------------------------

leaderboard = {}  # dict {"utente1_utente2": score}

romantic_images = [
    "https://i.imgur.com/v5f0VQd.jpg",
    "https://i.imgur.com/Lc0Tx3Y.jpg",
    "https://i.imgur.com/BH9s4j3.jpg",
    "https://i.imgur.com/XFcePqG.jpg",
    "https://i.imgur.com/FZpt8Lb.jpg"
]

love_memes = [
    "https://i.imgur.com/qYVTo7x.jpg",
    "https://i.imgur.com/2QjvZwh.jpg",
    "https://i.imgur.com/CPf7aMZ.jpg"
]

def generate_ship_score():
    return random.randint(0, 100)

def get_love_description(score: int) -> str:
    if score < 20:
        return "💔 Forse è meglio restare amici..."
    elif score < 40:
        return "😅 C'è un po' di feeling, ma serve tempo!"
    elif score < 60:
        return "💞 Qualcosa bolle in pentola!"
    elif score < 80:
        return "❤️ Ottima sintonia! Potrebbe funzionare davvero!"
    else:
        return "💖 Anime gemelle trovate! È vero amore!"

def generate_ship_name(user1: str, user2: str) -> str:
    u1 = user1[:len(user1)//2]
    u2 = user2[len(user2)//2:]
    return (u1 + u2).capitalize()

def random_love_image():
    if random.random() < 0.7:
        return random.choice(romantic_images)
    return random.choice(love_memes)

# ------------------------- Eventi -------------------------

@bot.event
async def on_ready():
    logger.info(f"Connesso come {bot.user} (ID: {bot.user.id})")
    try:
        synced = await tree.sync()
        logger.info(f"Slash commands sincronizzati: {len(synced)}")
    except Exception as e:
        logger.warning(f"Errore sync tree: {e}")

# ------------------------- Comando testuale principale -------------------------

@bot.command(name='ship')
async def ship(ctx: commands.Context, user1: discord.Member = None, user2: discord.Member = None):
    """Crea una ship amorosa tra due utenti."""
    if not user1 or not user2:
        await ctx.send("Usa: !ship @utente1 @utente2 ❤️")
        return

    score = generate_ship_score()
    description = get_love_description(score)
    hearts = '❤️' * (score // 20) or '💔'
    ship_name = generate_ship_name(user1.display_name, user2.display_name)
    image_url = random_love_image()

    key = f"{user1.id}_{user2.id}"
    leaderboard[key] = max(score, leaderboard.get(key, 0))

    embed = discord.Embed(
        title=f"💘 Love Ship: {ship_name}",
        description=f"{user1.mention} 💞 {user2.mention}",
        color=random.choice([discord.Color.red(), discord.Color.pink(), discord.Color.magenta()])
    )
    embed.add_field(name="Compatibilità", value=f"**{score}%** {hearts}", inline=False)
    embed.add_field(name="Descrizione", value=description, inline=False)
    embed.set_image(url=image_url)
    embed.set_footer(text="Generato con amore ❤️")

    await ctx.send(embed=embed)

# ------------------------- Slash command -------------------------

@tree.command(name="ship", description="Crea una ship amorosa tra due utenti ❤️")
@app_commands.describe(user1="Primo utente", user2="Secondo utente")
async def slash_ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    score = generate_ship_score()
    description = get_love_description(score)
    hearts = '❤️' * (score // 20) or '💔'
    ship_name = generate_ship_name(user1.display_name, user2.display_name)
    image_url = random_love_image()

    key = f"{user1.id}_{user2.id}"
    leaderboard[key] = max(score, leaderboard.get(key, 0))

    embed = discord.Embed(
        title=f"💘 Love Ship: {ship_name}",
        description=f"{user1.mention} 💞 {user2.mention}",
        color=random.choice([discord.Color.red(), discord.Color.pink(), discord.Color.magenta()])
    )
    embed.add_field(name="Compatibilità", value=f"**{score}%** {hearts}", inline=False)
    embed.add_field(name="Descrizione", value=description, inline=False)
    embed.set_image(url=image_url)
    embed.set_footer(text="Generato con amore ❤️")

    await interaction.response.send_message(embed=embed)

# ------------------------- Leaderboard -------------------------

@bot.command(name='leaderboard')
async def leaderboard_cmd(ctx: commands.Context):
    if not leaderboard:
        await ctx.send("Nessuna ship ancora registrata 💔")
        return

    sorted_pairs = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:10]
    desc = "\n".join([f"{i+1}. <@{pair.split('_')[0]}> 💞 <@{pair.split('_')[1]}> — **{score}%**" for i, (pair, score) in enumerate(sorted_pairs)])

    embed = discord.Embed(title="🏆 Classifica delle Ship", description=desc, color=discord.Color.gold())
    await ctx.send(embed=embed)

# ------------------------- Avvio -------------------------

if __name__ == '__main__':
    if not TOKEN:
        logger.warning("Variabile DISCORD_TOKEN non trovata. Inserisci il token come DISCORD_TOKEN.")
    bot.run(TOKEN)
