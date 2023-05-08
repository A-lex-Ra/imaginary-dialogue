import telebot
from telebot import types
import gptapi


bot = telebot.TeleBot('Enter your bot token here')

n = 0


class UserDialog:
    def __init__(self, userid):
        self.id = userid
        self.theme = ''
        self.sp1_name = ''
        self.sp2_name = ''
        self.last_sp1_rep = ''
        self.last_sp2_rep = ''
        self.sp1_rep = ''


users = dict()


@bot.message_handler(commands=['start'])
def start(message):
    userid = message.from_user.id

    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # markup.add(types.KeyboardButton("/dialog"))

    bot.send_message(userid, 'Привет! Я помогу тебе представить любой разговор (все совпадения случайны)!\n'
                                           'Напиши /dialog, чтобы задать персонажей и тему.')


@bot.message_handler(commands=['dialog'])
def config_dialog(message):
    global users
    userid = message.from_user.id
    users[userid] = UserDialog(userid)

    bot.send_message(userid, 'Как зовут первого собеседника?')
    bot.register_next_step_handler(message, get_first_speaker)


def command_handle(message):
    userid = message.from_user.id
    bot.send_message(userid, "Предыдущий процесс был прерван. Вы можете начать новый /dialog")# или покинуть этот чат")


def get_first_speaker(message):
    if message.text[0] == '/':
        command_handle(message)
        return
    global users
    userid = message.from_user.id
    users[userid].sp1_name = message.text

    bot.send_message(userid, 'Как зовут второго собеседника?')
    bot.register_next_step_handler(message, get_second_speaker)


def get_second_speaker(message):
    if message.text[0] == '/':
        command_handle(message)
        return
    global users
    userid = message.from_user.id
    users[userid].sp2_name = message.text

    bot.send_message(userid, 'Тема диалога:')
    bot.register_next_step_handler(message, get_theme)


def get_theme(message):
    if message.text[0] == '/':
        command_handle(message)
        return
    global users
    userid = message.from_user.id
    users[userid].theme = message.text

    start_dialog(userid)


#################### -----Dialog
def start_dialog(userid):
    global users
    markup = types.InlineKeyboardMarkup()  # наша клавиатура
    markup.add(types.InlineKeyboardButton(text='Первое слово за мной!', callback_data='user_replica'),
               types.InlineKeyboardButton(text='Начинайте!', callback_data='force_start_dialog'))

    start_msg = bot.send_message(userid, 'Ваш ID: ' + str(userid) +
                     '\nПервый собеседник: ' + users[userid].sp1_name +
                     '\nВторой собеседник: ' + users[userid].sp2_name +
                                 '\nТема: ' + users[userid].theme, reply_markup=markup)

    # bot.edit_message_reply_markup(start_msg.chat.id,start_msg.id,reply_markup=None)


def get_forced_replica(userid):
    global users
    users[userid].sp1_rep = f"\"{users[userid].sp2_name}, давайте поговорим на тему \"{users[userid].theme}\"\""


def get_gpt_replica(userid):
    global users
    u = users[userid]
    try:
        u.sp1_rep = gptapi.get_answer_from_Davinci(u.sp1_name, u.sp2_name, u.theme,
                                                   u.last_sp1_rep, u.last_sp2_rep)
    except BaseException as e:
        global n
        n += 1
        u.sp1_rep = 'Я - ТЫКВА!!! '+str(n)
        print(e)


def user_replica_handler(message, userid, please_msg):
    if message.text[0] == '/':
        command_handle(message)
        return
    global users
    users[userid].sp1_rep = f"\"{message.text}\""
    dialog_step(userid)
    try:
        bot.delete_message(please_msg.chat.id, please_msg.id)
    except:
        pass
    try:
        bot.delete_message(message.chat.id, message.id)
    except:
        pass


def dialog_step(userid):
    global users

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Далее', callback_data='gpt_replica'),
               types.InlineKeyboardButton(text='Фраза (' + users[userid].sp2_name + ')',
                                          callback_data='user_replica'),
               types.InlineKeyboardButton(text='Хватит!', callback_data='stop'))

    bot.send_message(userid, users[userid].sp1_name + ':\n' + users[userid].sp1_rep, reply_markup=markup)
    users[userid].last_sp1_rep = users[userid].last_sp2_rep
    users[userid].last_sp2_rep = users[userid].sp1_rep
    users[userid].sp1_rep = ''
    users[userid].sp1_name, users[userid].sp2_name = users[userid].sp2_name, \
        users[userid].sp1_name
    print(userid, users[userid].last_sp1_rep, users[userid].last_sp2_rep, "\n", sep="\n")


def finish(userid):
    bot.send_message(userid, "===БОТ===\nДо скорого, человек!)))")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global users
    userid = call.from_user.id
    if call.data == "force_start_dialog":
        get_forced_replica(userid)
        dialog_step(userid)
    elif call.data == "user_replica":
        please_msg = bot.send_message(userid, 'Введите фразу (' + users[userid].sp1_name + "):")
        bot.register_next_step_handler(please_msg, user_replica_handler, userid, please_msg)

    elif call.data == "gpt_replica":
        get_gpt_replica(userid)
        dialog_step(userid)

    elif call.data == "stop":
        finish(userid)
    try:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.id, reply_markup=None)
    except:
        pass



#     if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
#
#         bot.send_message(call.message.chat.id, 'Запомню : )');
#     elif call.data == "no":
#         bot.send_message(call.message.chat.id, 'Ну и не надо!!!');
#         print(call.message.id)
#         for i in range(call.message.id, 0, -1):
#             try:
#                 bot.delete_message(call.message.chat.id, i)
#             except:
#                 break

bot.polling(none_stop=True)
