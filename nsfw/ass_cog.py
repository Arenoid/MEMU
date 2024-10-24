import discord
from discord.ext import commands
import aiohttp

class AssCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ass')
    @commands.is_nsfw()  # Restricts command to NSFW channels
    async def milf(self, ctx):
        api_url = "https://api.waifu.im/search/?included_tags=ass"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and data['images']:
                        image_url = data['images'][0]['url']

                        embed = discord.Embed(
                            title="ASS Image",
                            description="Here's an ASS from waifu.im.",
                            color=0x800080  # Purple color
                        )
                        embed.set_image(url=image_url)
                        embed.set_footer(text="Powered by waifu.im")

                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Error",
                            description="Could not find any ASS images at the moment. Please try again later.",
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

    # Error handler to catch when the command is used in non-NSFW channels
    @milf.error
    async def milf_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed = discord.Embed(
                title="NSFW Command",
                description="This command can only be used in NSFW channels. Please try again in an appropriate channel.",
                color=discord.Color.red()  # Red color for warning
            )
            embed.set_footer(text="Contact an admin if you think this is a mistake.")
            await ctx.send(embed=embed)

# This is the required setup function
async def setup(bot):
    await bot.add_cog(AssCog(bot))
