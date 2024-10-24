import discord
from discord.ext import commands
import requests

class BonkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_gif(self):
        url = 'https://api.waifu.pics/sfw/bonk'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['url']
        return None

    @commands.command(name='bonk')
    async def bonk(self, ctx, member: discord.Member):
        gif_url = await self.fetch_gif()
        if gif_url:
            await ctx.send(f"{ctx.author.mention} bonked {member.mention}\n{gif_url}")
        else:
            await ctx.send("Could not fetch a bonk GIF.")

async def setup(bot):
    await bot.add_cog(BonkCog(bot))
