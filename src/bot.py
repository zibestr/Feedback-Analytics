import asyncio
import os
import sys
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
import os
from sqlalchemy import select
import json
import importlib.util

from db_models import db_session
from db_models.courses import Course
from db_models.students import Student
from db_models.feedbacks import Feedback

logging.basicConfig(level=logging.INFO)
API_TOKEN = getToken.getToken()
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

os.chdir(os.path.abspath("src/"))
db_session.global_init(os.path.abspath('web/db/database.sqlite3'))
session = db_session.create_session()
statement = select(Course)
textFromDb = session.scalars(statement).all()


web_size = 10


class ID(StatesGroup):
    ID = State()


class Form(StatesGroup):
    removeID = State()
    WebID = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()



class MarkCallback(CallbackData, prefix="mark"):
    data: int


class CourceCallback(CallbackData, prefix="cource"):
    nex: int
    data: int


async def setUserIDInDB(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ID = int(data["ID"])
    try:
        student = Student(system_id=ID, course_id=1)
        session.add_all([student])
        session.commit()
        await message.answer("ID {} пользователя получен и занесён в базу данных. При желании написать отзыв нажмите команду \n /feedback".format(ID))
    except Exception as e:
        t = state.get_data
        if "(sqlite3.IntegrityError) UNIQUE constraint failed" in str(e) and "ID" in t and t["ID"]>0:
            await message.answer("Такой ID уже используется, просто наберите \n /feedback")
        else:
            print("FFFFFFFFFFFFFFFFFFFF")
        session.rollback()




@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    await message.answer("Здравствуйте, дорогие пользователи. Введите свой код пользователя с сайта")
    await state.set_state(ID.ID)





# Хэндлер на команду /feedback
@dp.message(Command("feedback"))
async def cmd_feedbask(message: types.Message) -> None:
    global textFromDb
    textFromDb = session.scalars(statement).all()
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
    await message.answer("Выбери другие оценки, когда захочешь оставить отзыв")


@dp.callback_query(MarkCallback.filter(F.data > 5))
async def contin(call: Message, state: FSMContext):
    await call.answer("Вы готовы к диалогу")
    await bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )
    builder = InlineKeyboardBuilder()
    if len(textFromDb)<= web_size:
        for index in textFromDb:
            builder.button(text= index.name, callback_data=CourceCallback(data=index.id, nex=-1))
    else:
        for index in textFromDb[:web_size]:
            builder.button(text= index.name, callback_data=CourceCallback(data=index.id, nex=-1))
        builder.button(text=u"\u2192", callback_data=CourceCallback(data=-1,nex=web_size))
    builder.adjust(1)
    await call.message.answer("Выберите вебинар", reply_markup=builder.as_markup())
    await state.set_state(Form.WebID)



@dp.callback_query(CourceCallback.filter(F.nex!=-1))
async def Next(call : CallbackQuery, callback_data : CourceCallback):
    builder = InlineKeyboardBuilder()
    await call.answer()
    for index in textFromDb[callback_data.nex:web_size+callback_data.nex]:
        builder.button(text= index.name, callback_data=CourceCallback(data=index.id, nex=-1))
    if callback_data.nex-web_size>=0:
        builder.button(text=u"\u2190", callback_data=CourceCallback(data=-1,nex=callback_data.nex-web_size))
    if callback_data.nex+web_size<len(textFromDb):
        builder.button(text=u"\u2192", callback_data=CourceCallback(data=-1,nex=callback_data.nex+web_size))
    builder.adjust(1)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=builder.as_markup())


@dp.callback_query(CourceCallback.filter(F.data != -1))
async def Question1(call : CallbackQuery, callback_data: CourceCallback, state: FSMContext) -> None:
    remove = await state.get_data()
    print(remove)
    remove = remove["RemoveMessage"] if "RemoveMessage" in remove else None
    if remove is not None:
        await bot.edit_message_text(chat_id=call.message.chat.id,message_id=remove, text="Выбран вебинар {} \n Что вам больше всего понравилось в теме вебинара и почему?".format(textFromDb[callback_data.data-1].name))
    else:
        r = await call.message.answer("Выбран вебинар {} \n  Что вам больше всего понравилось в теме вебинара и почему?".format(textFromDb[callback_data.data-1].name))
        await state.update_data(RemoveMessage=r.message_id)
    await state.update_data(WebID=callback_data.data)
    await state.set_state(Form.question2)
    await call.answer()



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
        await message.answer("Спасибо за отзыв, мы обязательно его учтём. Если хотите оставить ещё отзыв наберите команду \n /feedback")
        await state.update_data(question5=message.text)
        await putInDb(message, state)
    else:
        await message.answer("Произошла ошибка. Попробуйте позже")


async def putInDb(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    ID = data["ID"]
    await state.clear()
    await state.update_data(ID=ID)
    del data["RemoveMessage"]
    res = {}
    for i in data:
        res[i] = data[i]
    w = str(res) # Сериализованная строка словаря для того, чтобы unique работал
    try:
        statement = select(Student).filter_by(system_id=ID, course_id=1)
        user_obj = session.scalars(statement).all()
        student_id = user_obj[0].id
        feedback = Feedback(answers=w, student_id=student_id)
        session.add_all([feedback])
        session.commit()
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            await message.answer("Отзыв заполняется не первый раз. Все результаты были получены. Вы можете написать отзыв на другой вебинар командой \n /feedback")
            session.rollback()
        print(e)




# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

