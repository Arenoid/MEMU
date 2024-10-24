import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info')
    async def info(self, ctx):
        # Create an array of pages to hold embed objects
        pages = []
        
        # Page 1: Fun Commands
        page1 = discord.Embed(title="**Help Command**", description="Here are the commands you can use:", color=0x800080)  # Purple color
        page1.add_field(name="__**🎉 FUN COMMANDS**__", value="Commands to entertain you!", inline=False)
        page1.add_field(name="`m!magic8ball <question>`", value="Ask a question to the Magic Eight Ball.", inline=False)
        page1.add_field(name="`m!meme`", value="Get a random meme from the internet.", inline=False)
        page1.add_field(name="`m!weather <location>`", value="Get the current weather for the specified location.", inline=False)
        page1.add_field(name="`m!anime <anime name>`", value="Know about an anime!", inline=False)
        page1.add_field(name="`m!trivia <number of questions> <difficulty(easy/medium/hard)>`", value="Ask you random questions about any topics", inline=False)
        page1.add_field(name="`m!joke`", value="Tells you a joke", inline=False)
        pages.append(page1)

        # Page 2: Safe for Work (SFW) Commands
        page2 = discord.Embed(title="**Help Command**", description="Here are the commands you can use:", color=0x800080)
        page2.add_field(name="__**🌸 SAFE FOR WORK (SFW) COMMANDS**__", value="Commands that are safe for all audiences!", inline=False)
        page2.add_field(name="`m!waifu`", value="Fetch a random waifu image.", inline=False)
        page2.add_field(name="`m!yeet`", value="YEET YEET YEET.", inline=False)
        page2.add_field(name="`m!neko`", value="Get a random Neko pic.", inline=False)
        page2.add_field(name="`m!bonk <@user>`", value="Bonks a user.", inline=False)
        page2.add_field(name="`m!bully <@user>`", value="Bullies a user.", inline=False)
        page2.add_field(name="`m!kill <@user>`", value="Kills a user (not IRL).", inline=False)
        page2.add_field(name="`m!poke <@user>`", value="Pokes the user!", inline=False)
        pages.append(page2)

        # Page 3: Not Safe for Work (NSFW) Commands
        page3 = discord.Embed(title="**Help Command**", description="Here are the commands you can use:", color=0x800080)
        page3.add_field(name="__**🔞 NOT SAFE FOR WORK (NSFW) COMMANDS**__", value="Commands that contain adult content.", inline=False)
        page3.add_field(name="`m!hentai <number>`", value="Fetch a random hentai image.", inline=False)
        page3.add_field(name="`m!blowjob`", value="Fetches a blowjob GIF.", inline=False)
        page3.add_field(name="`m!trap`", value="Try it yourself :D", inline=False)
        page3.add_field(name="`m!boobs`", value="Sends images of boobs.", inline=False)
        page3.add_field(name="`m!ass`", value="Sends images of ass.", inline=False)
        page3.add_field(name="`m!milf`", value="Shows you MILF pictures", inline=False)
        pages.append(page3)

        # Page 4: Moderation Commands
        page4 = discord.Embed(title="**Help Command**", description="Here are the commands you can use:", color=0x800080)
        page4.add_field(name="__**👩‍⚖️ MODERATION COMMANDS**__", value="Commands that contain moderation options.", inline=False)
        page4.add_field(name="`m!mute <@user> <time>`", value="Mutes the user from the server.", inline=False)
        page4.add_field(name="`m!kick <@user>`", value="Kicks the user from the server.", inline=False)
        page4.add_field(name="`m!ban <@user>`", value="Bans the user permanently from the server.", inline=False)
        page4.add_field(name="`m!warn <@user>`", value="Warns the user and takes action on the basis of warns! (3 warns = mute || 5 warns = kick || 10 warns = ban)", inline=False)
        page4.add_field(name="`m!purge <no of messages>`", value="Purges messages from a channel.", inline=False)
        pages.append(page4)

        # Send the first page
        message = await ctx.send(embed=pages[0])

        # Add reactions for pagination
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        current_page = 0

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)

                if str(reaction.emoji) == "▶️":
                    current_page += 1
                    if current_page >= len(pages):
                        current_page = 0  # Loop back to the first page
                elif str(reaction.emoji) == "◀️":
                    current_page -= 1
                    if current_page < 0:
                        current_page = len(pages) - 1  # Loop back to the last page

                await message.edit(embed=pages[current_page])
                await message.remove_reaction(reaction, user)

            except Exception as e:
                await ctx.send("Time out! Please use the command again.")
                break

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
