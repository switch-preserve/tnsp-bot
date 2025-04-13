import discord
from discord.ext import commands
import requests
import os

# Get the bot token from environment variables
TOKEN = os.getenv("TOKEN")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Bot prefix and setup
bot = commands.Bot(command_prefix="/tnsp ", intents=intents)

# Role name that has permission
REQUIRED_ROLE_NAME = "Special"

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

# Helper: Check if user has Special role
def has_special_role(ctx):
    return any(role.name == REQUIRED_ROLE_NAME for role in ctx.author.roles)

# Command: /tnsp download [PreserveID] [optional: dlc or update]
@bot.command(name="download")
async def download(ctx, preserve_id: str, content_type: str = None):
    if not has_special_role(ctx):
        await ctx.send("🚫 You don’t have permission to use this command.")
        return

    # Fetch game JSON from GitHub
    url = f"https://raw.githubusercontent.com/switch-preserve/preserve-db/main/games/{preserve_id.upper()}.json"
    response = requests.get(url)

    if response.status_code != 200:
        await ctx.send("❌ Game not found.")
        return

    game_data = response.json()

    # Compose Embed
    embed = discord.Embed(
        title=game_data.get("title", "Unknown Title"),
        description=game_data.get("description", "No description provided."),
        color=0x2ecc71
    )
    embed.add_field(name="Preserve ID", value=preserve_id.upper(), inline=True)
    embed.add_field(name="Title ID", value=game_data.get("title_id", "Unknown"), inline=True)

    # Attach image
    image_url = f"https://raw.githubusercontent.com/switch-preserve/preserve-db/main/icons/{preserve_id.upper()}.png"
    embed.set_thumbnail(url=image_url)

    # Attach screenshot if available
    screenshot_url = game_data.get("screenshot")
    if screenshot_url:
        embed.set_image(url=screenshot_url)

    # Add download link (temporary placeholder)
    embed.add_field(name="Download", value="[Download Content](https://github.com/switch-preserve/preserve-db)", inline=False)

    try:
        await ctx.author.send(embed=embed)
        await ctx.send("✅ Sent you the game info in DMs!")
    except discord.Forbidden:
        await ctx.send("❌ I couldn't DM you. Please allow DMs from server members.")

bot.run(TOKEN)
