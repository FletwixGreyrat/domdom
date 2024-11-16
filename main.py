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
    area = State()
    kompl = State()
    plot = State()
    plan = State()
    pay = State()
# https://telegra.ph/KP-individualnoe-75-m-10-11
# https://telegra.ph/KP-individualnoe-112-m-10-11
# https://telegra.ph/KP-individualnoe-120-m-10-11
# https://telegra.ph/KP-individualnoe-155-m-10-11
# https://telegra.ph/KP-individualnoe-157-m-10-11
# https://telegra.ph/KP-individualnoe-180-m-10-11


@dp.message_handler(commands=["start"], state=None)
async def start_command(message: types.Message):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Начать", callback_data="start_opros"))
    # kb.add(types.InlineKeyboardButton(text='Ознакомиться с общей презентацией', url="https://telegra.ph/wefrgthyju-10-02"))
    photo = open("images/1.png", "rb")
    await bot.send_photo(message.from_user.id, photo=photo, caption="""Вас приветствует компания Дом-Дом 
Мы собрали для Вас самые надежные, теплые, современные дома из 
Полистеролбетона 
Передового по всем характеристикам материала на рынке частного Домостроения.

Уникальные дома в которые вы уже сможете въехать менее чем через 3 месяца после решения строится!

Пожалуйста, ответьте на 5 вопросов (это займет менее 3-хминут), чтобы мы могли подготовить для Вас лучшее предложение и презентацию по дому Вашей мечты. Дополнительно вы получите развернутую консультацию нашего Эксперта, а также полезный подарок на выбор.""", reply_markup=kb)
 

@dp.callback_query_handler(text="start_opros", state=None)
async def start_opros_command(call: types.CallbackQuery):

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="75 м²", callback_data="sel_area:75"))
    kb.add(types.InlineKeyboardButton(text="112 м²", callback_data="sel_area:112"))
    kb.add(types.InlineKeyboardButton(text="120 м²", callback_data="sel_area:120"))
    kb.add(types.InlineKeyboardButton(text="150 м²", callback_data="sel_area:150"))
    kb.add(types.InlineKeyboardButton(text="180 м²", callback_data="sel_area:180"))
    kb.add(types.InlineKeyboardButton(text="Другая площаль", callback_data="sel_area:other"))

    photo = open("images/2.png", "rb")
    await call.message.edit_media(media=types.InputMediaPhoto(media=photo))
    await call.message.edit_caption(caption="Какая площадь дома Вас интересует?", reply_markup=kb)
    await opros_FSM.area.set()
    
# @dp.callback_query_handler(text_startswith="type:", state=opros_FSM)
# async def select_type_command(call: types.CallbackQuery):
#     data = call.data.split(":")[1]
#     kb = types.InlineKeyboardMarkup()
#     if data == "tip":
#         kb.add(types.InlineKeyboardButton(text="75 м²", url="https://telegra.ph/KP-75-m-10-03"))
#         kb.add(types.InlineKeyboardButton(text="112 м²", url="https://telegra.ph/KP-112-m-10-03"))
#         kb.add(types.InlineKeyboardButton(text="120 м²", url="https://telegra.ph/KP-120-m-10-03"))
#         kb.add(types.InlineKeyboardButton(text="155 м²", url="https://telegra.ph/KP-155-m-10-03"))
#         kb.add(types.InlineKeyboardButton(text="157 м²", url="https://telegra.ph/KP-157-m-10-03"))
#         kb.add(types.InlineKeyboardButton(text="180 м²", url="https://telegra.ph/KP-180-m-10-03"))
#         kb.add(types.InlineKeyboardButton(text="Выбрать", callback_data="select_area:tip"))

#     else:

#         # https://telegra.ph/KP-individualnoe-75-m-10-11
# # https://telegra.ph/KP-individualnoe-112-m-10-11
# # https://telegra.ph/KP-individualnoe-120-m-10-11
# # https://telegra.ph/KP-individualnoe-155-m-10-11
# # https://telegra.ph/KP-individualnoe-157-m-10-11
# # https://telegra.ph/KP-individualnoe-180-m-10-11
#         kb.add(types.InlineKeyboardButton(text="75 м²", url="https://telegra.ph/KP-individualnoe-75-m-10-11"))
#         kb.add(types.InlineKeyboardButton(text="112 м²", url="https://telegra.ph/KP-individualnoe-112-m-10-11"))
#         kb.add(types.InlineKeyboardButton(text="120 м²", url="https://telegra.ph/KP-individualnoe-120-m-10-11"))
#         kb.add(types.InlineKeyboardButton(text="155 м²", url="https://telegra.ph/KP-individualnoe-155-m-10-11"))
#         kb.add(types.InlineKeyboardButton(text="157 м²", url="https://telegra.ph/KP-individualnoe-157-m-10-11"))
#         kb.add(types.InlineKeyboardButton(text="180 м²", url="https://telegra.ph/KP-individualnoe-180-m-10-11"))
#         kb.add(types.InlineKeyboardButton(text="Выбрать", callback_data="select_area:ind"))

        
#     await call.message.edit_text("Выберите площадь", reply_markup=kb)



