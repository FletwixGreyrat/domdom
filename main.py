import redis
import datetime
from models import *
from sqlalchemy.orm import aliased
from config import TOKEN, settings
from db_helper import db_helper
from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext
from contextlib import asynccontextmanager
from sqlalchemy import insert, select, func, and_
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters.state import State, StatesGroup
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker



engine = create_async_engine(url=settings.url, echo=settings.echo)

session_factory = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
)

storage = RedisStorage2(host='localhost', port=6379, db=5)



bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)


class opros_FSM(StatesGroup):
    area = State()
    kompl = State()
    plot = State()
    plan = State()
    pay = State()


class Statistics_FSM(StatesGroup):
    dates = State()
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
    kb.add(types.InlineKeyboardButton(text="Хай Тек 75 м²", callback_data="sel_area:75"))
    kb.add(types.InlineKeyboardButton(text="Хай Тек 112 м²", callback_data="sel_area:112"))
    kb.add(types.InlineKeyboardButton(text="Хай Тек 120 м²", callback_data="sel_area:120"))
    kb.add(types.InlineKeyboardButton(text="Хай Тек 155 м²", callback_data="sel_area:155"))
    kb.add(types.InlineKeyboardButton(text="Хай Тек 180 м²", callback_data="sel_area:180"))
    kb.add(types.InlineKeyboardButton(text="Микеле 139 м²", callback_data="sel_area:139"))
    kb.add(types.InlineKeyboardButton(text="Другая площаль", callback_data="sel_area:other"))

    photo = open("images/2.png", "rb")
    await call.message.edit_media(media=types.InputMediaPhoto(media=photo))
    await call.message.edit_caption(caption="Какая площадь дома Вас интересует?", reply_markup=kb)
    await opros_FSM.area.set()
    


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
        kb.add(types.InlineKeyboardButton(text="Нужна консультация", callback_data="kompl:5"))
        await call.message.edit_media(media=types.InputMediaPhoto(media=open("images/3.png", "rb")))
        await call.message.edit_caption(caption="""Мы предлагаем следующие комплектации:
1. Теплый контур
2. Теплый контур + межкомнатные перегородки
3. Теплый контур + межкомнатные перегородки + инженерные
коммуникации
Выберете необходимый вариант ответа:""", reply_markup=kb)
    if data == "75":
        answer = "1"

    elif data == "112":
        answer = "2"

    elif data == "120":
        answer = "3"

    elif data == "155":
        answer = "4"

    elif data == "180":
        answer = "5"
    
    elif data == "139":
        answer = "6"
    
    elif data == "other":
        answer = "7"

    async with session_factory() as session:
        await session.execute(insert(Question1).values(type_of_answer=answer, user_id=call.message.chat.id, date=datetime.now().strftime("%Y.%m.%d")))
        await session.commit()


    
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

    async with session_factory() as session:
        await session.execute(insert(Question2).values(type_of_answer=data, user_id=call.message.chat.id, date=datetime.now().strftime("%Y.%m.%d")))
        await session.commit()

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
        
    if data == "да":
        answer = "1"
    elif data == "нет":
        answer = "2"
    elif data == "oformlenie":
        answer = "3"
    else:
        answer = "4"

    
    async with session_factory() as session:
        await session.execute(insert(Question3).values(type_of_answer=answer, user_id=call.message.chat.id, date=datetime.now().strftime("%Y.%m.%d")))
        await session.commit()

        
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

    if data == "1_2_month":
        answer = "1"
    elif data == "now":
        answer = "2"
    elif data == "6":
        answer = "3"
    else:
        answer = "4"
    
    photo = open("images/6.png", 'rb')
    media = types.InputMediaPhoto(media=photo)
    await call.message.edit_media(media=media)
    await call.message.edit_caption(caption="Как планируете приобретать дом?", reply_markup=kb)

    async with session_factory() as session:
        await session.execute(insert(Question4).values(type_of_answer=answer, user_id=call.message.chat.id, date=datetime.now().strftime("%Y.%m.%d")))
        await session.commit()


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

    if data == "ipoteka":
        answer = "1"
    elif data == "nal":
        answer = "2"
    elif data == "beznal":
        answer = "3"
    elif data == "kons":
        answer = "4"
    
    async with session_factory() as session:
        await session.execute(insert(Question5).values(type_of_answer=answer, user_id=call.message.chat.id, date=datetime.now().strftime("%Y.%m.%d") ))
        await session.commit()

@dp.message_handler(commands=["s"], state=opros_FSM)
async def zxc(message: types.Message, state: FSMContext):
    await state.finish()


