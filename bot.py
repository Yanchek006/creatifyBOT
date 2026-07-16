import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

# --- НАСТРОЙКА ЛОГИРОВАНИЯ ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

TOKEN = "8956581254:AAEfx3P42nb10QiDDv5HJjyBvCYLJwid0f8"
CHAT_ID = "995444571"

# --- СОЗДАЕМ БОТА БЕЗ ДОПОЛНИТЕЛЬНЫХ СЕССИЙ (ПРОСТОЙ ВАРИАНТ) ---
try:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    logger.info("✅ Бот успешно инициализирован")
except Exception as e:
    logger.error(f"❌ Ошибка инициализации бота: {e}")
    sys.exit(1)

dp = Dispatcher()

# Хранилище прогресса пользователей
user_progress = {}

# --- КЛАВИАТУРА ---
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎓 Начать обучение")],
        [KeyboardButton(text="📚 Мои подарки"), KeyboardButton(text="📞 Связаться")],
        [
            KeyboardButton(text="💡 Полезная информация"),
            KeyboardButton(text="🌐 На сайт"),
        ],
    ],
    resize_keyboard=True,
)


# ============================================
# СТАРТ
# ============================================
@dp.message(CommandStart())
async def start(message: Message):
    user_progress[message.from_user.id] = {"step": 0, "score": 0}

    await message.answer(
        "🧙‍♂️ <b>Добро пожаловать в CREATIFY!</b>\n\n"
        "Я помогу тебе прокачать навыки в дизайне.\n\n"
        "🎓 <b>«Начать обучение»</b> — интерактивный квест из 9 заданий\n"
        "📚 <b>«Мои подарки»</b> — чек-лист и шаблоны\n"
        "💡 <b>«Полезная информация»</b> — советы и лайфхаки\n"
        "🌐 <b>«На сайт»</b> — перейти на сайт CREATIFY\n\n"
        "👇 Выбери, с чего начнём!",
        reply_markup=main_kb,
    )


# ============================================
# 📚 МОИ ПОДАРКИ
# ============================================
@dp.message(lambda message: message.text == "📚 Мои подарки")
async def gifts(message: Message):
    await message.answer(
        "🎁 <b>Твои подарки от CREATIFY:</b>\n\n"
        "📋 <b>Чек-лист дизайнера</b>\n"
        "1. Проверь контраст\n"
        "2. Проверь иерархию\n"
        "3. Проверь адаптив\n"
        "4. Проверь скорость загрузки\n"
        "5. Проверь читаемость текста\n\n"
        "🖼 <b>Готовые плашки для работы:</b>\n"
        "• Обложка для соцсетей\n"
        "• Презентация 5 слайдов\n"
        "• Инфографика 3 варианта\n\n"
        "📌 <i>Напиши @AvoError — вышлю все файлы!</i>"
    )


# ============================================
# 📞 СВЯЗАТЬСЯ
# ============================================
@dp.message(lambda message: message.text == "📞 Связаться")
async def contact(message: Message):
    await message.answer(
        "📬 <b>Связаться со мной:</b>\n\n"
        "📱 Telegram: @AvoError\n"
        "📧 Email: creatify_cf@mail.ru\n"
        "📞 Телефон: +7 (903) 738-02-76\n\n"
        "💬 <i>Всегда на связи по вопросам дизайна!</i>"
    )


# ============================================
# 🌐 НА САЙТ
# ============================================
@dp.message(lambda message: message.text == "🌐 На сайт")
async def site(message: Message):
    await message.answer(
        "🌐 <b>Сайт CREATIFY</b>\n\n"
        "👉 https://yanchek006.github.io/creatify/\n\n"
        "📖 <b>На сайте ты найдёшь:</b>\n"
        "• Портфолио\n"
        "• Услуги по дизайну\n"
        "• Обучение и курсы\n"
        "• Полезные статьи\n\n"
        "<i>Выбирай своё направление и стартуй!</i>"
    )


