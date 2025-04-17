# 🤖 Truth or Dare Telegram Bot

A Telegram bot that brings chaotic fun to your group chats. Built with Python, `python-telegram-bot`, and a sprinkle of SQLite for storing players. It randomly selects a player and throws them a Truth or Dare question from a CSV file. Simple, stupid, and actually fun.

---

## ⚙️ Features

- `/join` and `/leave` to hop in or out of the game.
- Random player + random question combo.
- CSV-powered question pool.
- SQLite for keeping track of who's playing.
- Works only in **group chats** — no solo truth or dare, you lonely weirdo.

---

## 🐍 Technologies

- Python
- python-telegram-bot
- SQLite3
- pandas
- CSV file for questions

---

## 🧠 How It Works

1. Add the bot to a **Telegram group chat**.
2. Members type `/join` to enter the game.
3. Once there are at least **2 players**, anyone can use `/start_game`.
4. Players type `T` or `D`:
   - A **random player** is chosen.
   - A random **Truth** or **Dare** question is selected from the CSV.
5. Use `/end` to stop the game and clear all players.

---

## 📁 CSV Format (`questions.csv`)

The bot uses a CSV file named `questions.csv` in the same directory, formatted like this:

| Type | questions                           |
|------|-------------------------------------|
| T    | What's your biggest fear?           |
| D    | Do 10 jumping jacks right now.      |
| T    | What's a secret you've never told?  |
| D    | Send a meme to your most recent ex. |

- `Type`: Must be either `T` (Truth) or `D` (Dare)
- `questions`: The actual question text

---

## 🚀 Usage

### 1. Clone the repo:

#### in bash type
git clone https://github.com/your-username/truth-or-dare-bot.git
cd truth-or-dare-bot

### 2. Set your bot token:
#### Open the Python file and replace this:
TOKEN = #bots token
#### With your actual bot token from @BotFather:
TOKEN = "your-super-secret-bot-token"

### 3. Run the bot:
#### python bot.py
