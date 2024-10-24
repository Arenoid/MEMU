import discord
from discord.ext import commands
import aiohttp
import random

class VideoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='video')
    async def video(self, ctx):
        url = 'https://www.reddit.com/r/nextfuckinglevel/hot/.json?limit=100'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        videos = data.get('data', {}).get('children', [])
                        video_data = []

                        for video in videos:
                            if video['data'].get('is_video'):
                                video_url = video['data'].get('media', {}).get('reddit_video', {}).get('fallback_url')
                                title = video['data'].get('title')
                                if video_url and title:
                                    video_data.append((video_url, title))
                        
                        if video_data:
                            selected_video = random.choice(video_data)
                            video_url, title = selected_video
                            await ctx.send(f"**{title}**\n{video_url}")
                        else:
                            await ctx.send("No videos found at the moment.")
                    else:
                        await ctx.send("Failed to fetch videos. Please try again later.")
            except Exception as e:
                print(f"An error occurred: {e}")
                await ctx.send("An error occurred while trying to fetch videos.")

async def setup(bot):
    await bot.add_cog(VideoCog(bot))
