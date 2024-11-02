# 📚 Discord Bot - Help Command with Categories and Pagination

This is a feature-rich **Help Command** for your Discord bot, offering an interactive and categorized display of commands. Users can explore different categories, including Fun, Safe for Work (SFW), Not Safe for Work (NSFW), Moderation, and Math commands. The bot uses pagination to easily navigate through each category with reactions.

## ✨ Features
- **📄 Categorized Help Commands**: Commands are grouped into specific categories for easy navigation.
- **⏪⏩ Paginated Embeds**: Users can flip through different categories using the ◀️ and ▶️ reactions.
- **⚙️ Modular Design**: Easy to expand with new commands and categories.
- **🔒 NSFW Content Warning**: NSFW commands are separated into their own category for clarity and to respect server settings.

## 📜 Command Categories

### 🎉 Fun Commands
Entertaining commands to have some fun in your server!
- `m!magic8ball <question>` - Ask a question to the Magic Eight Ball.
- `m!meme` - Get a random meme from the internet.
- `m!weather <location>` - Get the current weather for a specified location.
- `m!anime <anime name>` - Get details about an anime.
- `m!trivia <number> <difficulty>` - Get random trivia questions!
- `m!joke` - Tells you a joke.

### 🌸 Safe for Work (SFW) Commands
Commands safe for all audiences.
- `m!waifu` - Fetch a random waifu image.
- `m!yeet` - YEET!
- `m!neko` - Get a random Neko image.
- `m!bonk <@user>` - Bonks a user.
- `m!bully <@user>` - Bullies a user.
- `m!poke <@user>` - Pokes the user!

### 🔞 NSFW Commands
Contains adult content (use with caution).
- `m!hentai <number>` - Fetch a random hentai image.
- `m!blowjob` - Fetches a blowjob GIF.
- `m!trap` - Try it yourself :D
- `m!boobs` - Sends images of boobs.
- `m!ass` - Sends images of ass.
- `m!r34 <character name> <number of images>` - Shows r34 pictures of your choice.

### 👩‍⚖️ Moderation Commands
Commands for server moderation.
- `m!mute <@user> <time>` - Temporarily mutes a user.
- `m!kick <@user>` - Kicks a user from the server.
- `m!ban <@user>` - Bans a user from the server.
- `m!warn <@user>` - Issues a warning to a user.
- `m!purge <number>` - Deletes a specified number of messages from a channel.

### 📐 Math Commands
Solve mathematical problems and graph functions.
- `m!graph <equation>` - Graphs a mathematical equation (supports text or image input).

## 🚀 Getting Started

1. **Install** the required packages:
   ```bash
   pip install discord.py
