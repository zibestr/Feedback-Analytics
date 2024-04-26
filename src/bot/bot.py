import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData
import getToken

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
API_TOKEN = getToken.getToken()
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()


class ID(StatesGroup):
    ID = State()


class Form(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()



class MarkCallback(CallbackData, prefix="am"):
    data: int


class CourceCallback(CallbackData, prefix="am"):
    data: str


async def setUserIDInDB(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ID = data["ID"]
    await message.answer("ID {} пользователя получен и занесён в базу данных. При желании написать отзыв нажмите команду \n /feedback".format(ID))



@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await message.answer("Здравствуйте, дорогие пользователи. Введите свой код пользователя с сайта")
    await state.set_state(ID.ID)





# Хэндлер на команду /start
@dp.message(Command("feedback"))
async def cmd_feedbask(message: types.Message) -> None:
    builder = InlineKeyboardBuilder()
    for index in range(1, 6):
        builder.button(text=f"{index}", callback_data=MarkCallback(data=index))
    builderSecond = InlineKeyboardBuilder()
    for index in range(6, 11):
        builderSecond.button(text=f"{index}", callback_data=MarkCallback(data=index))
    markup_second = InlineKeyboardMarkup(inline_keyboard=builderSecond.export())
    builder.attach(InlineKeyboardBuilder.from_markup(markup_second))
    await message.answer("Здравствуйте. На шкале от 1 до 10, насколько вы готовы поделиться вашим мнением о вебинаре?", reply_markup=builder.as_markup())


@dp.callback_query(MarkCallback.filter(F.data < 6))
async def exit(message: Message):
    await message.answer("Всё понятно, значит пока не готов говорить, крутите его ребята!")


@dp.callback_query(MarkCallback.filter(F.data > 5))
async def contin(call: Message, state: FSMContext):
    await call.answer("Вы готовы к диалогу")
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    builder = InlineKeyboardBuilder()
    textFromDb = ["Курс 1", "Курс 2", "Курс 3", "Курс 4"]
    for index in textFromDb:
        builder.button(text=index, callback_data=CourceCallback(data=index))
    await call.message.answer("Выберите свой курс", reply_markup=builder.as_markup())
    await state.set_state(Form.question1)


@dp.callback_query(CourceCallback.filter(F.data != ""))
async def Question1(call : CallbackQuery, callback_data: CourceCallback, state: FSMContext) -> None:
    #print(callback_data.data)
    await state.update_data(question1=callback_data.data)
    await call.answer()
    await call.message.answer("Что вам больше всего понравилось в теме вебинара и почему?")
    await state.set_state(Form.question2)



# Хэндлер на обработку текстовых сообщений
@dp.message(F.text)
async def echo(message: Message,  state: FSMContext) -> None:
    st = await state.get_state()
    if st==ID.ID:
        await state.update_data(ID=message.text)
        await setUserIDInDB(message, state)
    elif st==Form.question2:
        await message.answer("Были ли моменты в вебинаре, которые вызвали затруднения в понимании материала? Можете описать их?")
        await state.update_data(question2=message.text)
        await state.set_state(Form.question3)
    elif st==Form.question3:
        await message.answer("Какие аспекты вебинара, по вашему мнению, нуждаются в улучшении и какие конкретные изменения вы бы предложили?")
        await state.update_data(question3=message.text)
        await state.set_state(Form.question4)
    elif st==Form.question4:
        await message.answer("Есть ли темы или вопросы, которые вы бы хотели изучить более подробно в следующих занятиях?")
        await state.update_data(question4=message.text)
        await state.set_state(Form.question5)
    elif st==Form.question5:
        await message.answer("Спасибо за отзыв, мы обязательно его учтём")
        await state.update_data(question5=message.text)
        await putInDb(message, state)
    else:
        await message.answer("Произошла ошибка. Попробуйте позже")


async def putInDb(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    s = ""
    for i in data:
        s+= "{} - {}\n".format(i,data[i])
    await message.answer("Этого не должно быть, но пока не прикручена бд сливаем данные сюда \n {}".format(s))




# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

