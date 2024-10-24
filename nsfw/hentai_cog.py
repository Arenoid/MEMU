import discord
from discord.ext import commands
import aiohttp

class NSFWCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hentai')
    async def nsfw_image(self, ctx, num_images: int = 1):
        """Fetches between 1 and 5 NSFW images from waifu.pics."""

        # Ensure the command is used in an NSFW channel
        if not ctx.channel.is_nsfw():
            embed = discord.Embed(
                title="NSFW Only",
                description="This command can only be used in NSFW channels.",
                color=0xFF0000  # Red color for error
            )
            await ctx.send(embed=embed)
            return

        # Ensure the number of images requested is within the valid range
        if num_images < 1 or num_images > 5:
            await ctx.send("Please request between 1 and 5 images.")
            return

        image_urls = []

        async with aiohttp.ClientSession() as session:
            for _ in range(num_images):
                async with session.get('https://api.waifu.pics/nsfw/waifu') as response:
                    if response.status == 200:
                        data = await response.json()
                        image_urls.append(data.get('url'))
                    else:
                        # Notify the user if any image retrieval fails but continue fetching others
                        await ctx.send(f"Failed to retrieve an image in attempt {_ + 1}.")
        
        # Send all successfully fetched images to the user
        if image_urls:
            await ctx.send("\n".join(image_urls))
        else:
            await ctx.send("No images could be retrieved. Please try again later.")

async def setup(bot):
    await bot.add_cog(NSFWCog(bot))
