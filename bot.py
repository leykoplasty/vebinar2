import telebot
import personal_data
import main

token = personal_data.token
bot = telebot.TeleBot(token)

@bot.message_handler(regexp="Хочу найти работу")
def send_report(message):
    bot.reply_to(message, 'Привет, я буду откликаться на вакансии за тебя')
    url_serch_form = main.parser()
    #print(url_serch_form)
    bot.reply_to(message, 'Откликаюсь на все вакансии по этой ссылке:'+url_serch_form)
bot.infinity_polling()