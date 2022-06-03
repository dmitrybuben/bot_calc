import telebot

bot = telebot.TeleBot('5339174241:AAEcujT2D4PvezBEu_lbLkICt8N2vX4TINE')

value = ''  # текущее значение калькулятора
old_value = ''

keyboard = telebot.types.InlineKeyboardMarkup() # создание клавиатуры
keyboard.row(   telebot.types.InlineKeyboardButton(' ', callback_data='no'), # что написано на кнопке и что возращает нажатие 
                telebot.types.InlineKeyboardButton('C', callback_data='C'),
                telebot.types.InlineKeyboardButton('<=', callback_data='<='),
                telebot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(   telebot.types.InlineKeyboardButton('7', callback_data='7'), # что написано на кнопке и что возращает нажатие 
                telebot.types.InlineKeyboardButton('8', callback_data='8'),
                telebot.types.InlineKeyboardButton('9', callback_data='9'),
                telebot.types.InlineKeyboardButton('*', callback_data='*'))

keyboard.row(   telebot.types.InlineKeyboardButton('4', callback_data='4'), # что написано на кнопке и что возращает нажатие 
                telebot.types.InlineKeyboardButton('5', callback_data='5'),
                telebot.types.InlineKeyboardButton('6', callback_data='6'),
                telebot.types.InlineKeyboardButton('-', callback_data='-'))

keyboard.row(   telebot.types.InlineKeyboardButton('1', callback_data='1'), # что написано на кнопке и что возращает нажатие 
                telebot.types.InlineKeyboardButton('2', callback_data='2'),
                telebot.types.InlineKeyboardButton('3', callback_data='3'),
                telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(   telebot.types.InlineKeyboardButton(' ', callback_data='no'), # что написано на кнопке и что возращает нажатие 
                telebot.types.InlineKeyboardButton('0', callback_data='0'),
                telebot.types.InlineKeyboardButton(',', callback_data='.'),
                telebot.types.InlineKeyboardButton('=', callback_data='='))

@bot.message_handler(commands=['start','calc']) # обработчик событий
def getMessage(message):
    global value
    if value == '':
        bot.send_message(message.from_user.id, '0',reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value,reply_markup=keyboard)

@bot.callback_query_handler(func = lambda call: True) # обработчик событий по нажатию кнопки
def callback_func(query):
    global value, old_value
    data = query.data   # то, что возвращает кнопка - чему равен аргумент callback_data
    if data == 'no':
        pass    # оператор-заглушка == отсутствию операции
    elif data == 'C':
        value = ''
    elif data == '<=':
        if value != '':
            value = value[:len(value)-1]
    elif data == '=':
        try:    # обработка исключений - если делить на О
            value = str(eval(value))    # считаем значение
        except:
            value = 'Ошибка!'
    else:
        value += data   # прибавим цифру или знак

    if (value != old_value and value != '') or ('0' != old_value and value == '') :
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id,message_id=query.message.message_id, text='0',reply_markup=keyboard)
            old_value = '0'
        else:
            bot.edit_message_text(chat_id=query.message.chat.id,message_id=query.message.message_id, text=value,reply_markup=keyboard)
            old_value = value

    if value == 'Ошибка': value = ''

print('bot started')

bot.polling(non_stop=False, interval=0) # запуск

