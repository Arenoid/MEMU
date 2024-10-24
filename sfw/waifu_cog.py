import discord
from discord.ext import commands
import requests

class WaifuImages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='waifu')
    async def get_waifu_image(self, ctx):
        
        try:
            response = requests.get('https://api.waifu.pics/sfw/waifu')
            data = response.json()
            image_url = data['url']

            embed = discord.Embed(title="Here's a waifu for you!")
            embed.set_image(url=image_url)
            await ctx.send(embed=embed)
        except Exception as e:
            print(f"Error fetching image: {e}")
            await ctx.send("Couldn't fetch a waifu image right now. Please try again later.")


async def setup(bot):
    await bot.add_cog(WaifuImages(bot))
