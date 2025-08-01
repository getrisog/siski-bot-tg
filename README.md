# Pencil GIF Bot

🤖 Telegram bot for sending random GIF animations based on keywords.

## Features

- 🎬 Downloading and sending GIF files from URLs
- 🔑 Configurable keywords
- 🔤 Smart word normalization (understands different forms: "коты" → "кот")
- 😏 Funny responses about boobs ("Not cat, but boobs!")
- 🐳 Docker container support
- 📊 Management and monitoring commands

## Bot Commands

- `/start` - Welcome and bot information
- `/help` - Usage help
- `/status` - Bot status (number of GIF URLs, keywords)
- `/test` - Bot functionality test and word normalization diagnostics

## Installation and Setup

### 1. Get Telegram Bot Token

1. Find @BotFather in Telegram
2. Send `/newbot` command
3. Follow the instructions to create a bot
4. Copy the received token

### 2. Configure GIF URLs

Edit the `gif_urls.txt` file and add your GIF URLs:

```bash
# Each line - new URL
https://www.yapfiles.com/files/1085841/images.gif
https://example.com/another.gif
https://example.com/third.gif

# Lines starting with # - comments
# https://example.com/commented.gif
```

### 3. Configure Environment Variables

Copy the example file and configure variables:

```bash
cp env.example .env
```

Edit the `.env` file:

```env
TELEGRAM_TOKEN=your_actual_bot_token_here
KEYWORDS=кот,собака,машина,природа,еда,сиськи,фото,картинка
GIF_URLS_FILE=gif_urls.txt
```

### 4. Run with Docker

```bash
# Build image
docker build -t pencil-gif-bot .

# Run container
docker run -d --name pencil-bot --env-file .env pencil-gif-bot

# View logs
docker logs -f pencil-bot

# Stop
docker stop pencil-bot
```

### 5. Run without Docker

```bash
# Install uv (if not installed)
pip install uv

# Install dependencies
uv sync

# Run bot
uv run python -m pencil_bot.main
```

## Project Structure

```
argon_bot/
├── pencil_bot/           # Main bot module
│   ├── __init__.py       # Module initialization
│   ├── main.py           # Main startup file
│   ├── config.py         # Configuration
│   ├── gif_bot.py        # Main bot class
│   └── handlers.py       # Command handlers
├── pyproject.toml        # Dependencies for uv
├── Dockerfile            # Docker configuration
├── env.example           # Environment variables example
├── gif_urls.txt          # GIF URLs file
├── README.md             # Documentation
└── .dockerignore         # Docker exclusions
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_TOKEN` | Telegram bot token | Required |
| `KEYWORDS` | Keywords separated by commas | `кот,собака,машина,природа,еда,сиськи` |
| `GIF_URLS_FILE` | GIF URLs file | `gif_urls.txt` |

## Logging

The bot maintains detailed logs of all operations:
- Loading GIF URLs on startup
- Keyword detection
- Downloading and sending GIF files
- Errors

## Security

- Bot runs under non-privileged user in Docker
- All environment variables are loaded from `.env` file

## Troubleshooting

### Bot not responding
1. Check token correctness in `.env`
2. Make sure bot is added to chat
3. Check logs: `docker logs pencil-bot`

### No GIF files
1. Make sure `gif_urls.txt` file exists and contains URLs
2. Check URL accessibility in browser
3. Check file permissions

### Docker errors
1. Make sure Docker is installed
2. Try rebuilding image: `docker build --no-cache -t pencil-gif-bot .` 