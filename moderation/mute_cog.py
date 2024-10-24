import discord
from discord.ext import commands
import asyncio  

class MuteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mute', help='Mutes a member in the server for a specified duration (e.g., 10s, 5m, 1h).')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, duration: str, *, reason=None):
     
        time_multiplier = {'s': 1, 'm': 60, 'h': 3600}
        time_unit = duration[-1]
        if time_unit not in time_multiplier or not duration[:-1].isdigit():
            await ctx.send("Invalid duration format. Use the format like `10s` for seconds, `5m` for minutes, or `1h` for hours.")
            return

       
        duration_in_seconds = int(duration[:-1]) * time_multiplier[time_unit]

        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if not mute_role:
            
            mute_role = await ctx.guild.create_role(name='Muted', permissions=discord.Permissions(send_messages=False, speak=False))

            for channel in ctx.guild.channels:
                await channel.set_permissions(mute_role, speak=False, send_messages=False)

        await member.add_roles(mute_role, reason=reason)
        await ctx.send(f'{member.mention} has been muted for {duration} for: {reason}')

   
        await asyncio.sleep(duration_in_seconds)

        
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f'{member.mention} has been automatically unmuted after {duration}.')

    @commands.command(name='unmute', help='Unmutes a member in the server.')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f'{member.mention} has been unmuted.')
        else:
            await ctx.send(f'{member.mention} is not muted.')

async def setup(bot):
    await bot.add_cog(MuteCog(bot))
