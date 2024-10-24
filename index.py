import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


client = commands.Bot(command_prefix="m!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"Logged in as {client.user}!")
    await client.change_presence(activity=discord.Game(f"m!info"))


@client.command()
async def ping(ctx):
    start_time = time.time()
    

    embed = discord.Embed(title="Pong! 🏓", color=0x9900FF) 
    initial_message = await ctx.send(embed=embed)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000
    embed.add_field(name="Response Time", value=f"{response_time:.2f} ms")
    await initial_message.edit(embed=embed)




async def load_cogs():
    await client.load_extension('fun.eight_ball_cog')
    await client.load_extension('sfw.waifu_cog')
    await client.load_extension('fun.weather_cog')
    await client.load_extension('fun.meme_cog')
    await client.load_extension('nsfw.hentai_cog')
    await client.load_extension('info.info_cog')
    await client.load_extension('sfw.neko_cog')
    await client.load_extension('nsfw.blowjob_cog')
    await client.load_extension('nsfw.trap_cog')
    await client.load_extension('sfw.yeet_cog')
    await client.load_extension('info.anime_cog')
    await client.load_extension('moderation.ban_cog')
    await client.load_extension('moderation.kick_cog')
    await client.load_extension('moderation.mute_cog')
    await client.load_extension('fun.randomvid_cog')
    await client.load_extension('nsfw.ass_cog')
    await client.load_extension('nsfw.boobs_cog')
    await client.load_extension('sfw.bonk_cog')
    await client.load_extension('sfw.bully_cog')
    await client.load_extension('sfw.kill_cog')
    await client.load_extension('sfw.poke_cog')
    await client.load_extension('fun.trivia_cog')
    await client.load_extension('moderation.warn_cog')
    await client.load_extension('moderation.purge_cog')
    await client.load_extension('nsfw.mif_cog')
    await client.load_extension('fun.joke_cog')

    



async def main():
    async with client:
        await load_cogs()
        await client.start(TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
