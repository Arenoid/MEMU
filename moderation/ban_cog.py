import discord
from discord.ext import commands

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban', help='Bans a member from the server.')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f'{member.mention} has been banned from the server.')
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(BanCog(bot))
