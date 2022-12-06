import os
import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def load_4serv():
    data = pd.read_excel('./4services/4serv.xlsx', header= None, sheet_name=[f'Услуга {i}' for i in range (1,5)])
    out = pd.DataFrame(columns=['category', 'q', 'a', 'file'])
    for el in data:
        out = pd.concat([out, data.get(el).rename(columns={0 : 'category', 1 : 'q', 2: 'a', 3 : 'file'})], ignore_index= True)

    return out


def load_faq():
    data = pd.read_excel('./faq/faq.xlsx', header= None).rename(columns={0 : 'q', 1 : 'a'})
    return data


def load_terms():
    data = pd.read_excel('./terms/terms.xlsx', header= None).rename(columns={0 : 'q', 1 : 'a', 2 : 'file'})
    return data



def load_stats():
    data = pd.read_excel('./stats/stats.xlsx', header= None).rename(columns={0 : 'category', 1 : 'dope', 2: 'nope'})

    if data.shape[0] == 0:
        data = pd.DataFrame(columns=['category', 'dope', 'nope'])

    return data
    # Прописать везде для пустых файлов


def main_kb():
    data = load_4serv()
    data = pd.unique(data['category']).tolist()

    keyboard = InlineKeyboardMarkup()
    for element in data:
        keyboard.add(InlineKeyboardButton(text=str(element), callback_data=str(f'{data.index(element)}')))
    keyboard.add(InlineKeyboardButton(text='Часто задаваемые вопросы', callback_data='faq'))
    keyboard.row(InlineKeyboardButton(text='Поиск...🔎', callback_data='search'), InlineKeyboardButton(text='Термины', callback_data='terms'))
    # keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit"))
    return keyboard


def q_kb(categoryId):
    data = load_4serv()
    categoryData = pd.unique(data['category']).tolist()

    rule = categoryData[int(categoryId)]

    keyboard = InlineKeyboardMarkup()
    
    # qCounter = 0
    #qCounter можно убрать
    for el in range(data.shape[0]):
        if data.loc[el]['category'] == rule:
            keyboard.add(InlineKeyboardButton(text=str(data.loc[el]['q']), callback_data=str(f'{categoryId}_{el}'))) #qCounter
            # qCounter += 1

    keyboard.row(InlineKeyboardButton(text='👍', callback_data=f'addstats_1_{categoryId}'), InlineKeyboardButton(text='👎', callback_data=f'addstats_0_{categoryId}'))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit"))
    return keyboard


def a_kb(categoryAndQId):
    data = load_4serv()
    categoryData = pd.unique(data['category']).tolist()

    rule = categoryData[int(categoryAndQId[0])]

    aData = data.loc[int(categoryAndQId[1])]['a']
    fData = data.loc[int(categoryAndQId[1])]['file']

    # aData = out.loc[int(categoryAndQId[1])]['a'].where(out.loc[int(categoryAndQId[1])]['category'] == rule).dropna()
    # fData = out.loc[int(categoryAndQId[1])]['file'].where(out.loc[int(categoryAndQId[1])]['category'] == rule).dropna()

    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit"))
    return aData, fData, keyboard


def faq_kb(categoryId):
    data = load_faq()

    keyboard = InlineKeyboardMarkup()

    for el in range(data.shape[0]):
        keyboard.add(InlineKeyboardButton(text=str(data.loc[el]['q']), callback_data=str(f'{categoryId}_{el}')))

    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit"))
    return keyboard


def faq_ans_kb(categoryAndQId):
    data = load_faq()

    keyboard = InlineKeyboardMarkup()

    if len(categoryAndQId.split('_')) < 2:
        ans = data.loc[int(categoryAndQId[3])]['a']
    else:
        ans = data.loc[int(categoryAndQId.split('_')[1])]['a']
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit"))

    return ans, keyboard


def addStats(mark):
    data = load_4serv()
    categoryData = pd.unique(data['category']).tolist()
    category = categoryData[int(mark.split('_')[2])]

    stats = load_stats()

    if stats[stats['category'] == category].shape[0] == 0:
        stats.loc[stats.shape[0]] = [category, 0, 0]

    for el in range(stats.shape[0]):

        if stats.loc[el]['category'] == category:
            if int(mark.split('_')[1]) == 1:
                stats.loc[el] = [category, int(stats.loc[el]['dope']) + 1, int(stats.loc[el]['nope'])]
            else:
                stats.loc[el] = [category, int(stats.loc[el]['dope']), int(stats.loc[el]['nope']) + 1]

    stats.to_excel('./stats/stats.xlsx', columns= None, index= None, header= None, engine='xlsxwriter')


def infoSearch(msg):
    data = load_4serv()
    ans = []
    for el in range(data.shape[0]):
        if msg[:-2].lower() in data.loc[el]['a'].lower():
            ans.append([data.loc[el]['category'], data.loc[el]['q']])

    return ans


def infoSearch2(msg):
    data = load_terms()
    keyboard = InlineKeyboardMarkup()
    qCounter = 0
    for el in range(data.shape[0]):
            if msg in data.loc[el]['a']:
                keyboard.add(InlineKeyboardButton(text=str(data.loc[el]['q']), callback_data=str(f'terms_{el}')))
                qCounter += 1
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit"))
    return qCounter, keyboard


def terms_kb(msg):

    if len(msg.split('_')) == 1:
        data = load_terms()
        keyboard = InlineKeyboardMarkup()
        for el in range(data.shape[0]):
                keyboard.add(InlineKeyboardButton(text=str(data.loc[el]['q']), callback_data=str(f'{msg.split("_")[0]}_{el}')))
        keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit"))
        return keyboard
    else:
        data = load_terms()
        keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Назад", callback_data="exit"))
        aData = data.loc[int(msg.split('_')[1])]['a']
        fData = data.loc[int(msg.split('_')[1])]['file']
        return aData, fData, keyboard