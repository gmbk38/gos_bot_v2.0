import logging
from admin import *
from users import *
from extra import chat_type as ct, was_admin
from logs import User_log as ul

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

API_TOKEN = '5683599741:AAEAaqWehHZX9zzDyEvH9q3g0D3tHDaVR-I'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

admin = False
user = ul()

search = False

@dp.message_handler(commands=['access'])
async def startAns(message: types.Message):

    global admin

    if len(message.text.split()) != 3 or not isAdmin (message.text.split()[1], message.text.split()[2]):
        await message.answer(f'Ошибка!\n\nПроверьте данные для входа и попробуйте снова')

    else:
        await message.answer(f'Здравствуйте, {message.from_user.first_name}\nВы авторизированы в роли администратора', reply_markup=admin_main_kb())
        admin = True


@dp.message_handler(commands=['start'])
async def startAns(message: types.Message):

    if not ct(message):
        user.id = message.chat.id
        user.name = message.chat.title
        user.user_record()
        return False
        
    await message.answer(f'Здравствуйте, {message.from_user.first_name}\nЧем я могу помочь?', reply_markup=main_kb())

    user.id = message.chat.id
    user.name = message.from_user.username
    user.user_record()


@dp.message_handler(commands=['upd'])
async def updAns(message: types.Message):

    global admin

    if len(message.text.split()) != 3 or not admin:
        await message.answer(f'Проверьте корректность данных, в логине и пароле не должно быть пробелов')
    else:
        updLogin(message.text)
        await message.answer(f'Данные обновлены, повторите авторизацию')
        admin = False


@dp.message_handler(commands=['spam'])
async def spamAns(message: types.Message):

    global admin

    if not admin:
        await message.answer(f'Сначала войдите в панель администратора')
    else:
        msg = message.text.split(' ', 1)[1]
        users = msgToAll()
        for id in users:
            await bot.send_message(id, msg)
        await message.answer(f'Рассылка отправлена')  


@dp.message_handler(content_types=['text'])
async def searchAns(message: types.Message):

    global search

    if search:
        if len(infoSearch(message.text)) == 0:
            await bot.send_message(message.chat.id, 'По данному запросу ничего не найдено')
        else:
            data = infoSearch(message.text)
            msg = f'Текст "{message.text}" встречается в следующих направлениях:\n\n'
            for el in data:
                line = f'{el[0]} ▶▶▶ {el[1]}\n\n'
                msg += line
            await bot.delete_message(message.chat.id, message.message_id - 1)
            await bot.send_message(message.chat.id, msg)
            await bot.send_message(message.chat.id, f'Результат поиска находится выше!\n\nВыберите интересующую вас категорию', reply_markup=main_kb())
            search = False
    else:
        await bot.send_message(message.chat.id, 'Сначала выберите поиск 🔎 в меню навигации')


@dp.callback_query_handler()
async def btnAns(callback: types.CallbackQuery):

    global admin
    global search

    if len(callback.data) == 1:
        # Выбрана категория
        await callback.message.edit_text(f'Выберите интересующий вас вопрос', reply_markup=q_kb(callback.data))

    elif len(callback.data.split('_')[0]) == 1 and len(callback.data.split('_')) == 2:
        aData, fData, kb = a_kb(callback.data.split('_'))
        try:
            await bot.send_document(callback.message.chat.id, open(f'files/{fData}', 'rb'))
            await callback.message.delete()
            await bot.send_message(callback.message.chat.id, f'{aData}', reply_markup=kb)
        except Exception as ex:
            await callback.message.edit_text(f'{aData}', reply_markup=kb)

    elif callback.data[:3] == 'faq':
        if len(callback.data) == 3:
            await callback.message.edit_text(f'Выберите интересующий вас вопрос', reply_markup=faq_kb(callback.data))
        else:
            ans, kb = faq_ans_kb(callback.data)
            await callback.message.edit_text(f'{ans}', reply_markup=kb)

    elif callback.data.split('_')[0] == 'addstats':
        addStats(callback.data)
        await callback.message.edit_text(f'Ваша оценка отправлена!\n\nВыберите интересующую вас категорию', reply_markup=main_kb())

    elif callback.data[:6] == 'search':
            search = True
            await callback.message.edit_text(f'Отправьте сообщение с данными для поиска\n\n', reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text="Назад", callback_data="exit")))
    
    elif callback.data[:5] == 'terms':
        if len(callback.data.split('_')) == 1:
            await callback.message.edit_text(f'Выберите интересующий вас термин\n\n', reply_markup=terms_kb(callback.data))
        else:
            aData, fData, kb = terms_kb(callback.data)
            try:
                await bot.send_document(callback.message.chat.id, open(f'files/{fData}', 'rb'))
                await callback.message.delete()
                await bot.send_message(callback.message.chat.id, f'{aData}', reply_markup=kb)
            except Exception as ex:
                await callback.message.edit_text(f'{aData}', reply_markup=kb)
            
    elif callback.data == 'exit':
        search = False
        await callback.message.edit_text(f'Выберите интересующую вас категорию', reply_markup=main_kb())


    # Работа с кнопками админа
    elif callback.data.split('_')[0] == 'admin' and not admin:
        await callback.message.edit_text(f'Сперва выполните вход')
    else:

        if callback.data.split('_')[1] == 'login':
            await callback.message.edit_text(f'Введите новые данные следующим образом:\n\n/upd логин пароль', reply_markup=admin_back_btn())

        if callback.data.split('_')[1] == 'faq':
            await callback.message.edit_text(f'Введите новые данные следующим образом:\n\n/faq  пароль')
            # =========================================================================================================================================================

        if callback.data.split('_')[1] == 'spam':
            await callback.message.edit_text(f'Введите рассылку следующим образом:\n\n/spam сообщение', reply_markup=admin_back_btn())

        if callback.data.split('_')[1] == 'stats':
            await callback.message.edit_text(f'{getStats()}', reply_markup=admin_back_btn())

        if callback.data.split('_')[1] == 'back':
            await callback.message.edit_text(f'Вы авторизированы в роли администратора', reply_markup=admin_main_kb())

        if callback.data.split('_')[1] == 'exit':
            admin = False
            await callback.message.edit_text(f'Выберите интересующую вас категорию', reply_markup=main_kb())

executor.start_polling(dp, skip_updates=True)