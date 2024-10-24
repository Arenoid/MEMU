import discord
from discord.ext import commands
import aiohttp

class boobsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='boobs')
    @commands.is_nsfw()  # This decorator ensures the command only works in NSFW channels
    async def boob(self, ctx):
        
        api_url = "https://api.waifu.im/search/?included_tags=ero"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and data['images']:
                        image_url = data['images'][0]['url']

                        embed = discord.Embed(
                            title="Boobs Image",
                            description="Here's a Boobs from waifu.im.",
                            color=0x800080  # Purple color
                        )
                        embed.set_image(url=image_url)
                        embed.set_footer(text="Powered by waifu.im")

                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Error",
                            description="Could not find any Boobs images at the moment. Please try again later.",
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

    @boob.error
    async def boob_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            await ctx.send("This command can only be used in NSFW channels.")

async def setup(bot):
    await bot.add_cog(boobsCog(bot))
