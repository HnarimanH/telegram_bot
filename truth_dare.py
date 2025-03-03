from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import random
import pandas as pd

class DataBase:
    def __init__(self):
        connection = sqlite3.connect("data_base.db")
        cursor = connection.cursor()
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_data(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group1 TEXT NOT NULL,
                player TEXT NOT NULL
            )
            """
        )
        connection.commit()
        connection.close()
    
    def insert(self, group1, name):
        with sqlite3.connect("data_base.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO user_data (group1, player) VALUES (?, ?)",
                (group1, name)
            )
            connection.commit()
    
    def delete(self, group1, name=None):
        with sqlite3.connect("data_base.db") as connection:
            cursor = connection.cursor()
            if name:
                cursor.execute(
                    "DELETE FROM user_data WHERE group1 = ? AND player = ?",
                    (group1, name)
                )
            else:
                cursor.execute(
                    "DELETE FROM user_data WHERE group1 = ?",
                    (group1,)
                )
            connection.commit()

    def select_name(self, group1, name):
        with sqlite3.connect("data_base.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT player FROM user_data WHERE group1 = ? AND player = ?",
                (group1, name)
            )
            result = cursor.fetchone()
            return result[0] if result else None

    def select_all_players(self, group1):
        with sqlite3.connect("data_base.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT player FROM user_data WHERE group1 = ?",
                (group1,)
            )
            result = cursor.fetchall()
            return [row[0] for row in result]  

data_base = DataBase()


TOKEN = "7900842404:AAF7ew8DyO4bEVPvV3OsPmMqXI_EO7B0wKQ"

class Questions:
    def __init__(self):
        try:
            self.df = pd.read_csv("questions.csv")  
            print("CSV file loaded successfully.")
        except FileNotFoundError:
            print("Could not find 'questions.csv'.")
            self.df = None  
    
    def choose_random(self, q_type):
        if self.df is None:
            return "No questions available (CSV file missing)."
        
        if "Type" not in self.df.columns or "Type" not in self.df.columns:
            return "Invalid CSV format: Missing required columns."
        
        questions = self.df[self.df["Type"] == q_type]["questions"].tolist()
        
        if not questions:
            return f"No questions found for type '{q_type}'."
        
        return random.choice(questions)


data_q = Questions()

class Bot:
    def __init__(self):
        self.app = Application.builder().token(TOKEN).build()
        self.players = 0

        
        self.app.add_handler(CommandHandler('start', self.start_command))
        self.app.add_handler(CommandHandler('join', self.join_command))
        self.app.add_handler(CommandHandler('leave', self.leave_command))
        self.app.add_handler(CommandHandler('start_game', self.game_command))
        self.app.add_handler(CommandHandler('end', self.end_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_input))
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat = update.message.chat
        group1 = update.message.chat.title
        data_base.delete(group1)
        if chat.type not in ["group", "supergroup"]:
            await update.message.reply_text("Hi! Let's play Truth or Dare! Add me to a group.")
        else:
            await update.message.reply_text("Hi! Type '/join' to join the game. You need at least 2 players!")

    async def join_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        group1 = update.message.chat.title
        name = update.message.from_user.first_name
        print(f"{name} joined the game from group ({group1}), in data_base: {data_base.select_name(group1, name)}")
        if name == data_base.select_name(group1, name):  
            await update.message.reply_text(f"{name} already joined the game!")
        elif data_base.select_name(group1, name) is None:
            data_base.insert(group1, name)
            self.players += 1
            await update.message.reply_text(f"{name} joined the game!")

    async def leave_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        group1 = update.message.chat.title
        name = update.message.from_user.first_name
        db_name = data_base.select_name(group1, name)

        if db_name is None:
            await update.message.reply_text(f"{name} is not in the game.")
        else:  
            data_base.delete(group1, name)
            await update.message.reply_text(f"{name} left the game!")

    async def game_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        group1 = update.message.chat.title
        all_players = data_base.select_all_players(group1)
        
        if len(all_players) < 2:
            await update.message.reply_text("You need at least 2 players to start the game!")
            return
        
        await update.message.reply_text("Type 'T' for Truth or 'D' for Dare.")

    async def handle_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text.strip().upper()
        group1 = update.message.chat.title
        all_players = data_base.select_all_players(group1)
        
        if user_input in ['T', 'D']:
            player, question = await self.choose_pq(all_players, user_input)
            if player and question:
                await update.message.reply_text(f"{player}, {question}")
            else:
                await update.message.reply_text("No questions available for the selected type.")
        else:
            await update.message.reply_text("Please type 'T' for Truth or 'D' for Dare.")

    async def end_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        group1 = update.message.chat.title
        data_base.delete(group1)
        self.players = 0
        await update.message.reply_text("Game ended. All players have been removed.")

    def run(self):
        print("Bot is running...")
        self.app.run_polling()

    async def choose_pq(self, all_players, user_input):
        print(all_players)
        player = random.choice(all_players)
        question = data_q.choose_random(user_input)
        
        if not question:
            return None, None
        
        return player, question

if __name__ == "__main__":
    bot = Bot()
    bot.run()