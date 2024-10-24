import discord
from discord.ext import commands
import aiohttp

class AnimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime')
    async def anime(self, ctx, *, title: str):
        """Fetch anime details using the Jikan API."""
        url = f'https://api.jikan.moe/v4/anime?q={title}&limit=1'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data['data']:
                        anime = data['data'][0]
                        embed = discord.Embed(
                            title=anime['title'],
                            description=anime['synopsis'],
                            color=discord.Color.blue()
                        )
                        embed.add_field(name='Episodes', value=anime['episodes'], inline=True)
                        embed.add_field(name='Score', value=anime['score'], inline=True)
                        embed.add_field(name='Status', value=anime['status'], inline=True)
                        embed.set_image(url=anime['images']['jpg']['large_image_url'])
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"No anime found with title: {title}")
                else:
                    await ctx.send("Couldn't fetch anime details. Please try again later.")

async def setup(bot):
    await bot.add_cog(AnimeCog(bot))
