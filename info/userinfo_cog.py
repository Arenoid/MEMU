import discord
from discord.ext import commands

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(title=f"👤 User Info for {member}", color=0x800080)  # Purple color
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined at", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Created at", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
        embed.add_field(name="Roles", value=', '.join([role.name for role in member.roles[1:]]), inline=True)

        await ctx.send(embed=embed)

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"🏰 Server Info for {guild.name}", color=0x800080)  # Purple color
        embed.add_field(name="👑 Owner", value=guild.owner, inline=True)
        embed.add_field(name="👥 Members", value=guild.member_count, inline=True)
        embed.add_field(name="📅 Created at", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
