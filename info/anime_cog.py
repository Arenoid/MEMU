import discord
from discord.ext import commands
import aiohttp

class AnimeInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime')
    async def anime_info(self, ctx, *, anime_name: str):
        """Fetches information about an anime from Kitsu API."""

        # Base URL for the Kitsu API search
        base_url = "https://kitsu.io/api/edge/anime"

        # Setting up the parameters for the search query
        params = {"filter[text]": anime_name}

        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status != 200:
                    await ctx.send("⚠️ An error occurred while fetching the anime details.")
                    return

                data = await response.json()

                # Check if there are results
                if not data["data"]:
                    await ctx.send(f"❌ No anime found with the name '{anime_name}'.")
                    return

                # Fetching the first result
                anime = data["data"][0]["attributes"]

                # Create embed with anime details
                embed = discord.Embed(
                    title=anime["canonicalTitle"],
                    description=anime["synopsis"][:300] + "...",  # Limiting to 300 characters
                    color=0x3498db
                )
                embed.set_thumbnail(url=anime["posterImage"]["medium"])
                embed.add_field(name="❯ Japanese Title", value=anime.get("titles", {}).get("ja_jp", "N/A"), inline=True)
                embed.add_field(name="❯ Age Rating", value=anime.get("ageRating", "N/A"), inline=True)
                embed.add_field(name="❯ Average Rating", value=anime.get("averageRating", "N/A"), inline=True)
                embed.add_field(name="❯ Status", value=anime.get("status", "N/A"), inline=True)
                embed.add_field(name="❯ Episode Count", value=anime.get("episodeCount", "N/A"), inline=True)
                embed.add_field(name="❯ Start Date", value=anime.get("startDate", "N/A"), inline=True)
                embed.add_field(name="❯ End Date", value=anime.get("endDate", "N/A"), inline=True)
                embed.set_footer(text="Data provided by Kitsu.io")

                await ctx.send(embed=embed)

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(AnimeInfo(bot))
