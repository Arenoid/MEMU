import discord
from discord.ext import commands
import random

class MagicEightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["eightball", "eight ball", "8ball", "8b"])
    async def magic_eight_ball(self, ctx, *, question):
       
        with open("response.txt") as f:
            random_responses = f.readlines()
            response = random.choice(random_responses).strip()  

        await ctx.send(response)


async def setup(bot):
    await bot.add_cog(MagicEightBall(bot))
