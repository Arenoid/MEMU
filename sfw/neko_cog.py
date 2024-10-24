import discord
from discord.ext import commands
import aiohttp

class nekocog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='neko')
    @commands.is_nsfw() 
    async def nsfw_image(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/sfw/neko') as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get('url')

                
                    embed = discord.Embed(
                        title="Neko Image",
                        description="Here's a random Neko image for you!",
                        color=discord.Color.red()
                    )
                    embed.set_image(url=image_url)
                    embed.set_footer(text="Image provided by waifu.pics")

                    await ctx.send(embed=embed)
                else:
                    await ctx.send('Failed to retrieve image.')

async def setup(bot):
    await bot.add_cog(nekocog(bot))