# ============================================
# 💡 ПОЛЕЗНАЯ ИНФОРМАЦИЯ
# ============================================
@dp.message(lambda message: message.text == "💡 Полезная информация")
async def useful_info(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎨 3 фишки презентации", callback_data="info_fishki"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Инфографика для WB", callback_data="info_wb"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📚 ТОП-5 книг по дизайну", callback_data="info_books"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💡 Лайфхаки дизайнера", callback_data="info_lifehacks"
                )
            ],
        ]
    )
    await message.answer(
        "💡 <b>Полезная информация для дизайнера</b>\n\n"
        "Выбери тему, которая тебя интересует 👇",
        reply_markup=kb,
    )


# ============================================
# 🎓 НАЧАТЬ ОБУЧЕНИЕ - ГЛАВНОЕ МЕНЮ
# ============================================
@dp.message(lambda message: message.text == "🎓 Начать обучение")
async def start_quest(message: Message):
    user_id = message.from_user.id
    if user_id not in user_progress:
        user_progress[user_id] = {"step": 0, "score": 0}

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Стартовать квест", callback_data="quest_intro"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📊 Мой прогресс", callback_data="quest_progress"
                )
            ],
        ]
    )
    await message.answer(
        "🎓 <b>Добро пожаловать в КВЕСТ-МАРАФОН CREATIFY!</b>\n\n"
        "🔥 <b>9 заданий</b>, которые прокачают твой скилл\n"
        "🏆 <b>Система баллов</b> — зарабатывай очки\n"
        "💡 <b>Реальные кейсы</b> из практики\n\n"
        "А после 9 задания тебя ждёт <b>БОНУС</b> 🎁\n\n"
        "Готов стать профи? Погнали! 👇",
        reply_markup=kb,
    )


