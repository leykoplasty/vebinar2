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
    all_vacs = main.parser(bot,message)
    main.write_gt(all_vacs)

bot.infinity_polling()
