import discord
from discord.ext import commands
import os
import matplotlib.pyplot as plt
import numpy as np
import easyocr
from sympy import sympify, lambdify

class GraphCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reader = easyocr.Reader(['en'])  # Initialize EasyOCR for English

    async def fetch_equation_from_image(self, image):
        """Extracts equation from an image using EasyOCR."""
        image_path = f"temp_{image.filename}"
        await image.save(image_path)  # Save the image temporarily

        results = self.reader.readtext(image_path)
        os.remove(image_path)  # Remove the temporary image after processing
        equation = ' '.join([result[1] for result in results if result[1]])
        return equation

    @commands.command(name='graph')
    async def graph(self, ctx, *, equation=None):
        """Graph a given equation or an image of an equation."""
        if equation is None and ctx.message.attachments:
            # If no equation is provided, check for an image attachment
            attachment = ctx.message.attachments[0]
            equation = await self.fetch_equation_from_image(attachment)
        
        if equation is None:
            await ctx.send("Please provide an equation or send an image.")
            return

        # Preprocess the equation string
        equation = equation.replace('^', '**')  # Replace ^ with **
        
        # Add implicit multiplication for terms like 2x
        equation = equation.replace(' ', '')  # Remove spaces
        equation = equation.replace('(', '(1*')  # Handle case like (2x) to (1*2x)
        for i in range(len(equation)):
            if equation[i].isdigit() and (i + 1 < len(equation) and equation[i + 1].isalpha()):
                equation = equation[:i + 1] + '*' + equation[i + 1:]  # Insert '*' between number and variable

        try:
            # Convert the equation into a sympy expression
            expr = sympify(equation)
            func = lambdify('x', expr)

            # Generate x values and corresponding y values
            x = np.linspace(-10, 10, 400)
            y = func(x)

            # Plotting the graph
            plt.figure(figsize=(10, 5))
            plt.plot(x, y, label=str(expr))
            plt.title(f'Graph of {equation}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.axhline(0, color='black', linewidth=0.5, ls='--')
            plt.axvline(0, color='black', linewidth=0.5, ls='--')
            plt.grid()
            plt.legend()
            plt.savefig('graph.png')
            plt.close()

            # Send the graph back to the Discord channel
            await ctx.send(file=discord.File('graph.png'))

        except Exception as e:
            await ctx.send(f"An error occurred while processing the equation: {e}")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(GraphCog(bot))
