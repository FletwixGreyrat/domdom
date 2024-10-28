import redis

from config import TOKEN
from aiogram.dispatcher import FSMContext
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters.state import State, StatesGroup


storage = RedisStorage2(host='localhost', port=6379, db=5)

bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)


class opros_FSM(StatesGroup):
    type_of_kp = State()
    area = State()
    last = State()
    plot = State()
    plan = State()
    home = State()
    pay = State()
     


async def start_or_others_symbols(message: types.Message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text='Ознакомиться с общей презентацией', url="https://telegra.ph/wefrgthyju-10-02"))
    await message.answer("Приветственное сообщение", reply_markup=kb)
 

@dp.message_handler(commands=["start"], state=None)
async def start_command(message: types.Message): 
    await start_or_others_symbols(message=message)

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Начать", callback_data="start_opros"))
    await message.answer("Вы не против для начала ответить на несколько вопросов, чтобы мы смогли понять ваши предпочтения и предоставить наиболее подходящий вариант из нашего каталога", reply_markup=kb)



@dp.callback_query_handler(text="start_opros", state=opros_FSM)
async def start_opros_command(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Типовое", callback_data="type:tip"))
    kb.add(types.InlineKeyboardButton("Индивидуальное", callback_data="type:ind"))
    await call.message.answer("Выберите тип КП:", reply_markup=kb)
    
@dp.callback_query_handler(text_startswith="type:")
async def select_type_command(call: types.CallbackQuery):
    data = call.data.split(":")[1]
    kb = types.InlineKeyboardMarkup()
    if data == "tip":
        kb.add(types.InlineKeyboardButton(text="75 м²", url="https://telegra.ph/KP-75-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="112 м²", url="https://telegra.ph/KP-112-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="120 м²", url="https://telegra.ph/KP-120-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="155 м²", url="https://telegra.ph/KP-155-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="157 м²", url="https://telegra.ph/KP-157-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="180 м²", url="https://telegra.ph/KP-180-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="Выбрать", callback_data="select_area:tip"))

    else:
        kb.add(types.InlineKeyboardButton(text="75 м²", url="https://telegra.ph/KP-75-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="112 м²", url="https://telegra.ph/KP-112-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="120 м²", url="https://telegra.ph/KP-120-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="155 м²", url="https://telegra.ph/KP-155-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="157 м²", url="https://telegra.ph/KP-157-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="180 м²", url="https://telegra.ph/KP-180-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="Выбрать", callback_data="select_area:ind"))

        
    await call.message.edit_text("Можете ознакомиться и выбрать площадь", reply_markup=kb)


@dp.callback_query_handler(text_startswith="select_area", state=opros_FSM)
async def show_area_command(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(":")[1]
    await opros_FSM.type_of_kp.set()
    async with state.proxy() as dat:
        if data == "ind":
            dat["type"] = "Индивидуальное"
        else:
            dat["type"] = "Типовое"

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="75 м²", callback_data="sel_area:75"))
    kb.add(types.InlineKeyboardButton(text="112 м²", callback_data="sel_area:112"))
    kb.add(types.InlineKeyboardButton(text="120 м²", callback_data="sel_area:120"))
    kb.add(types.InlineKeyboardButton(text="155 м²", callback_data="sel_area:155"))
    kb.add(types.InlineKeyboardButton(text="157 м²", callback_data="sel_area:157"))
    kb.add(types.InlineKeyboardButton(text="180 м²", callback_data="sel_area:180"))
    kb.add(types.InlineKeyboardButton(text="Назад", callback_data="sel_area:back"))
    await call.message.edit_text(text="Выберите площадь", reply_markup=kb)


@dp.callback_query_handler(text_startswith="sel_area", state=opros_FSM)
async def select_area_command(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(":")[1]

    async with state.proxy() as dat:
        type_of_kp = dat["type"]
    
    kb = types.InlineKeyboardMarkup()
    if data == "back":
        if type_of_kp == "Типовое":


            kb.add(types.InlineKeyboardButton(text="75 м²", url="https://telegra.ph/KP-75-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="112 м²", url="https://telegra.ph/KP-112-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="120 м²", url="https://telegra.ph/KP-120-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="155 м²", url="https://telegra.ph/KP-155-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="157 м²", url="https://telegra.ph/KP-157-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="180 м²", url="https://telegra.ph/KP-180-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="Выбрать", callback_data="select_area"))
            
    
        else:

            kb.add(types.InlineKeyboardButton(text="75 м²", url="https://telegra.ph/KP-75-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="112 м²", url="https://telegra.ph/KP-112-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="120 м²", url="https://telegra.ph/KP-120-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="155 м²", url="https://telegra.ph/KP-155-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="157 м²", url="https://telegra.ph/KP-157-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="180 м²", url="https://telegra.ph/KP-180-m-10-03"))
            kb.add(types.InlineKeyboardButton(text="Выбрать", callback_data="select_area"))
        await call.message.edit_text("Для начала ознакомьтесь с презентацией дома под устраивающую вас площадь", reply_markup=kb)
        return
    
    else:
        

        async with state.proxy() as dat:
            dat["area"] = data + " м²"
            
        kb.add(types.InlineKeyboardButton(text="Теплый контур", callback_data="last:1"))
        kb.add(types.InlineKeyboardButton(text="Теплый контур и перегородки", callback_data="last:2"))
        kb.add(types.InlineKeyboardButton(text="Теплый контур, перегородки и инжекторы", callback_data="last:3"))

        await call.message.edit_text(text="Вот тут не знаю, что написать", reply_markup=kb)


@dp.callback_query_handler(text_startswith="last:", state=opros_FSM)
async def last_question_command(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as dat:
        area = dat["area"]
        dat["last"] = call.data.split(":")[1]
        last = dat["last"]
    

    await call.message.edit_text(f"Площадь: {area}\nЧто-то: {last}")
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Да", callback_data="plot:да"))
    kb.add(types.InlineKeyboardButton(text="Нет", callback_data="plot:нет"))
    kb.add(types.InlineKeyboardButton(text="На стадии оформления", callback_data="plot:oformlenie"))

    await call.message.answer("У вас есть земельный участок?", reply_markup=kb)

    await opros_FSM.next()

@dp.callback_query_handler(text_startswith="plot:", state=opros_FSM)
async def plan_question_command(call: types.CallbackQuery, state: FSMContext):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="сейчас", callback_data="plan:now"))
    kb.add(types.InlineKeyboardButton(text="1-2 месяца", callback_data="plan:1_2_month"))
    kb.add(types.InlineKeyboardButton(text="Через 6 месяцев", callback_data="plan:6month"))
    kb.add(types.InlineKeyboardButton(text="Не определились", callback_data="plan:none"))

    data = call.data.split(":")[1]
    async with state.proxy() as dat:
        if data == "да":
            dat["plot"] = "есть"
        elif data == "нет":
            dat["plot"] = "нет"
        else:
            dat["plot"] = "на стадии оформления"

    await call.message.edit_text(text="Когда планируете строительство?", reply_markup=kb)
    await opros_FSM.next()



@dp.callback_query_handler(text_startswith="plan:", state=opros_FSM)
async def home_question_command(call: types.CallbackQuery, state: FSMContext):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="В течение трех месяцев", callback_data="home:3"))
    kb.add(types.InlineKeyboardButton(text="Через 6 месяцев", callback_data="home:6"))
    kb.add(types.InlineKeyboardButton(text="Не определились", callback_data="home:none"))
    data = call.data.split(":")[1]

    async with state.proxy() as dat:
        if data == "now":
            dat["plan"] = "сейчас"
        elif data == "1_2_month":
            dat["plan"] = "1-2 месяца"
        elif data == "6month":
            dat["plan"] = "через 6 месяцев"
        else:
            dat["plan"] = "не определились"

    await call.message.edit_text(text="Когда хотите заехать в дом?", reply_markup=kb)
    await opros_FSM.next()



@dp.callback_query_handler(text_startswith="home:", state=opros_FSM)
async def pay_question_command(call: types.CallbackQuery, state: FSMContext):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Ипотека", callback_data="pay:ipoteka"))
    kb.add(types.InlineKeyboardButton(text="Наличные", callback_data="pay:nal"))
    kb.add(types.InlineKeyboardButton(text="Безналичные", callback_data="pal:beznal"))
    
    data = call.data.split(":")[1]
    async with state.proxy() as dat:
        if data == "3":
            dat["home"] = "через три месяца"
        elif data == "6":
            dat["home"] = "через 6 месяцев"
        else:
            dat["home"] = "не определились"
    await call.message.edit_text(text="Укажите форму оплаты:", reply_markup=kb)
    await opros_FSM.next()



@dp.callback_query_handler(text_startswith="pay:", state=opros_FSM)
async def send_phone_number_command(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(":")[1]
    async with state.proxy() as dat:
        if data == "ipoteka":
            dat["pay"] = "ипотека"
        elif data == "6":
            dat["pay"] = "наличные"
        else:
            dat["pay"] = "безналичные"
    
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(text="Поделиться контактом📱", request_contact=True))
    
    await call.message.answer("Отправьте свой контакт", reply_markup=kb)

@dp.message_handler(commands=["sex"], state=opros_FSM)
async def zxc(message: types.Message, state: FSMContext):
    await state.finish()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=opros_FSM)
async def get_phone_and_results(message: types.Message, state: FSMContext):
    async with state.proxy() as dat:
        dat["phone"] = message.contact.phone_number
    
        await message.answer(dat)
        await state.finish()

@dp.callback_query_handler(text_startswith="", state=opros_FSM)
async def select_type(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split()

    async with state.proxy() as data:
        data[""]

@dp.message_handler()
async def others_symbols_handler_command(message: types.Message):
    await start_or_others_symbols(message=message)


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)

