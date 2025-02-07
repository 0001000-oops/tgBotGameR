import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from game_logic import QuizGame

   # Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

   # Словарь для хранения игр пользователей
user_games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
       await update.message.reply_text('Привет! Давайте сыграем в викторину! Используйте команду /quiz, чтобы начать.')
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
       user_id = update.message.from_user.id
       user_games[user_id] = QuizGame()
       
       await send_question(update, user_id)

async def send_question(update: Update, user_id):
       game = user_games[user_id]
       
       if game.is_game_over():
           await update.message.reply_text(f'Игра окончена! Ваш результат: {game.get_score()} из {len(game.questions)}.')
           del user_games[user_id]
           return

       question = game.get_current_question()
       answers = question["answers"]
       
       keyboard = [[KeyboardButton(answer)] for answer in answers]
       reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

       await update.message.reply_text(question["question"], reply_markup=reply_markup)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
       user_id = update.message.from_user.id

       if user_id not in user_games:
           await update.message.reply_text('Сначала начните игру с командой /quiz.')
           return

       game = user_games[user_id]
       question = game.get_current_question()

       if update.message.text in question["answers"]:
           answer_index = question["answers"].index(update.message.text)
           is_correct = game.answer_question(answer_index)

           if is_correct:
               await update.message.reply_text('Правильно!')
           else:
               await update.message.reply_text('Неправильно!')

           await send_question(update, user_id)
       else:
           await update.message.reply_text('Пожалуйста, выберите один из предложенных вариантов.')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
       user_id = update.message.from_user.id
       
       if user_id in user_games:
           del user_games[user_id]
           await update.message.reply_text('Игра остановлена.')
       else:
           await update.message.reply_text('У вас нет активной игры.')

if __name__ == '__main__':
       application = ApplicationBuilder().token('7292341333:AAEiaP0p7qYRlCg-5c25Otatusi6bHX3E74').build()

       application.add_handler(CommandHandler('start', start))
       application.add_handler(CommandHandler('quiz', quiz))
       application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))
       application.add_handler(CommandHandler('stop', stop))

       application.run_polling()