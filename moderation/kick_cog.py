import discord
from discord.ext import commands

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', help='Kicks a member from the server.')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'{member.mention} has been kicked from the server.')
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(KickCog(bot))