# ============================================
# ПРОГРЕСС
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_progress")
async def show_progress(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_progress:
        user_progress[user_id] = {"step": 0, "score": 0}

    step = user_progress[user_id]["step"]
    score = user_progress[user_id]["score"]

    await callback.message.answer(
        f"📊 <b>Твой прогресс</b>\n\n"
        f"✅ Пройдено заданий: {step}/9\n"
        f"⭐ Набрано баллов: {score}\n\n"
    )
    await callback.answer()


# ============================================
# КВЕСТ - ВСТУПЛЕНИЕ
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_intro")
async def quest_intro(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Задание 1", callback_data="quest_1")]
        ]
    )

    await callback.message.answer(
        "🎯 <b>КВЕСТ-МАРАФОН СТАРТУЕТ!</b>\n\n"
        "Ты - начинающий дизайнер. Твоя задача — пройти 9 заданий.\n\n"
        "📌 <b>Правила:</b>\n"
        "• На каждый вопрос — 2 варианта ответа\n"
        "• За правильный ответ +1 балл\n"
        "• В конце — бонус 🎁\n\n"
        "Готов? Начинаем! 👇",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ЗАДАНИЕ 1: СИНДРОМ САМОЗВАНЦА
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_1")
async def quest_1(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="😰 Переделать всё с нуля", callback_data="q1_wrong"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💪 Объяснить свой выбор", callback_data="q1_right"
                )
            ],
        ]
    )

    await callback.message.answer(
        "📌 <b>Задание 1/9: Синдром самозванца</b>\n\n"
        "Ты сделал классный макет, но клиент пишет:\n"
        "«Ммм… давай попробуем по-другому?»\n\n"
        "🤔 <b>Твои действия?</b>",
        reply_markup=kb,
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data in ["q1_right", "q1_wrong"])
async def quest_1_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id not in user_progress:
        user_progress[user_id] = {"step": 0, "score": 0}

    if callback.data == "q1_right":
        user_progress[user_id]["score"] += 1
        text = "✅ <b>Верно!</b> Объясни клиенту, почему ты сделал так — это твоя суперсила!"
    else:
        text = (
            "❌ <b>Ошибка!</b> Не переделывай всё с нуля — объясни свой выбор клиенту."
        )

    user_progress[user_id]["step"] = 1

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Задание 2", callback_data="quest_2")]
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        f"{text}\n\n"
        f"⭐ Баллы: {user_progress[user_id]['score']}\n"
        f"📊 Прогресс: {user_progress[user_id]['step']}/9\n\n"
        "Погнали дальше! 👇",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ЗАДАНИЕ 2: БРИФ
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_2")
async def quest_2(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🤝 Начать работу сразу", callback_data="q2_wrong"
                )
            ],
            [InlineKeyboardButton(text="📋 Запросить бриф", callback_data="q2_right")],
        ]
    )

    await callback.message.answer(
        "📌 <b>Задание 2/9: Бриф</b>\n\n"
        "Клиент говорит: «Сделай мне сайт, я потом скажу, что нравится».\n\n"
        "🤔 <b>Твои действия?</b>",
        reply_markup=kb,
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data in ["q2_right", "q2_wrong"])
async def quest_2_answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "q2_right":
        user_progress[user_id]["score"] += 1
        text = (
            "✅ <b>Верно!</b> Бриф — спасение от 100 правок! 5 вопросов спасут нервы."
        )
    else:
        text = (
            "❌ <b>Ошибка!</b> Без брифа ты утонешь в правках. Всегда запрашивай бриф!"
        )

    user_progress[user_id]["step"] = 2

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Задание 3", callback_data="quest_3")]
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        f"{text}\n\n"
        f"⭐ Баллы: {user_progress[user_id]['score']}\n"
        f"📊 Прогресс: {user_progress[user_id]['step']}/9\n\n"
        "Ещё одно задание! 👇",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ЗАДАНИЕ 3: РЕФЕРЕНСЫ
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_3")
async def quest_3(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎨 Сделать по своему вкусу", callback_data="q3_wrong"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📸 Показать референсы", callback_data="q3_right"
                )
            ],
        ]
    )

    await callback.message.answer(
        "📌 <b>Задание 3/9: Референсы</b>\n\n"
        "Клиент не может объяснить, какой стиль хочет.\n\n"
        "🤔 <b>Твои действия?</b>",
        reply_markup=kb,
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data in ["q3_right", "q3_wrong"])
async def quest_3_answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "q3_right":
        user_progress[user_id]["score"] += 1
        text = "✅ <b>Верно!</b> Референсы — это язык, который понимает клиент!"
    else:
        text = "❌ <b>Ошибка!</b> Ты не экстрасенс. Всегда показывай референсы!"

    user_progress[user_id]["step"] = 3

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Задание 4", callback_data="quest_4")]
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        f"{text}\n\n"
        f"⭐ Баллы: {user_progress[user_id]['score']}\n"
        f"📊 Прогресс: {user_progress[user_id]['step']}/9\n\n"
        "Продолжаем! 👇",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ЗАДАНИЕ 4: ПРАВКИ
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_4")
async def quest_4(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Правки устно", callback_data="q4_wrong")],
            [
                InlineKeyboardButton(
                    text="📋 Правки письменно", callback_data="q4_right"
                )
            ],
        ]
    )

    await callback.message.answer(
        "📌 <b>Задание 4/9: Правки</b>\n\n"
        "Клиент прислал 5 голосовых с правками.\n\n"
        "🤔 <b>Как лучше работать с правками?</b>",
        reply_markup=kb,
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data in ["q4_right", "q4_wrong"])
async def quest_4_answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "q4_right":
        user_progress[user_id]["score"] += 1
        text = "✅ <b>Верно!</b> Письменные правки — это порядок, а не хаос в чате!"
    else:
        text = "❌ <b>Ошибка!</b> Голосовые правки — это хаос. Только письменно!"

    user_progress[user_id]["step"] = 4

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Задание 5", callback_data="quest_5")]
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        f"{text}\n\n"
        f"⭐ Баллы: {user_progress[user_id]['score']}\n"
        f"📊 Прогресс: {user_progress[user_id]['step']}/9\n\n"
        "Уже половина! 👇",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ЗАДАНИЕ 5: КЛИЕНТСКИЙ ВКУС
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_5")
async def quest_5(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎨 Спросить «Нравится?»", callback_data="q5_wrong"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💼 Спросить «Решает задачу?»", callback_data="q5_right"
                )
            ],
        ]
    )

    await callback.message.answer(
        "📌 <b>Задание 5/9: Вкус VS Бизнес</b>\n\n"
        "Клиент говорит: «Мне не нравится этот цвет».\n\n"
        "🤔 <b>Что спросить?</b>",
        reply_markup=kb,
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data in ["q5_right", "q5_wrong"])
async def quest_5_answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "q5_right":
        user_progress[user_id]["score"] += 1
        text = "✅ <b>Верно!</b> «Нравится» — про вкус, «Решает задачу» — про бизнес!"
    else:
        text = "❌ <b>Ошибка!</b> Не спрашивай «Нравится?» — спрашивай «Решает задачу?»"

    user_progress[user_id]["step"] = 5

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Задание 6", callback_data="quest_6")]
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        f"{text}\n\n"
        f"⭐ Баллы: {user_progress[user_id]['score']}\n"
        f"📊 Прогресс: {user_progress[user_id]['step']}/9\n\n"
        "Ты в зоне! 👇",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ЗАДАНИЕ 6: ИНФОГРАФИКА
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_6")
async def quest_6(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Только текст", callback_data="q6_wrong")],
            [InlineKeyboardButton(text="🎨 Текст + визуал", callback_data="q6_right")],
        ]
    )

    await callback.message.answer(
        "📌 <b>Задание 6/9: Инфографика</b>\n\n"
        "Клиент просит сделать презентацию с цифрами.\n\n"
        "🤔 <b>Как лучше подать информацию?</b>",
        reply_markup=kb,
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data in ["q6_right", "q6_wrong"])
async def quest_6_answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "q6_right":
        user_progress[user_id]["score"] += 1
        text = "✅ <b>Верно!</b> Инфографика увеличивает понимание и запоминаемость!"
    else:
        text = "❌ <b>Ошибка!</b> Только текст — это скучно. Инфографика продаёт!"

    user_progress[user_id]["step"] = 6

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Задание 7", callback_data="quest_7")]
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        f"{text}\n\n"
        f"⭐ Баллы: {user_progress[user_id]['score']}\n"
        f"📊 Прогресс: {user_progress[user_id]['step']}/9\n\n"
        "Ты крут! 👇",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ЗАДАНИЕ 7: КОНТРАСТ
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_7")
async def quest_7(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔴 Игнорировать", callback_data="q7_wrong")],
            [
                InlineKeyboardButton(
                    text="🟢 Проверить контраст", callback_data="q7_right"
                )
            ],
        ]
    )

    await callback.message.answer(
        "📌 <b>Задание 7/9: Контраст</b>\n\n"
        "Ты сделал дизайн, но текст на сайте плохо читается.\n\n"
        "🤔 <b>Что делать?</b>",
        reply_markup=kb,
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data in ["q7_right", "q7_wrong"])
async def quest_7_answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "q7_right":
        user_progress[user_id]["score"] += 1
        text = (
            "✅ <b>Верно!</b> Контраст — это читаемость. Без него пользователь уйдёт!"
        )
    else:
        text = "❌ <b>Ошибка!</b> Контраст — основа юзабилити. Всегда проверяй!"

    user_progress[user_id]["step"] = 7

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📖 Задание 8", callback_data="quest_8")]
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        f"{text}\n\n"
        f"⭐ Баллы: {user_progress[user_id]['score']}\n"
        f"📊 Прогресс: {user_progress[user_id]['step']}/9\n\n"
        "Осталось 2 задания! 👇",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ЗАДАНИЕ 8: АДАПТИВ
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_8")
async def quest_8(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📱 Только десктоп", callback_data="q8_wrong")],
            [
                InlineKeyboardButton(
                    text="📱📱 Адаптив под все устройства", callback_data="q8_right"
                )
            ],
        ]
    )

    await callback.message.answer(
        "📌 <b>Задание 8/9: Адаптив</b>\n\n"
        "Клиент говорит: «Сайт должен быть на телефоне».\n\n"
        "🤔 <b>Что ты сделаешь?</b>",
        reply_markup=kb,
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data in ["q8_right", "q8_wrong"])
async def quest_8_answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "q8_right":
        user_progress[user_id]["score"] += 1
        text = "✅ <b>Верно!</b> Адаптив — это про уважение к пользователю!"
    else:
        text = "❌ <b>Ошибка!</b> 60% трафика с телефонов. Без адаптива ты теряешь клиентов!"

    user_progress[user_id]["step"] = 8

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎁 ПОСЛЕДНЕЕ ЗАДАНИЕ → БОНУС", callback_data="quest_9"
                )
            ]
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        f"{text}\n\n"
        f"⭐ Баллы: {user_progress[user_id]['score']}\n"
        f"📊 Прогресс: {user_progress[user_id]['step']}/9\n\n"
        "🎁 <b>Осталось последнее задание!</b>\n"
        "После него тебя ждёт <b>БОНУС</b> — готовый PDF-файл по дизайну!\n\n"
        "Нажми на кнопку 👇",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ЗАДАНИЕ 9: ОБЛОЖКА + ПРОДАЖА
