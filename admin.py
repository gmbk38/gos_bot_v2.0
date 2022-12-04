import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def load_login():
    data = pd.read_excel('./admin/login.xlsx', header= None).rename(columns={0 : 'login', 1 : 'pwd'})
    return data


def load_stats():
    data = pd.read_excel('./stats/stats.xlsx', header= None).rename(columns={0 : 'category', 1 : 'dope', 2: 'nope'})
    return data


def load_users():
    data = pd.read_excel('./users/users.xlsx', header= None).rename(columns={0 : 'id', 1 : 'name'})
    return data    


def isAdmin(login, pwd):
    data = load_login()
    if (str(login) == str(data.loc[data.shape[0] - 1]['login']) and str(pwd) == str(data.loc[data.shape[0] - 1]['pwd'])):
        return True
    else:
        return False


def admin_main_kb():

    keyboard = InlineKeyboardMarkup()

    login_edit = InlineKeyboardButton(text="Изменить логин и пароль", callback_data="admin_login")
    faq_edit = InlineKeyboardButton(text="Изменить FAQ", callback_data="admin_faq")
    keyboard.row(login_edit, faq_edit)
    statistic = InlineKeyboardButton(text="Статистика", callback_data="admin_stats")
    msg_to_all = InlineKeyboardButton(text="Написать сообщение ВСЕМ", callback_data="admin_spam")
    keyboard.row(statistic, msg_to_all)
    admin_exit = InlineKeyboardButton(text="Выход", callback_data="admin_exit")
    keyboard.add(admin_exit)
    return keyboard


def admin_back_btn():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="admin_back"))
    return keyboard


def getStats():
    users = load_users()
    users_count = 0
    groups_count = 0

    for el in range(users.shape[0]):
        if int(users.loc[el]['id']) > 0:
            users_count += 1
        else:
            groups_count += 1

    ans = f'Актуальная статистика:\n\nКоличество пользователей: {users_count} 👤\n\nКоличество групп: {groups_count} 👥\n\n'

    stats = load_stats()

    for el in range(stats.shape[0]):
        ans += f"{stats.loc[el]['category']}:\n✅ {stats.loc[el]['dope']} ❌ {stats.loc[el]['nope']}\n\n"
    return ans


def updLogin(msg):
    msg = msg.split(' ')
    data = load_login()
    data.loc[data.shape[0]] = [str(msg[1]), str(msg[2])]

    data.to_excel('./admin/login.xlsx', columns= None, index= None, header= None, engine='xlsxwriter')


def msgToAll():
    users = pd.unique(load_users()['id']).tolist()
    return users