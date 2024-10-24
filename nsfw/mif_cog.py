import discord
from discord.ext import commands
import aiohttp

class MilfCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='milf')
    async def milf(self, ctx):
        """Fetches a random MILF image from waifu.im."""
        # Check if the channel is NSFW
        if not ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="NSFW Only",
                description="This command can only be used in NSFW channels.",
                color=0xFF0000  # Red color for error
            )
            await ctx.send(embed=embed)
            return
        
        api_url = "https://api.waifu.im/search/?included_tags=milf"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and data['images']:
                        image_url = data['images'][0]['url']

                        embed = discord.Embed(
                            title="MILF Image",
                            description="Here's a MILF from waifu.im.",
                            color=0x800080  # Purple color
                        )
                        embed.set_image(url=image_url)
                        embed.set_footer(text="Powered by waifu.im")

                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Error",
                            description="Could not find any MILF images at the moment. Please try again later.",
                            color=0x800080  # Purple color
                        )
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error",
                        description="Failed to fetch images from waifu.im. Please try again later.",
                        color=0x800080  # Purple color
                    )
                    await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MilfCog(bot))