@dp.callback_query_handler(text_startswith="sel_area", state=opros_FSM)
async def select_area_command(call: types.CallbackQuery, state: FSMContext):

    data = call.data.split(":")[1]

    async with state.proxy() as dat:
        if data == "other":
            dat["area"] = "требуется консультация"

        else:
            dat["area"] = data + " м²"

    if data == "other":
        kb = types.ReplyKeyboardMarkup()
        kb.add(types.KeyboardButton(text="Скачать предложение и получить развёрнутую консультацию", request_contact=True))

        await call.message.answer(text="""Спасибо, что заполнили наш опросник
Мы уже готовим предложение для Вас!

Чтобы получить его нажмите на кнопку
""", reply_markup=kb)
    
        await opros_FSM.next()
        await opros_FSM.next()
        await opros_FSM.next()
    
    else:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="1", callback_data="kompl:1"))
        kb.add(types.InlineKeyboardButton(text="2", callback_data="kompl:2"))
        kb.add(types.InlineKeyboardButton(text="3", callback_data="kompl:3"))
        kb.add(types.InlineKeyboardButton(text="4", callback_data="kompl:4"))
        kb.add(types.InlineKeyboardButton(text="Нужна консультация", callback_data="kompl:5"))
        await call.message.edit_media(media=types.InputMediaPhoto(media=open("images/3.png", "rb")))
        await call.message.edit_caption(caption="""Мы предлагаем следующие комплектации:
1. Теплый контур
2. Теплый контур + межкомнатные перегородки
3. Теплый контур + межкомнатные перегородки + инженерные
коммуникации
3. Вайт-бокс (Теплый контур + межкомнатные перегородки + инженерные
коммуникации и предчистовая отделка)
Выберете необходимый вариант ответа:""", reply_markup=kb)
    
    await opros_FSM.next()

@dp.callback_query_handler(text_startswith="kompl:", state=opros_FSM)
async def last_question_command(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(":")[1]
    async with state.proxy() as dat:
        if data == "1":
            dat["kompl"] = "Теплый контур"
        
        elif data == "2":
            dat["kompl"] = "Теплый контур + межкомнатные перегородки"

        elif data == "3":
            dat['kompl'] = "Теплый контур + межкомнатные перегородки + инженерные коммуникации"

        elif data == "4":
            dat["kompl"] = "Вайт-бокс"
        
        elif data == "5":
            dat["kompl"] = "требуется консультация"
    
    if data == "5":
        kb = types.ReplyKeyboardMarkup()
        kb.add(types.KeyboardButton(text="Скачать предложение и получить развёрнутую консультацию", request_contact=True))

        await call.message.answer(text="""Спасибо, что заполнили наш опросник
Мы уже готовим предложение для Вас!

Чтобы получить его нажмите на кнопку
""", reply_markup=kb)
    
        await opros_FSM.next()
        await opros_FSM.next()
    
    else:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="Да, есть", callback_data="plot:yes"))
        kb.add(types.InlineKeyboardButton(text="Нет", callback_data="plot:no"))
        kb.add(types.InlineKeyboardButton(text="На стадии оформления", callback_data="plot:oformlenie"))
        kb.add(types.InlineKeyboardButton(text="На стадии выбора местности", callback_data="plot:mestnost"))
        await call.message.edit_media(media=types.InputMediaPhoto(media=open("images/4.png", "rb")))
        await call.message.edit_caption(caption="У вас есть земельный участок?", reply_markup=kb)

    await opros_FSM.next()

@dp.callback_query_handler(text_startswith="plot:", state=opros_FSM)
async def plan_question_command(call: types.CallbackQuery, state: FSMContext):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Сейчас", callback_data="plan:now"))
    kb.add(types.InlineKeyboardButton(text="В течение 1-2 месяцев", callback_data="plan:1_2_month"))
    kb.add(types.InlineKeyboardButton(text="В течение 6 месяцев", callback_data="plan:6month"))
    kb.add(types.InlineKeyboardButton(text="Пока не определились", callback_data="plan:none"))

    data = call.data.split(":")[1]
    async with state.proxy() as dat:
        if data == "да":
            dat["plot"] = "есть"
        elif data == "нет":
            dat["plot"] = "нет"
        elif data == "oformlenie":
            dat["plot"] = "на стадии оформления"
        else:
            dat["plot"] = "на стадии выбора местности"
        
    await call.message.edit_media(media=types.InputMediaPhoto(media=open("images/5.png", "rb")))
    await call.message.edit_caption(caption="Когда планируете строительство?", reply_markup=kb)
    await opros_FSM.next()



