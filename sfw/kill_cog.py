import discord
from discord.ext import commands
import requests

class KillCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_gif(self):
        url = 'https://api.waifu.pics/sfw/kill'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data['url']
        return None

    @commands.command(name='kill')
    async def kill(self, ctx, member: discord.Member):
        gif_url = await self.fetch_gif()
        if gif_url:
            await ctx.send(f"{ctx.author.mention} killed {member.mention}\n{gif_url}")
        else:
            await ctx.send("Could not fetch a kill GIF.")

async def setup(bot):
    await bot.add_cog(KillCog(bot))