# ============================================
@dp.callback_query(lambda callback: callback.data == "quest_9")
async def quest_9(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Сделать просто", callback_data="q9_wrong")],
            [
                InlineKeyboardButton(
                    text="🔥 Сделать цепляющей", callback_data="q9_right"
                )
            ],
        ]
    )

    await callback.message.answer(
        "📌 <b>Задание 9/9: Обложка для Wildberries</b>\n\n"
        "Ты готовишь карточку товара для Wildberries.\n"
        "От обложки зависит, купит товар или нет.\n\n"
        "🤔 <b>Какую обложку ты сделаешь?</b>\n\n"
        "💡 <i>Правильный ответ откроет тебе доступ к бонусу!</i>",
        reply_markup=kb,
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data in ["q9_right", "q9_wrong"])
async def quest_9_answer(callback: CallbackQuery):
    user_id = callback.from_user.id

    if callback.data == "q9_right":
        user_progress[user_id]["score"] += 1
        text = "✅ <b>Верно!</b> Цепляющая обложка увеличивает CTR в 2 раза!"
    else:
        text = "❌ <b>Ошибка!</b> Простая обложка не конкурирует. Делай цепляющей!"

    user_progress[user_id]["step"] = 9
    score = user_progress[user_id]["score"]

    # Определяем уровень
    if score >= 8:
        level = "🏆 <b>ПРОФИ!</b> Ты дизайнер-эксперт!"
    elif score >= 6:
        level = "🎯 <b>ПРОДВИНУТЫЙ!</b> Ты на правильном пути!"
    elif score >= 4:
        level = "📚 <b>УЧЕНИК!</b> У тебя есть потенциал!"
    else:
        level = "🎓 <b>НОВИЧОК!</b> Начни сначала, будет полезно!"

    # КНОПКА ПРОДАЖИ PDF
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📥 Хочу PDF-файл!", callback_data="buy_pdf")],
            [
                InlineKeyboardButton(
                    text="📖 Перейти на сайт",
                    url="https://yanchek006.github.io/creatify/",
                )
            ],
            [InlineKeyboardButton(text="📞 Связаться", callback_data="contact_final")],
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        f"🎉 <b>ПОЗДРАВЛЯЮ! Ты прошёл все 9 заданий!</b>\n\n"
        f"{level}\n\n"
        f"📊 <b>Твой результат:</b>\n"
        f"• Баллов: {score}/9\n"
        f"• Пройдено: 9/9 заданий\n\n"
        "🎁 <b>ТЕБЯ ЖДЁТ БОНУС!</b>\n\n"
        "📄 <b>PDF-ГИД «КАК СОЗДАТЬ ИНФОГРАФИКУ, КОТОРАЯ ПРОДАЁТ»</b>\n\n"
        "🔥 <b>Этот гид — твой пропуск в мир профессиональной инфографики!</b>\n\n"
        "📖 <b>Что внутри:</b>\n"
        "• ГЛАВА 1: Что такое инфографика и зачем она нужна\n"
        "• ГЛАВА 2: Основы инфографики — структура и композиция\n"
        "• ГЛАВА 3: Цвет, стиль и визуал — как сделать красиво\n"
        "• ГЛАВА 4: Техническая часть — инструменты и программы\n"
        "• ГЛАВА 5: Сбор карточки товара — пошаговый алгоритм\n"
        "• ГЛАВА 6: Дизайн карточки товара — готовые решения\n\n"
        "💡 <b>Почему этот гид стоит 999 ₽?</b>\n"
        "✅ Ты перестанешь тратить часы на переделки\n"
        "✅ Начнёшь создавать инфографику, которая продаёт\n"
        "✅ Получишь готовые шаблоны и чек-листы\n"
        "✅ Увеличишь свои чеки на проектах\n\n"
        "💰 <b>Цена: 999 ₽</b>\n"
        "Но для тебя <b>СКИДКА 50%</b> за прохождение квеста!\n\n"
        "🔥 <b>Твоя цена: 499 ₽</b>\n\n"
        "👇 Нажми, чтобы получить PDF-гид!",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ПОКУПКА PDF
