import discord
from discord.ext import commands
import aiohttp
import random

class TriviaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_games = {}

    @commands.command(name='trivia')
    async def gk(self, ctx, num_questions: int = 5, difficulty: str = 'medium'):
        if num_questions <= 0 or num_questions > 20:
            await ctx.send("Please choose a number of questions between 1 and 20.")
            return

        if difficulty.lower() not in ['easy', 'medium', 'hard']:
            await ctx.send("Invalid difficulty! Please choose from 'easy', 'medium', or 'hard'.")
            return

        await self.start_trivia(ctx, num_questions, difficulty.lower())

    async def start_trivia(self, ctx, num_questions, difficulty):
        url = f'https://opentdb.com/api.php?amount={num_questions}&difficulty={difficulty}&type=multiple'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    questions = data.get('results', [])
                    
                    if questions:
                        self.active_games[ctx.author.id] = {
                            'questions': questions,
                            'current_question': 0,
                            'lives': 3,
                            'ctx': ctx
                        }
                        await self.ask_question(ctx)
                    else:
                        await ctx.send("Failed to fetch trivia questions. Please try again later.")
                else:
                    await ctx.send("Failed to reach the trivia server. Please try again later.")

    async def ask_question(self, ctx):
        game = self.active_games.get(ctx.author.id)

        if game and game['lives'] > 0:
            question_data = game['questions'][game['current_question']]
            question = question_data['question']
            correct_answer = question_data['correct_answer']
            incorrect_answers = question_data['incorrect_answers']

            choices = incorrect_answers + [correct_answer]
            random.shuffle(choices)

            game['correct_answer'] = correct_answer
            game['choices'] = choices

            # Clean the question to remove HTML entities if necessary
            question = discord.utils.escape_markdown(question)  # Escape markdown characters for Discord

            embed = discord.Embed(
                title=f"🔮 Trivia Time! Question {game['current_question'] + 1}",
                description=question,
                color=discord.Color.purple()  # Use a soft purple color theme
            )

            for index, choice in enumerate(choices, start=1):
                choice = discord.utils.escape_markdown(choice)  # Escape options for safety
                embed.add_field(
                    name=f"Option {index}",
                    value=f"```{choice}```",  # Format options in a code block style for better readability
                    inline=False
                )

            embed.set_footer(text=f"Lives remaining: {game['lives']} ❤️")
            embed.set_thumbnail(url="https://example.com/purple_trivia_icon.png")  # Add an optional themed thumbnail

            question_message = await ctx.send(embed=embed)

            # React with number emojis for answering options
            reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
            for i in range(len(choices)):
                await question_message.add_reaction(reactions[i])

            game['question_message'] = question_message

        elif game and game['lives'] == 0:
            await ctx.send(f"Game over, {ctx.author.mention}! You've run out of lives. Better luck next time! 💔")
            del self.active_games[ctx.author.id]

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return

        game = self.active_games.get(user.id)
        if game and reaction.message.id == game.get('question_message').id:
            try:
                reaction_map = {
                    '1️⃣': 0,
                    '2️⃣': 1,
                    '3️⃣': 2,
                    '4️⃣': 3
                }

                user_choice_index = reaction_map.get(str(reaction.emoji))

                if user_choice_index is not None:
                    correct_answer = game['correct_answer']
                    chosen_answer = game['choices'][user_choice_index]

                    if chosen_answer == correct_answer:
                        await reaction.message.channel.send(f"🎉 That's correct, {user.mention}! Nicely done!")
                        game['current_question'] += 1  # Move to the next question only if answered correctly
                    else:
                        game['lives'] -= 1
                        await reaction.message.channel.send(f"❌ That's incorrect, {user.mention}. Lives remaining: {game['lives']}. Please try again!")

                    await reaction.message.clear_reactions()  # Remove reactions after an answer is submitted

                    if game['lives'] > 0 and game['current_question'] < len(game['questions']):
                        await self.ask_question(game['ctx'])  # Use the stored context for the next question
                    elif game['lives'] == 0:
                        await reaction.message.channel.send(f"Game over, {user.mention}! You've run out of lives.")
                        del self.active_games[user.id]

            except Exception as e:
                print(f"An error occurred: {e}")

# This is the required setup function
async def setup(bot):
    await bot.add_cog(TriviaCog(bot))
