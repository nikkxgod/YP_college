import telebot
bot = telebot.TeleBot('7159348995:AAE1Y_Ta2Ey9VPtPWiu6Vz5CIqRhOVbn1VI')
chat_id =  '-1002064549773'
def send_message():
    stroka = (f'да, бери в долг и ставь')
    bot.send_message(chat_id=chat_id, text=stroka)
send_message()