@dp.callback_query_handler(text_startswith="plan:", state=opros_FSM)

async def pay_question_command(call: types.CallbackQuery, state: FSMContext):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="В ипотеку", callback_data="pay:ipoteka"))
    kb.add(types.InlineKeyboardButton(text="За наличные", callback_data="pay:nal"))
    kb.add(types.InlineKeyboardButton(text="По безналичному платежу", callback_data="pay:beznal"))
    kb.add(types.InlineKeyboardButton(text="Нужна консультанция", callback_data="pay:kons"))
    
    data = call.data.split(":")[1]
    async with state.proxy() as dat:
        if data == "1_2_month":
            dat["plan"] = "через три месяца"
        elif data == "now":
            dat["plan"] = "сейчас"
        elif data == "6":
            dat["plan"] = "через 6 месяцев"
        else:
            dat["plan"] = "не определились"
    photo = open("images/6.png", 'rb')
    media = types.InputMediaPhoto(media=photo)
    await call.message.edit_media(media=media)
    await call.message.edit_caption(caption="Как планируете приобретать дом?", reply_markup=kb)
    await opros_FSM.next()



@dp.callback_query_handler(text_startswith="pay:", state=opros_FSM)
async def send_phone_number_command(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(":")[1]
    async with state.proxy() as dat:
        if data == "ipoteka":
            dat["pay"] = "ипотека"
        elif data == "nal":
            dat["pay"] = "наличные"
        elif data == "beznal":
            dat["pay"] = "безналичные"
        elif data == "kons":
            dat["pay"] = "нужна консультация"
    
    
    kb = types.ReplyKeyboardMarkup()
    kb.add(types.KeyboardButton(text="Скачать предложение и получить развёрнутую консультацию", request_contact=True))
    await call.message.answer("""Спасибо, что заполнили наш опросник
Мы уже готовим предложение для Вас!

Чтобы получить его нажмите на кнопку
""", reply_markup=kb)

@dp.message_handler(commands=["s"], state=opros_FSM)
async def zxc(message: types.Message, state: FSMContext):
    await state.finish()


@dp.message_handler(content_types=types.ContentType.CONTACT, state=opros_FSM.pay)
async def get_phone_and_results(message: types.Message, state: FSMContext):
    text = ""
    async with state.proxy() as data:
        area = data["area"]
        text += f"Площадь: {area}\n"
        try:
            kompl = data["kompl"]
            text += f"Комплектация: {kompl}\n"
        except:
            pass
        
        try:
            plot = data["plot"]
            plan = data["plan"]
            pay = data["pay"]
            text += f"Земельный участок: {plot}\n" + f"Планы на заселение: {plan}\n" + f"Форма оплаты: {pay}\n"
        except:
            pass
    text += f"Номер телефона: {message.contact.phone_number}"

    
    if area != "требуется консультация":
        url = f"https://telegra.ph/KP-{area.split()[0]}-m-10-03"
        lst = ["75", "112", "120", "155", "157", "180"]
        lst.remove(area.split()[0])

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="Ознакомиться", url=url))
        kb.add(types.InlineKeyboardButton(text="Еще", callback_data="qq:" + ":".join(lst)))

        await message.answer("Готово! Можете ознакомиться с презентацией\n Вы также можете ознакомиться с нашими типовыми решениями, нажав на кнопку \"Еще\"", reply_markup=kb)
    
    else:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="75 м²", url="https://telegra.ph/KP-75-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="112 м²", url="https://telegra.ph/KP-112-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="120 м²", url="https://telegra.ph/KP-120-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="155 м²", url="https://telegra.ph/KP-155-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="157 м²", url="https://telegra.ph/KP-157-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="180 м²", url="https://telegra.ph/KP-180-m-10-03"))
        await message.answer("Спасибо, наш эксперт скоро свяжется с Вами. А пока вы можете ознакомиться с нашими типовыми решениями", reply_markup=kb)
    # await message.answer(text)

    await state.finish()
    
    await bot.send_message(7527015844, text=text)

@dp.callback_query_handler(text_startswith="qq:")
async def get_prezs(call: types.CallbackQuery):
    data = call.data.split(":")[1:]
    kb = types.InlineKeyboardMarkup()
    for i in data:
        kb.add(types.InlineKeyboardButton(text=f"{i} м²", url=f"https://telegra.ph/KP-{i}-m-10-03"))
    
    await call.message.answer("Готово! Вы можете ознакомиться с презентациями по кнопкам ниже", reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)