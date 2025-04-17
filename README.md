# Truth or Dare Telegram Bot 🤖🎲

A Telegram bot that brings the classic Truth or Dare game to your group chats. Written in Python with `python-telegram-bot`, SQLite, and just enough chaos.

![Bot Demo](https://img.shields.io/badge/Demo-%F0%9F%94%A5-red) *(Replace with actual gif/video link if available)*

## Features 🔥
- `/start` - Initiate game (bot auto-resets previous session)
- `/join` - Join the game with your Telegram name
- `/leave` - Bail out like a responsible adult
- `/start_game` - Begin the madness (requires ≥2 players)
- `T`/`D` - Choose Truth or Dare when game starts
- `/end` - Nuclear option to reset everything
- SQLite persistence for player data
- CSV-based question bank (easy to customize)

## Setup ⚙️

### 1. Clone & Dependencies
```bash
git clone https://github.com/yourusername/truth-or-dare-bot.git
cd truth-or-dare-bot
pip install python-telegram-bot pandas
