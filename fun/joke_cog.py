import discord
from discord.ext import commands
import aiohttp

class JokeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='joke')
    async def joke(self, ctx):
        """Fetch a random joke from JokeAPI."""
        api_url = 'https://v2.jokeapi.dev/joke/Any'  # Endpoint to get a random joke

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                if resp.status == 200:
                    joke_data = await resp.json()
                    
                    embed = discord.Embed(title="Here's a Joke for You!", color=0x800080)  # Purple color
                    
                    if joke_data['type'] == 'single':
                        embed.description = joke_data['joke']
                    elif joke_data['type'] == 'twopart':
                        embed.description = joke_data['setup']
                        embed.add_field(name="Punchline", value=joke_data['delivery'])

                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Error",
                        description=f"Failed to fetch joke. Status code: {resp.status}",
                        color=0x800080  # Purple color
                    )
                    await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(JokeCog(bot))
