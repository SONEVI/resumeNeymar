import telebot
import random

# Создаем экземпляр бота
bot = telebot.TeleBot('5753088536:AAEca4Q0ShQzXL6P3inPyrNsKW-oXlNeN_Y')

n = open('kontakts.txt', 'r', encoding='UTF-8')
neymar = n.read().split('\n')
n.close()

neymar_img = []
for i in range(2):
    image = open(f'n{i}.jpg', 'rb')
    neymar_img.append(image.read())
    image.close()


@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Неймар Джуниор.")
    markup.add(item1)
    item2 = telebot.types.KeyboardButton("Позвоните мне.")
    markup.add(item2)
    button_phone = telebot.types.KeyboardButton(text="Отправить телефон", request_contact=True)
    markup.add(button_phone)
    bot.send_message(m.chat.id, 'Приветствую. Я бот, который дает резюме и инфо о людях. Выбери кнопку ниже, '
                                'чтобы продолжить.',
                     reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        print(message.contact)
        print(type(message.contact))
        print('Name: ' + str(message.contact.first_name))
        text = 'Пользователь: ' + message.contact.first_name + ': телефон: ' + message.contact.phone_number
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def text_handle(message):
    if message.text.strip() == 'Позвоните мне.':
        bot.send_contact(message.chat.id, '+1234567890', 'Неймар', 'Джуниор')
    bot.send_poll(message.chat.id, question='Кому Неймар забил первый гол за Барселону?',
                  options=('Атлетико', 'Реал Мадрид', 'Депортиво', 'Хетафе'),
                  type='quiz', correct_option=0,
                  explanation='Каталонцы сумели отыграться на 66-й минуте благодаря точному удару Неймара. Для '
                              'бразильца '
                              'этот мяч стал первым за испанский клуб в официальных матчах. Больше соперники голов не '
                              'забивали — матч завершился со счетом 1:1. Ответная встреча состоится 28 августа в '
                              'Барселоне.',
                  close_date=1704063600)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'C:/Python/Project/resume/files/received/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Я это сохраню.")
    except Exception as e:
        bot.reply_to(message, e)


bot.polling(none_stop=True, interval=0)
