import discord
from discord.ext import commands
from discord.utils import get
from collections import defaultdict

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warnings = defaultdict(int)  # Store warnings per user

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)  # Only users with the manage_messages permission can use this command
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        # Increment the user's warning count
        self.warnings[member.id] += 1
        warning_count = self.warnings[member.id]

        # Create an embed message for the warning
        embed = discord.Embed(
            title="User Warned",
            description=f"You have been warned in {ctx.guild.name} for: {reason or 'No reason provided.'} (Warning {warning_count}/10)",
            color=discord.Color.purple()
        )

        # Send the warning message to the user
        await member.send(embed=embed)

        # Check the number of warnings and take action if necessary
        if warning_count == 4:
            await self.mute_user(member, ctx.guild)
        elif warning_count == 6:
            await self.kick_user(member, ctx.guild)
        elif warning_count >= 11:
            await self.ban_user(member, ctx.guild)

        # Send feedback to the command issuer
        embed_feedback = discord.Embed(
            title="Warning Issued",
            description=f"{member.mention} has been warned. Total warnings: {warning_count}/10",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed_feedback)

    async def mute_user(self, member, guild):
        role = get(guild.roles, name="Muted")  # Ensure you have a role named "Muted"
        if role:
            await member.add_roles(role)
            embed = discord.Embed(
                title="User Muted",
                description=f"{member.mention} has been muted for exceeding 3 warnings.",
                color=discord.Color.purple()
            )
            await member.send(embed=embed)
            await guild.system_channel.send(embed=embed)
        else:
            print("Muted role not found.")

    async def kick_user(self, member, guild):
        await member.kick(reason="Exceeded 5 warnings.")
        embed = discord.Embed(
            title="User Kicked",
            description=f"{member.mention} has been kicked for exceeding 5 warnings.",
            color=discord.Color.purple()
        )
        await guild.system_channel.send(embed=embed)

    async def ban_user(self, member, guild):
        await member.ban(reason="Exceeded 10 warnings.")
        embed = discord.Embed(
            title="User Banned",
            description=f"{member.mention} has been banned for exceeding 10 warnings.",
            color=discord.Color.purple()
        )
        await guild.system_channel.send(embed=embed)

    @commands.command(name='clear_warnings')
    @commands.has_permissions(manage_messages=True)  # Permission check
    async def clear_warnings(self, ctx, member: discord.Member):
        if member.id in self.warnings:
            del self.warnings[member.id]
            embed = discord.Embed(
                title="Warnings Cleared",
                description=f"{member.mention}'s warnings have been cleared.",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="No Warnings",
                description=f"{member.mention} has no warnings to clear.",
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)

# This is the required setup function
async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
