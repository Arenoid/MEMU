import discord
from discord.ext import commands
import aiohttp

class Blowjob(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='blowjob')
    async def nsfw_image(self, ctx):
        """Fetches a random blowjob image from waifu.pics."""
        
        # Ensure the command is used in an NSFW channel
        if not ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="NSFW Only",
                description="This command can only be used in NSFW channels.",
                color=0xFF0000  # Red color for error
            )
            await ctx.send(embed=embed)
            return
        
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.waifu.pics/nsfw/blowjob') as response:
                if response.status == 200:
                    data = await response.json()
                    image_url = data.get('url')

                    embed = discord.Embed(
                        title="Blowjob",
                        description="Here's a random Blowjob image for you!",
                        color=discord.Color.red()
                    )
                    embed.set_image(url=image_url)
                    embed.set_footer(text="Image provided by waifu.pics")

                    await ctx.send(embed=embed)
                else:
                    await ctx.send('Failed to retrieve image.')

async def setup(bot):
    await bot.add_cog(Blowjob(bot))
