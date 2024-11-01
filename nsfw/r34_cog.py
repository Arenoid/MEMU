import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
import random
import asyncio

class r34(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.semaphore = asyncio.Semaphore(10)  # Control concurrency

    @commands.command(name='r34')
    async def nsfw_image(self, ctx, character: str = None, num_images: int = None):
        """Fetches NSFW images of a specific character from SaraHentai."""

        # Check if the command is used in an NSFW channel
        if not ctx.channel.is_nsfw():
            await ctx.send("🔞 This command can only be used in NSFW channels.")
            return

        # Validate input parameters
        if character is None or num_images is None:
            await ctx.send("⚠️ Please provide both the character name and the number of images. Usage: `!hentai <character_name> <number_of_images>`")
            return

        try:
            num_images = int(num_images)  # Convert num_images to integer
        except ValueError:
            await ctx.send("⚠️ The number of images must be a number. Usage: `!hentai <character_name> <number_of_images>`")
            return

        # Limit the number of images requested
        if num_images < 1 or num_images > 5:
            await ctx.send("⚠️ Please request between 1 and 5 images.")
            return

        image_urls = set()  # Use a set for unique URLs

        async with aiohttp.ClientSession() as session:
            # Search URL for SaraHentai with the specified character name
            search_url = f"https://saradahentai.com/?s={character.replace(' ', '+')}&post_type=wp-manga"
            try:
                async with session.get(search_url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')

                        # Collect post links
                        post_links = [post.find('a')['href'] for post in soup.select('.hitmag-post')]

                        # Use asyncio.gather to fetch images from posts concurrently with a semaphore
                        tasks = [self.fetch_post_image(session, post_link, image_urls) for post_link in post_links]
                        await asyncio.gather(*[self.semaphore_task(task) for task in tasks])

                        # Convert set to list for sampling
                        image_urls_list = list(image_urls)

                        # Check if we have enough unique images
                        if len(image_urls_list) < num_images:
                            await ctx.send("⚠️ Not enough unique images found. Sending available images instead.")
                            num_images = len(image_urls_list)

                        # Randomly select the requested number of images
                        random_images = random.sample(image_urls_list, num_images)

                        # Send each selected image URL as an image
                        for image_url in random_images:
                            await ctx.send(image_url)  # Send the image URL directly to Discord
                    else:
                        await ctx.send(f"❌ Error: Failed to retrieve images for '{character}'. Status code: {response.status}")
            except Exception as e:
                await ctx.send(f"❌ An error occurred: {str(e)}")

    async def semaphore_task(self, task):
        """Wrap the task with a semaphore."""
        async with self.semaphore:
            return await task

    async def fetch_post_image(self, session, post_link, image_urls):
        """Fetch the image from the individual post page."""
        try:
            async with session.get(post_link) as post_response:
                if post_response.status == 200:
                    post_html = await post_response.text()
                    post_soup = BeautifulSoup(post_html, 'html.parser')
                    img_tags = post_soup.select('.entry-content img')  # Get all images in the post
                    for img_tag in img_tags:
                        if img_tag.has_attr('src'):
                            image_urls.add(img_tag['src'])  # Add to the set for uniqueness
        except Exception as e:
            print(f"Error fetching {post_link}: {e}")

# Add the cog to the bot
async def setup(bot):
    await bot.add_cog(r34(bot))
