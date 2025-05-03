import telebot
from telebot import types
from logic import *
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(
        '1 Класс', '2 Класс', '3 Класс', '4 Класс', '5 Класс', '6 Класс',
        '7 Класс', '8 Класс', '9 Класс', '10 Класс', '11 Класс', '12 Класс'
    )
    bot.send_message(
        message.chat.id, 
        "👋 Привет, я твой помощник по расписанию! 📚\n\nВыбери класс, чтобы начать:", 
        reply_markup=markup
    )
    bot.register_next_step_handler(message, choose_class)

# обработка выбора класса
def choose_class(message):
    class_name = message.text[0]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('А-Класс', 'Б-Класс')  # добавлены варианты "А" и "Б"
    msg = bot.send_message(
        message.chat.id, 
        f"Вы выбрали {class_name}. Теперь выбери вариант: А или Б?", 
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, choose_variant, class_name)

# обработка выбора варианта (А или Б)
def choose_variant(message, class_name):
    variant = message.text
    full_class_name = f"{class_name} {variant}"  # составляем полное имя класса
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('📅 Посмотреть расписание на день', '📅 Посмотреть расписание на всю неделю')
    msg = bot.send_message(
        message.chat.id, 
        f"Вы выбрали {full_class_name}. Теперь выбери, что ты хочешь узнать:\n\n🔍",
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, choose_action, full_class_name)

# обработка выбора действия
def choose_action(message, class_name):
    if message.text == '📅 Посмотреть расписание на день':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница')
        msg = bot.send_message(
            message.chat.id, 
            f"Какой день недели тебя интересует? 🧐\nВыбери день:",
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, choose_day, class_name)
    elif message.text == '📅 Посмотреть расписание на всю неделю':
        full_schedule = get_full_week_schedule(class_name)
        bot.send_message(message.chat.id, f"Вот расписание на всю неделю для {class_name}:\n\n{full_schedule}")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выбери один из предложенных вариантов. 📲")

# обработка выбора дня
def choose_day(message, class_name):
    day = message.text
    schedule = get_schedule(class_name, day)
    bot.send_message(message.chat.id, f"📅 Вот расписание для {class_name} на {day}:\n\n{schedule}")

# запуск
print("Бот работает...")
if __name__ == "__main__":
    bot.polling(none_stop=True)
