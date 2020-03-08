import telebot
import vk_api
import config

token_tg = config.tg_token
token_vk = config.vk_token

bot = telebot.TeleBot(token_tg)
vk = vk_api.VkApi(token=token_vk,
                  api_version='5.50')


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})


@bot.message_handler(commands=['send'])
def start_message(message):
    try:
        info = message.text.split()
        char_id = int(info[1])
        text = info[2]
        write_msg(char_id, text)
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный id')


@bot.message_handler(commands=['get_all_users'])
def start_message(message):
    all_users = vk.method('messages.getConversations',
                          {'offset': 0, 'count': 200, 'filter': 'all', 'extended': False, 'group_id': '141744034'})
    info_users = vk.method('users.get', {
        'user_ids': ','.join(str(chat['conversation']['peer']['id']) for chat in all_users['items'])})
    info_users = [' '.join([str(user['id']), user['first_name'], user['last_name']]) for user in info_users]
    bot.send_message(message.chat.id, '\n'.join(info_users))


@bot.message_handler(commands=['send_all_users'])
def start_message(message):
    all_users = vk.method('messages.getConversations',
                          {'offset': 0, 'count': 200, 'filter': 'all', 'extended': False, 'group_id': '141744034'})
    ids = [chat['conversation']['peer']['id'] for chat in all_users['items']]
    try:
        message_for_send = message.text.split("-")[1]
        for element in ids:
            write_msg(element, message_for_send)
    except IndexError:
        bot.send_message(message.chat.id, 'Неверно отправлено сообщение')
