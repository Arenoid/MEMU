import discord
from discord.ext import commands

class PurgeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purge')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        """Deletes a specified number of messages from the channel."""
        if amount < 1:
            embed = discord.Embed(
                title="Error",
                description="Please specify a number greater than 0.",
                color=0x800080  # Purple color
            )
            await ctx.send(embed=embed)
            return

        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the purge command itself

        embed = discord.Embed(
            title="Purge Command",
            description=f"🗑️ Successfully deleted {len(deleted) - 1} messages!",
            color=0x800080  # Purple color
        )
        await ctx.send(embed=embed, delete_after=5)  # Message auto-deletes after 5 seconds

async def setup(bot):
    await bot.add_cog(PurgeCog(bot))
