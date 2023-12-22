from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove


from config import Token_Api
from keyboards import kb, kb_photo, ikb
import random

bot = Bot(Token_Api)
dp = Dispatcher(bot)


async def on_startup(_):
    print('Я запустился!')


async def send_random(message: types.Message):
    random_photo = random.choice(list(photos.keys()))
    await bot.send_photo(chat_id=message.chat.id,
                         photo=random_photo,
                         caption=photos[random_photo],
                         reply_markup=ikb)

HELP_COMMAND = """
<b>/start</b> - <em>Запуск бота</em>
<b>/help</b> - <em>Помощь!</em>
<b>/desc</b> - <em>Наш бот умеет</em>
<b>/Random photo</b> - <em>Рандомное фото</em>
"""

arr_photos = ["https://www.tutu.ru/file/4/b024c1aad77e42d424c96720b4d60712/",
              "https://www.tutu.ru/file/4/7ad442568e26f7be842fe83f85f8e85f/",
              "https://cfcdn.apowersoft.info/astro/picwish/_astro/banner-img-after@600w.113fbac2.png"]

photos = dict(zip(arr_photos, ['Девушка', 'Природа', 'Семья']))
random_photo = random.choice(list(photos.keys()))
flag = False


@dp.message_handler(Text(equals='Random photo'))
async def open_kb_photo(message: types.Message):
    global random_photo
    await message.answer(text='Рамдомные фотки',
                         reply_markup=ReplyKeyboardRemove())
    # await message.answer(text='Что бы отправить рандомную фотографию нажми кнопку "Рандом"',
    #                      reply_markup=kb_photo)
    await send_random(message)
    await message.delete()


# @dp.message_handler(Text(equals='Рандом'))
# async def send_random_photo(message: types.Message):
#     await send_random(message)
#     await message.delete()


@dp.message_handler(Text(equals='Главное меню'))
async def open_kb(message: types.Message):
    await message.answer(text='Добро пожаловать в главное меню',
                         reply_markup=kb)
    await message.delete()



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(text='Добро пожаловать в наш бот 🙈',
                         reply_markup=kb)
    await message.delete()



@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.answer(text=HELP_COMMAND,
                         parse_mode='HTML')
    await message.delete()


@dp.message_handler(commands=['desc'])
async def desc_command(message: types.Message):
    await message.answer(text='Бот умеет отправлять')
    await bot.send_sticker(chat_id=message.chat.id,
                           sticker="CAACAgIAAxkBAAEK6_llcuX3d-rsSuzirwOD3sBv_SrISgACaQADNyA6CrjgXAux1hKaMwQ")
    await message.delete()


@dp.message_handler(commands=['location'])
async def command_loccat(message: types.Message):
    await bot.send_location(chat_id=message.chat.id,
                            latitude=random.randint(0, 50),
                            longitude=random.randint(0, 50))



@dp.callback_query_handler()
async def callback_random_photo(callback: types.CallbackQuery):
    global random_photo
    global flag
    if callback.data == 'like':
        if not flag:
            await callback.answer('Вам пондравилось!')
            flag = not flag
        else:
            await callback.answer('Вы уже лайкали')
    elif callback.data == 'dislike':
        await callback.answer('Вам не пондравилось')
    elif callback.data == 'main':
        await callback.message.answer(text='Добро пожаловать в главное меню!',
                                      reply_markup=kb)
        await callback.message.delete()
        await callback.answer()
    else:
        random_photo = random.choice(list(filter(lambda x: x != random_photo, list(photos.keys()))))
        await callback.message.edit_media(types.InputMedia(media=random_photo,
                                                           type='photo',
                                                           caption=photos[random_photo]),
                                          reply_markup=ikb)
        await callback.answer()





if __name__ == '__main__':
    executor.start_polling(dispatcher=dp,
                           on_startup=on_startup,
                           skip_updates=True)