@dp.message_handler(commands=["ss"], state=Statistics_FSM)
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
    async with session_factory() as session:
        await session.execute(insert(FormIsPassed).values(user_id=message.from_user.id))
        await session.commit()
    
    if area != "требуется консультация":
        url = f"https://telegra.ph/KP-{area.split()[0]}-m-10-03"
        lst = ["75", "112", "120", "155", "157", "180", "139"]
        lst.remove(area.split()[0])

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="Ознакомиться", url=url))
        kb.add(types.InlineKeyboardButton(text="Еще", callback_data="qq:" + ":".join(lst)))

        await message.answer("Готово! Можете ознакомиться с презентацией\n Вы также можете ознакомиться с нашими типовыми решениями, нажав на кнопку \"Еще\"", reply_markup=kb)
    
    else:
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton(text="Хай Тек 75 м²", url="https://telegra.ph/KP-75-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="Хай Тек 112 м²", url="https://telegra.ph/KP-112-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="Хай Тек 120 м²", url="https://telegra.ph/KP-120-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="Хай Тек 155 м²", url="https://telegra.ph/KP-155-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="Калифорния 157 м²", url="https://telegra.ph/KP-157-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="Хай Тек 180 м²", url="https://telegra.ph/KP-180-m-10-03"))
        kb.add(types.InlineKeyboardButton(text="Микеле 139 м²", url="https://telegra.ph/KP-139-m-10-03"))
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



@dp.message_handler(commands=["stat"])
async def stat_start_fsm_idite_nahui_command(message: types.Message):
    admins = [277080855, 1047632917, 6142402831, 7527015844]
    if not message.from_user.id in admins:
        return
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Все время", callback_data="statistics:all_day"))

    await message.answer("""Введите промежуток дат в формате:     
ГГГГ.ММ.ДД
ГГГГ.ММ.ДД
""", reply_markup=kb)
    await Statistics_FSM.dates.set()


@dp.callback_query_handler(text_startswith="statistics:", state=Statistics_FSM)
async def get_statistics_of_all_the_time_command(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["date1"] = "2024.12.04"
        data["date2"] = datetime.now().strftime("%Y.%m.%d")
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Опрос пройден", callback_data="opr:passed"))
    kb.add(types.InlineKeyboardButton(text="Опрос не пройден", callback_data="opr:not"))
    kb.add(types.InlineKeyboardButton(text="Все данные", callback_data="opr:all"))


    await call.message.answer("Выберите тип проверки", reply_markup=kb)

@dp.message_handler(content_types="text", state=Statistics_FSM)
async def stat_date_fsm_idite_nahui_command(message: types.Message, state: FSMContext):
    date1, date2 = message.text.split("\n")
    

    try:

        d1 = datetime.strptime(date1, "%Y.%m.%d")
        d2 = datetime.strptime(date2, "%Y.%m.%d")


        if d1 > d2:
            raise ValueError("Первая дата должна быть меньше или равна второй дате.")
        
    except Exception as e:
        await message.answer("Неверный формат")
        return

    async with state.proxy() as data:
        data["date1"] = date1
        data["date2"] = date2
    
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(text="Опрос пройден", callback_data="opr:passed"))
    kb.add(types.InlineKeyboardButton(text="Опрос не пройден", callback_data="opr:not"))
    kb.add(types.InlineKeyboardButton(text="Все данные", callback_data="opr:all"))


    await message.answer("Выберите тип проверки", reply_markup=kb)


@dp.callback_query_handler(text_startswith="opr:", state=Statistics_FSM)
async def get_all_statistics(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split(":")[1]
    translate_question1 = {
        "1": "75",
        "2": "112",
        "3": "120",
        "4": "155",
        "5": "180",
        "6": "139",
        "7": "консультация"
    }

    translate_question2 = {
        "1": "Теплый контур",
        "2": "контур + перегородки",
        "3": "контур + перегородки + коммуникации",
        "5": "консультация",
    }

    translate_question3 = {
        "1": "есть",
        "2": "нет",
        "3": "оформление",
        "4": "выбор местности"
    }

    translate_question4 = {
        "1": "1-2 месяца",
        "2": "сейчас",
        "3": "через 6 месяцев",
        "4": "не определились"
    }

    translate_question5 = {
        "1": "ипотека",
        "2": "наличные",
        "3": "безналичные",
        "4": "консультация"
    }

    async with session_factory() as session:
        async with state.proxy() as dat:
            date1 = dat["date1"]
            date2 = dat["date2"]


        # ! НЕ ТРОГАТЬ
        subquery = select(FormIsPassed.user_id).distinct().subquery()
        # ! НЕ ТРОГАТЬ

        if data == "passed":
            type_ = "опрос пройден"
            # QUESTION 1

            query_exists = (
                select(Question1.type_of_answer, func.count().label("count"))
                .join(subquery, Question1.user_id == subquery.c.user_id)
                .where(and_(Question1.date >= date1, Question1.date <= date2))
                .group_by(Question1.type_of_answer)
            )
            
            result_exists = await session.execute(query_exists)
            q1 = {}
            for row in result_exists:
                q1[translate_question1[row[0]]] = row[1]

            not_added = list(translate_question1.values())
            for i in not_added:
                if not i in q1:
                    q1[i] = 0

            # QUESTION 2

            query_exists = (
                select(Question2.type_of_answer, func.count().label("count"))
                .join(subquery, Question2.user_id == subquery.c.user_id)
                .where(and_(Question2.date >= date1, Question2.date <= date2))
                .group_by(Question2.type_of_answer)
            )
            
            result_exists = await session.execute(query_exists)
            q2 = {}
            for row in result_exists:
                q2[translate_question2[row[0]]] = row[1]
            
            not_added = list(translate_question2.values())
            for i in not_added:
                if not i in q2:
                    q2[i] = 0
            # QUESTION 3

            query_exists = (
                select(Question3.type_of_answer, func.count().label("count"))
                .join(subquery, Question3.user_id == subquery.c.user_id)
                .where(and_(Question3.date >= date1, Question3.date <= date2))
                .group_by(Question3.type_of_answer)
            )
            
            result_exists = await session.execute(query_exists)
            q3 = {}
            for row in result_exists:
                q3[translate_question3[row[0]]] = row[1]

            not_added = list(translate_question3.values())
            for i in not_added:
                if not i in q3:
                    q3[i] = 0
            # QUESTION 4

            query_exists = (
                select(Question4.type_of_answer, func.count().label("count"))
                .join(subquery, Question4.user_id == subquery.c.user_id)
                .where(and_(Question4.date >= date1, Question4.date <= date2))
                .group_by(Question4.type_of_answer)
            )
            
            result_exists = await session.execute(query_exists)
            q4 = {}
            for row in result_exists:
                q4[translate_question4[row[0]]] = row[1]

            not_added = list(translate_question4.values())
            for i in not_added:
                if not i in q4:
                    q4[i] = 0
            # QUESTION 5

            query_exists = (
                select(Question5.type_of_answer, func.count().label("count"))
                .join(subquery, Question5.user_id == subquery.c.user_id)
                .where(and_(Question5.date >= date1, Question5.date <= date2))
                .group_by(Question5.type_of_answer)
            )
            
            result_exists = await session.execute(query_exists)
            q5 = {}
            for row in result_exists:
                q5[translate_question5[row[0]]] = row[1]

            not_added = list(translate_question5.values())
            for i in not_added:
                if not i in q5:
                    q5[i] = 0
        elif data == "not":
            type_ = "опрос не пройден"
            # QUESTION 1

            query_not_exists = (
                select(Question1.type_of_answer, func.count().label("count"))
                .outerjoin(subquery, Question1.user_id == subquery.c.user_id)
                .where(and_(Question1.date >= date1, Question1.date <= date2, subquery.c.user_id == None))
                .group_by(Question1.type_of_answer)
            )
        
            result_not_exists = await session.execute(query_not_exists)
            q1 = {}

            for row in result_not_exists:
                q1[translate_question1[row[0]]] = row[1]
            
            not_added = list(translate_question1.values())
            for i in not_added:
                if not i in q1:
                    q1[i] = 0
            # QUESTION 2

            query_not_exists = (
                select(Question2.type_of_answer, func.count().label("count"))
                .outerjoin(subquery, Question2.user_id == subquery.c.user_id)
                .where(and_(Question2.date >= date1, Question2.date <= date2, subquery.c.user_id == None))
                .group_by(Question2.type_of_answer)
            )
        
            result_not_exists = await session.execute(query_not_exists)
            q2 = {}
            for row in result_not_exists:
                q2[translate_question2[row[0]]] = row[1]

            not_added = list(translate_question2.values())
            for i in not_added:
                if not i in q2:
                    q2[i] = 0
            # QUESTION 3

            query_not_exists = (
                select(Question3.type_of_answer, func.count().label("count"))
                .outerjoin(subquery, Question3.user_id == subquery.c.user_id)
                .where(and_(Question3.date >= date1, Question3.date <= date2, subquery.c.user_id == None))
                .group_by(Question3.type_of_answer)
            )
        
            result_not_exists = await session.execute(query_not_exists)
            q3 = {}
            for row in result_not_exists:
                q3[translate_question3[row[0]]] = row[1]

            not_added = list(translate_question3.values())
            for i in not_added:
                if not i in q3:
                    q3[i] = 0
            # QUESTION 4

            query_not_exists = (
                select(Question4.type_of_answer, func.count().label("count"))
                .outerjoin(subquery, Question4.user_id == subquery.c.user_id)
                .where(and_(Question4.date >= date1, Question4.date <= date2, subquery.c.user_id == None))
                .group_by(Question4.type_of_answer)
            )
        
            result_not_exists = await session.execute(query_not_exists)
            q4 = {}
            for row in result_not_exists:
                q4[translate_question4[row[0]]] = row[1]

            not_added = list(translate_question4.values())
            for i in not_added:
                if not i in q4:
                    q4[i] = 0
            # QUESTION 5

            query_not_exists = (
                select(Question5.type_of_answer, func.count().label("count"))
                .outerjoin(subquery, Question5.user_id == subquery.c.user_id)
                .where(and_(Question5.date >= date1, Question5.date <= date2, subquery.c.user_id == None))
                .group_by(Question5.type_of_answer)
            )
        
            result_not_exists = await session.execute(query_not_exists)
            q5 = {}
            for row in result_not_exists:
                q5[translate_question5[row[0]]] = row[1]

            not_added = list(translate_question5.values())
            for i in not_added:
                if not i in q5:
                    q5[i] = 0
            
        else:
            type_ = "все данные"
            # QUESTION 1

            query_all = (
                select(Question1.type_of_answer, func.count().label("count"))
                .where(and_(Question1.date >= date1, Question1.date <= date2))
                .group_by(Question1.type_of_answer)
            )

            result_all = await session.execute(query_all)
            q1 = {}
            for row in result_all:
                q1[translate_question1[row[0]]] = row[1]

            not_added = list(translate_question1.values())
            for i in not_added:
                if not i in q1:
                    q1[i] = 0
            # QUESTION 2

            query_all = (
                select(Question2.type_of_answer, func.count().label("count"))
                .where(and_(Question2.date >= date1, Question2.date <= date2))
                .group_by(Question2.type_of_answer)
            )


            result_all = await session.execute(query_all)
            q2 = {}
            for row in result_all:
                q2[translate_question2[row[0]]] = row[1]

            not_added = list(translate_question2.values())
            for i in not_added:
                if not i in q2:
                    q2[i] = 0
            # QUESTION 3

            query_all = (
                select(Question3.type_of_answer, func.count().label("count"))
                .where(and_(Question3.date >= date1, Question3.date <= date2))
                .group_by(Question3.type_of_answer)
            )

            result_all = await session.execute(query_all)
            q3 = {}
            for row in result_all:
                q3[translate_question3[row[0]]] = row[1]

            not_added = list(translate_question3.values())
            for i in not_added:
                if not i in q3:
                    q3[i] = 0
            # QUESTION 4

            query_all = (
                select(Question4.type_of_answer, func.count().label("count"))
                .where(and_(Question4.date >= date1, Question4.date <= date2))
                .group_by(Question4.type_of_answer)
            )

            result_all = await session.execute(query_all)
            q4 = {}
            for row in result_all:
                q4[translate_question4[row[0]]] = row[1]


            not_added = list(translate_question4.values())
            for i in not_added:
                if not i in q4:
                    q4[i] = 0
            # QUESTION 5

            query_all = (
                select(Question5.type_of_answer, func.count().label("count"))
                .where(and_(Question5.date >= date1, Question5.date <= date2))
                .group_by(Question5.type_of_answer)
            )

            result_all = await session.execute(query_all)
            q5 = {}
            for row in result_all:
                q5[translate_question5[row[0]]] = row[1]

            not_added = list(translate_question5.values())
            for i in not_added:
                if not i in q5:
                    q5[i] = 0
    text = f"""
Тип проверки: {type_}
Даты выборки: с {date1} по {date2}

Площадь:
75 м²: {q1["75"]}
112 м²: {q1["112"]}
120 м²: {q1["120"]}
155 м²: {q1["155"]}
180 м²: {q1["180"]}
Консультация: {q1["консультация"]}

Комплектация:
Теплый контур: {q2["Теплый контур"]}
Контур + перегородки: {q2["контур + перегородки"]}
Контур + перегородки + коммуникации: {q2["контур + перегородки + коммуникации"]}
Консультация: {q2["консультация"]}

Наличие участка:
Есть: {q3["есть"]}
Нет: {q3["нет"]}
Оформление: {q3["оформление"]}
Выбор местности: {q3["выбор местности"]}

Планирование строительства:
1-2 месяца: {q4["1-2 месяца"]}
Сейчас: {q4["сейчас"]}
Через 6 месяцев: {q4["через 6 месяцев"]}
Не определились: {q4["не определились"]}

Покупка дома:
Ипотека: {q5["ипотека"]}
Наличные: {q5["наличные"]}
Безналичные: {q5["безналичные"]}
Консультация: {q5["консультация"]}
"""

    await call.message.answer(text)
    await state.finish()





        

        # Обработка результатов
        # stats_exists = {row[0]: row[1] for row in result_exists}
        # stats_not_exists = {row[0]: row[1] for row in result_not_exists}

    # async with session_factory() as session:
    #         # Que 1
    #         if data == "passed":
    #             total_count_query = select(func.count().label('total_count')).select_from(Question1)

    #             query = (
    #                 select(Question1.type_of_answer, func.count().label('answer_count'))
    #                 .join(FormIsPassed, Question1.user_id == FormIsPassed.user_id)
    #                 .group_by(Question1.type_of_answer)
    #             )

    #             total_count_res = await session.execute(total_count_query)
    #             total_count = total_count_res.scalar()

    #             res = await session.execute(query)
    #             rows = res.fetchall()
    #             que1 = {}
    #             for row in rows:
    #                 normalized_count = row.answer_count / total_count
    #                 que1[translate_question1[row.type_of_answer]] = int(normalized_count)
                    
    #             #  Que 2

    #             total_count_query = select(func.count().label('total_count')).select_from(Question2)

    #             query = (
    #                 select(Question2.type_of_answer, func.count().label('answer_count'))
    #                 .join(FormIsPassed, Question2.user_id == FormIsPassed.user_id)
    #                 .group_by(Question2.type_of_answer)
    #             )

    #             total_count_res = await session.execute(total_count_query)
    #             total_count = total_count_res.scalar()

    #             res = await session.execute(query)
    #             rows = res.fetchall()
    #             que2 = {}
    #             for row in rows:
    #                 normalized_count = row.answer_count / total_count
    #                 que2[translate_question2[row.type_of_answer]] = int(normalized_count)

    #             # Que3

    #             total_count_query = select(func.count().label('total_count')).select_from(Question3)

    #             query = (
    #                 select(Question3.type_of_answer, func.count().label('answer_count'))
    #                 .join(FormIsPassed, Question3.user_id == FormIsPassed.user_id)
    #                 .group_by(Question3.type_of_answer)
    #             )

    #             total_count_res = await session.execute(total_count_query)
    #             total_count = total_count_res.scalar()

    #             res = await session.execute(query)
    #             rows = res.fetchall()
    #             que3 = {}
    #             for row in rows:
    #                 normalized_count = row.answer_count / total_count
    #                 que3[translate_question3[row.type_of_answer]] = int(normalized_count)

    #             # Que4

    #             total_count_query = select(func.count().label('total_count')).select_from(Question4)

    #             query = (
    #                 select(Question4.type_of_answer, func.count().label('answer_count'))
    #                 .join(FormIsPassed, Question4.user_id == FormIsPassed.user_id)
    #                 .group_by(Question4.type_of_answer)
    #             )

    #             total_count_res = await session.execute(total_count_query)
    #             total_count = total_count_res.scalar()

    #             res = await session.execute(query)
    #             rows = res.fetchall()
    #             que4 = {}
    #             for row in rows:
    #                 normalized_count = row.answer_count / total_count
    #                 que4[translate_question4[row.type_of_answer]] = int(normalized_count)

    #             #  Que5

    #             total_count_query = select(func.count().label('total_count')).select_from(Question5)

    #             query = (
    #                 select(Question5.type_of_answer, func.count().label('answer_count'))
    #                 .join(FormIsPassed, Question5.user_id == FormIsPassed.user_id)
    #                 .group_by(Question5.type_of_answer)
    #             )

    #             total_count_res = await session.execute(total_count_query)
    #             total_count = total_count_res.scalar()

    #             res = await session.execute(query)
    #             rows = res.fetchall()
    #             que5 = {}
    #             for row in rows:
    #                 normalized_count = row.answer_count / total_count
    #                 que5[translate_question5[row.type_of_answer]] = int(normalized_count)


    #         if data == "not":
                
    #             query = (
    #         select(Question1.type_of_answer, func.count().label("answer_count"))
    #         .outerjoin(FormIsPassed, Question1.user_id == FormIsPassed.user_id)
    #         .group_by(Question1)
    #     )
    #             result = await session.execute(query)
    #             rows = result.fetchall()
    #             for row in rows:


if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