# ============================================
@dp.callback_query(lambda callback: callback.data == "buy_pdf")
async def buy_pdf(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Я оплатил(а), жду файл!", callback_data="pay_pdf"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📞 Написать @AvoError", url="https://t.me/AvoError"
                )
            ],
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "📥 <b>PDF-ГИД «КАК СОЗДАТЬ ИНФОГРАФИКУ, КОТОРАЯ ПРОДАЁТ»</b>\n\n"
        "📄 <b>Что ты получишь:</b>\n"
        "✅ Пошаговый алгоритм создания инфографики\n"
        "✅ 6 глав с подробными инструкциями\n"
        "✅ Готовые шаблоны и чек-листы\n"
        "✅ Секреты цвета и композиции\n"
        "✅ Реальные примеры карточек товаров\n\n"
        "💡 <b>Цена: 499 ₽</b> (скидка 50% за прохождение квеста)\n\n"
        "💰 <b>Реквизиты для оплаты:</b>\n\n"
        "📱 <b>По номеру телефона:</b>\n"
        "+7 (903) 738-02-76 (Т-Банк/Сбер)\n\n"
        "🟢 <b>СБП (Система быстрых платежей):</b>\n"
        "Номер телефона: +7 (903) 738-02-76\n"
        "Банк получателя: Т-Банк\n\n"
        "📌 <i>После оплаты нажми кнопку «Я оплатил(а)» и отправь скриншот чека @AvoError</i>\n\n"
        "⏱ <b>Файл придёт в течение 5 минут после подтверждения оплаты!</b>",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# ПОДТВЕРЖДЕНИЕ ОПЛАТЫ
