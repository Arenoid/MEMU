import discord
from discord.ext import commands
import requests
import os

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("ACCUWEATHER_API_KEY")
        self.base_url = "http://dataservice.accuweather.com/"

    @commands.command()
    async def weather(self, ctx, *, location: str):
        # Get location key
        location_url = f"{self.base_url}locations/v1/search?q={location}&apikey={self.api_key}"
        location_response = requests.get(location_url)

        if location_response.status_code == 200:
            location_data = location_response.json()
            if not location_data:
                await ctx.send("Location not found.")
                return
            
            location_key = location_data[0]["Key"]

            
            weather_url = f"{self.base_url}currentconditions/v1/{location_key}?apikey={self.api_key}"
            weather_response = requests.get(weather_url)

            if weather_response.status_code == 200:
                weather_data = weather_response.json()[0]
                temperature = weather_data["Temperature"]["Metric"]["Value"]
                weather_text = weather_data["WeatherText"]

            
                embed = discord.Embed(
                    title=f"Weather in {location}",
                    description=f"**Current Conditions:** {weather_text}\n**Temperature:** {temperature}°C",
                    color=discord.Color.blue()  
                )
                embed.set_footer(text="Weather data provided by AccuWeather")
                
                
                embed.title += " 🌤️"
                embed.description += " ☀️"

                await ctx.send(embed=embed)
            else:
                await ctx.send("Error fetching weather data.")
        else:
            await ctx.send("Error fetching location data.")

async def setup(bot):
    await bot.add_cog(WeatherCog(bot))
