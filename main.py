import discord
from discord.ext import commands
import requests
import json

# Constants
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
GITHUB_BASE_URL = 'https://raw.githubusercontent.com/switch-preserve/preserve-db/main/games/'
ICONS_BASE_URL = 'https://raw.githubusercontent.com/switch-preserve/preserve-db/main/icons/'
DOWNLOAD_LINK = 'https://github.com/switch-preserve/preserve-db'  # Temporary link
SPECIAL_ROLE_NAME = 'Special'

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot Setup
bot = commands.Bot(command_prefix='/tnsp ', intents=intents)

# Helper to check if user has Special role
def has_special_role(ctx):
    return any(role.name == SPECIAL_ROLE_NAME for role in ctx.author.roles)

# Download command
@bot.command(name='download')
async def download(ctx, preserve_id: str, content_type: str = None):
    if not has_special_role(ctx):
        await ctx.send("You don't have permission to use this command.")
        return

    preserve_id = preserve_id.upper()
    url = f"{GITHUB_BASE_URL}{preserve_id}.json"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            await ctx.send("Game not found in the database.")
            return

        game_data = response.json()
        embed = discord.Embed(title=game_data['title'], description=game_data['description'], color=0x00cc66)
        embed.set_thumbnail(url=f"{ICONS_BASE_URL}{preserve_id}.png")
        embed.add_field(name="Preserve ID", value=preserve_id, inline=True)
        embed.add_field(name="Title ID", value=game_data['titleID'], inline=True)

        if content_type == 'dlc' and game_data.get('dlc'):
            embed.add_field(name="DLC", value='\n'.join(game_data['dlc']), inline=False)
        elif content_type == 'update' and game_data.get('update'):
            embed.add_field(name="Update Version", value=game_data['update']['version'], inline=False)

        if game_data.get('screenshot'):
            embed.set_image(url=game_data['screenshot'])

        embed.add_field(name=" ", value=f"[Download Content]({DOWNLOAD_LINK})", inline=False)

        await ctx.author.send(embed=embed)
        await ctx.send("Check your DMs!")

    except Exception as e:
        print(f"Error: {e}")
        await ctx.send("Something went wrong trying to get that game.")

# Run the bot
bot.run(TOKEN)