# ============================================
@dp.callback_query(lambda callback: callback.data == "pay_pdf")
async def pay_confirmation(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📞 Написать @AvoError", url="https://t.me/AvoError"
                )
            ]
        ]
    )

    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "✅ <b>Отлично! Ты сделал первый шаг!</b>\n\n"
        "📤 <b>Что делать дальше:</b>\n\n"
        "1️⃣ Открой чат с @AvoError\n"
        "2️⃣ Отправь скриншот чека об оплате\n"
        "3️⃣ Получи PDF-гид в течение 5 минут\n"
        "4️⃣ Начни создавать инфографику, которая продаёт! 🚀\n\n"
        "👇 Жми на кнопку, чтобы написать @AvoError",
        reply_markup=kb,
    )
    await callback.answer()


# ============================================
# КОНТАКТЫ
# ============================================
@dp.callback_query(lambda callback: callback.data == "contact_final")
async def contact_final(callback: CallbackQuery):
    await callback.message.answer(
        "📬 <b>Связаться со мной:</b>\n\n"
        "📱 Telegram: @AvoError\n"
        "📧 Email: creatify_cf@mail.ru\n\n"
        "💬 <i>Всегда на связи! Задавай вопросы по дизайну 😊</i>"
    )
    await callback.answer()


# ============================================
# ИНФО-ОБРАБОТЧИКИ
# ============================================
@dp.callback_query(lambda callback: callback.data == "info_fishki")
async def info_fishki(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "🎨 <b>ТОП-3 фишки презентации дизайна</b>\n\n"
        "1️⃣ Покажи путь: задача → решение → почему это работает\n"
        "2️⃣ Закрой возражения: покажи референсы и спроси «Тебе такой вайб?»\n"
        "3️⃣ Спроси «Решает задачу?» вместо «Нравится?»\n\n"
        "🎓 Подробнее на сайте CREATIFY!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📖 Перейти к обучению",
                        url="https://yanchek006.github.io/creatify/",
                    )
                ]
            ]
        ),
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data == "info_wb")
async def info_wb(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "📊 <b>Инфографика для WB</b>\n\n"
        "Хорошая обложка увеличивает CTR в 2 раза!\n"
        "• CTR 1% → 10 покупателей\n"
        "• CTR 2% → 20 покупателей\n\n"
        "👉 Пишите @AvoError — помогу с дизайном!"
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data == "info_books")
async def info_books(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "📚 <b>ТОП-5 книг по дизайну</b>\n\n"
        "1. Мунари — «Фантазия»\n"
        "2. Арнхейм — «Искусство и визуальное восприятие»\n"
        "3. Kleon — «Steal Like an Artist»\n"
        "4. Альберс — «Взаимодействие цвета»\n"
        "5. Фриман — «Дао цифровой фотографии»"
    )
    await callback.answer()


@dp.callback_query(lambda callback: callback.data == "info_lifehacks")
async def info_lifehacks(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass

    await callback.message.answer(
        "💡 <b>Лайфхаки дизайнера</b>\n\n"
        "1️⃣ Бриф до старта — 5 вопросов спасут нервы\n"
        "2️⃣ Правки только письменно — таблица вместо хаоса\n"
        "3️⃣ Референсы на утверждение — клиент подписывает направление\n\n"
        "👉 Подробнее: @AvoError"
    )
    await callback.answer()


# ============================================
# ЗАПУСК БОТА С АВТОМАТИЧЕСКИМ ПЕРЕЗАПУСКОМ
# ============================================
async def main():
    """Главная функция с автоматическим перезапуском при ошибках"""
    logger.info("🚀 Бот CREATIFY с квест-марафоном и продажей запущен!")

    # Бесконечный цикл с перезапуском при ошибках
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            logger.error(f"❌ Ошибка в работе бота: {e}")
            logger.info("🔄 Перезапуск бота через 5 секунд...")
            await asyncio.sleep(5)
        else:
            # Если поллинг остановился без ошибки, просто перезапускаем
            logger.info("🔄 Поллинг остановлен, перезапуск...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
