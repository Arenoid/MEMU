import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
import asyncio

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print("Token:", TOKEN)  # Add this line in main.py right after loading the .env file



# Initialize the bot with intents and command prefix
client = commands.Bot(command_prefix="m!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    await client.change_presence(activity=discord.Game("m!info"))

@client.command()
async def ping(ctx):
    """Ping command to measure response time"""
    start_time = time.time()
    
    # Create initial embed message for pong
    embed = discord.Embed(title="Pong! 🏓", color=0x9900FF)
    initial_message = await ctx.send(embed=embed)
    
    # Calculate response time and update embed
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    embed.add_field(name="Response Time", value=f"{response_time:.2f} ms")
    await initial_message.edit(embed=embed)

async def load_cogs():
    """Dynamically loads cogs from specified directories"""
    cogs = [
        'fun.eight_ball_cog', 'sfw.waifu_cog', 'fun.weather_cog', 'fun.meme_cog',
        'nsfw.hentai_cog', 'info.info_cog', 'sfw.neko_cog', 'nsfw.blowjob_cog',
        'nsfw.trap_cog', 'sfw.yeet_cog', 'info.anime_cog', 'moderation.ban_cog',
        'moderation.kick_cog', 'moderation.mute_cog', 'fun.randomvid_cog',
        'nsfw.ass_cog', 'nsfw.boobs_cog', 'sfw.bonk_cog', 'sfw.bully_cog',
        'sfw.kill_cog', 'sfw.poke_cog', 'fun.trivia_cog', 'moderation.warn_cog',
        'moderation.purge_cog', 'nsfw.mif_cog', 'fun.joke_cog', 'info.userinfo_cog',
        'nsfw.r34_cog', 'maths.graph_cog'
    ]

    for cog in cogs:
        try:
            await client.load_extension(cog)
            print(f"Loaded extension: {cog}")
        except Exception as e:
            print(f"Failed to load extension {cog}: {e}")

async def main():
    """Main function to run the bot"""
    async with client:
        await load_cogs()
        await client.start(TOKEN)

# Run the bot
if __name__ == '__main__':
    asyncio.run(main())
