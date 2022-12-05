import telebot
import personal_data
import main

token = personal_data.token
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет, чтобы я откликнулся на вакансии, введи "Хочу найти работу"')

@bot.message_handler(regexp="Хочу найти работу")
def send_report(message):
    bot.reply_to(message, 'Я буду откликаться на вакансии за тебя')
    main.parser(bot,message)
    bot.reply_to(message, 'Я откликнулся на 100 вакансий и записал информацию о них в таблицу по этой ссылке:https://docs.google.com/spreadsheets/d/1H8XJHqJivpWBwZleqYAPXZ31S1QgeL1eKLJirw4okgI/edit#gid=0')


bot.infinity_polling()
