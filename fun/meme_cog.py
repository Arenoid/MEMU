import discord
from discord.ext import commands
import requests
import random

class MemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='meme')
    async def get_meme(self, ctx):
        """Fetch a random meme and send it in an embedded message."""
        meme_data = self.fetch_random_meme()
        
        if meme_data:
        
            embed = discord.Embed(
                title=meme_data['title'],
                color=discord.Color.random()
            )
            embed.set_image(url=meme_data['url'])
            embed.set_footer(text="Source: Meme API")

            await ctx.send(embed=embed)
        else:
            await ctx.send("Sorry, I couldn't fetch a meme at the moment.")

    def fetch_random_meme(self):
        """Fetch a random meme from the meme API."""
        url = "https://meme-api.com/gimme"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return {
                'title': data['title'],
                'url': data['url']
            }
        else:
            return None

async def setup(bot):
    await bot.add_cog(MemeCog(bot))
