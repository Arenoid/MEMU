import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')
    async def info(self, ctx):
        """Displays a paginated list of commands in different categories."""

        pages = [
            discord.Embed(title="**Help Command - Fun Commands**", description="Here are the fun commands you can use:", color=0x800080)
            .add_field(name="__**🎉 FUN COMMANDS**__", value="Commands to entertain you!", inline=False)
            .add_field(name="`m!magic8ball <question>`", value="Ask a question to the Magic Eight Ball.", inline=False)
            .add_field(name="`m!meme`", value="Get a random meme from the internet.", inline=False)
            .add_field(name="`m!weather <location>`", value="Get the current weather for the specified location.", inline=False)
            .add_field(name="`m!anime <anime name>`", value="Know about an anime!", inline=False)
            .add_field(name="`m!trivia <number> <difficulty>`", value="Random trivia questions!", inline=False)
            .add_field(name="`m!joke`", value="Tells you a joke.", inline=False),

            discord.Embed(title="**Help Command - Safe for Work Commands**", description="Safe for all audiences!", color=0x800080)
            .add_field(name="__**🌸 SAFE FOR WORK (SFW) COMMANDS**__", value="Commands that are safe for all audiences!", inline=False)
            .add_field(name="`m!waifu`", value="Fetch a random waifu image.", inline=False)
            .add_field(name="`m!yeet`", value="YEET YEET YEET.", inline=False)
            .add_field(name="`m!neko`", value="Get a random Neko pic.", inline=False)
            .add_field(name="`m!bonk <@user>`", value="Bonks a user.", inline=False)
            .add_field(name="`m!bully <@user>`", value="Bullies a user.", inline=False)
            .add_field(name="`m!poke <@user>`", value="Pokes the user!", inline=False),

            discord.Embed(title="**Help Command - NSFW Commands**", description="Not safe for work content!", color=0x800080)
            .add_field(name="__**🔞 NSFW COMMANDS**__", value="Contains adult content.", inline=False)
            .add_field(name="`m!hentai <number>`", value="Fetch a random hentai image.", inline=False)
            .add_field(name="`m!blowjob`", value="Fetches a blowjob GIF.", inline=False)
            .add_field(name="`m!trap`", value="Try it yourself :D", inline=False)
            .add_field(name="`m!boobs`", value="Sends images of boobs.", inline=False)
            .add_field(name="`m!ass`", value="Sends images of ass.", inline=False)
            .add_field(name="`m!r34 <character name> <number of images>`", value="Shows you r34 pictures of your choice.", inline=False),

            discord.Embed(title="**Help Command - Moderation Commands**", description="Commands for moderators.", color=0x800080)
            .add_field(name="__**👩‍⚖️ MODERATION COMMANDS**__", value="Commands for server moderation.", inline=False)
            .add_field(name="`m!mute <@user> <time>`", value="Mutes the user from the server.", inline=False)
            .add_field(name="`m!kick <@user>`", value="Kicks the user from the server.", inline=False)
            .add_field(name="`m!ban <@user>`", value="Bans the user permanently.", inline=False)
            .add_field(name="`m!warn <@user>`", value="Warns the user. Actions taken based on warns.", inline=False)
            .add_field(name="`m!purge <number>`", value="Deletes messages from a channel.", inline=False)
        ]

        message = await ctx.send(embed=pages[0])
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        current_page = 0

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            reaction, user = await self.bot.wait_for("reaction_add", check=check)

            if str(reaction.emoji) == "▶️":
                current_page = (current_page + 1) % len(pages)
            elif str(reaction.emoji) == "◀️":
                current_page = (current_page - 1) % len(pages)

            await message.edit(embed=pages[current_page])
            await message.remove_reaction(reaction, user)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
