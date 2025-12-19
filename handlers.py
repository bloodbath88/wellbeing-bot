# handlers.py — ФИНАЛЬНАЯ ВЕРСИЯ ДЛЯ Python 3.13 + aiogram 3.13.1
import asyncio
from aiogram import Router, F, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards import *
from database import (
    add_user, update_daily_trackers, get_today_trackers,
    save_mood, has_mood_today, get_points, unlock_achievement,
    get_achievements, add_points
)

dp = Dispatcher()
router = Router()
dp.include_router(router)

class Form(StatesGroup):
    water = State()
    sleep = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    add_user(message.from_user.id, message.from_user.first_name, message.from_user.username)
    await message.answer(
        "Привет! Я твой цифровой наставник по благополучию\n\n"
        "Я помогу найти баланс между телом, душой и развитием\n"
        "Выбери, с чего начнём сегодня?",
        reply_markup=main_menu
    )

@router.callback_query(F.data == "main")
async def back_to_main(call: CallbackQuery):
    await call.message.edit_text("Главное меню — выбирай блок:", reply_markup=main_menu)
    await call.answer()

# === БЛОК ТЕЛО ===
@router.callback_query(F.data == "block_body")
async def body_menu_handler(call: CallbackQuery):
    await call.message.edit_text(
        "Физическое благополучие (Тело)\n\n"
        "Формируем здоровые привычки — что будем делать?",
        reply_markup=body_menu
    )
    await call.answer()

@router.callback_query(F.data == "tracker")
async def tracker_menu_handler(call: CallbackQuery):
    stats = get_today_trackers(call.from_user.id)
    water = stats["water"] if stats else 0
    sleep = stats["sleep"] if stats else 0
    await call.message.edit_text(
        f"Трекер активности\n\n"
        f"Сегодня:\nВода: {water} л\nСон: {sleep} ч\n\n"
        f"Что запишем?",
        reply_markup=tracker_menu
    )
    await call.answer()

@router.callback_query(F.data.in_({"track_water", "track_sleep"}))
async def ask_tracker(call: CallbackQuery, state: FSMContext):
    if call.data == "track_water":
        await state.set_state(Form.water)
        await call.message.edit_text("Сколько литров воды выпил сегодня?\nНапример: 1.5")
    else:
        await state.set_state(Form.sleep)
        await call.message.edit_text("Сколько часов спал прошлой ночью?\nНапример: 8")
    await call.answer()

@router.message(Form.water)
async def save_water(message: Message, state: FSMContext):
    try:
        value = float(message.text.replace(",", "."))
        update_daily_trackers(message.from_user.id, water_liters=value)
        add_points(message.from_user.id, 5)
        unlock_achievement(message.from_user.id, "Гидратация +1", "Записал воду", "Droplet")
        stats = get_today_trackers(message.from_user.id)
        water = stats["water"] if stats else value
        sleep = stats["sleep"] if stats else 0
        await message.answer(
            f"Записал воду! Молодец 💧\n\nСегодня:\nВода: {water} л\nСон: {sleep} ч",
            reply_markup=body_menu
        )
    except:
        await message.answer("Напиши число, например 1.5")
    await state.clear()

@router.message(Form.sleep)
async def save_sleep(message: Message, state: FSMContext):
    try:
        value = float(message.text.replace(",", "."))
        hours = int(value)
        update_daily_trackers(message.from_user.id, sleep_hours=hours)
        add_points(message.from_user.id, 5)
        stats = get_today_trackers(message.from_user.id)
        water = stats["water"] if stats else 0
        sleep = stats["sleep"] if stats else hours
        await message.answer(
            f"Сон {hours} ч — отлично отдыхаем! 😴\n\nСегодня:\nВода: {water} л\nСон: {sleep} ч",
            reply_markup=body_menu
        )
    except:
        await message.answer("Напиши целое число (например: 8)")
    await state.clear()

@router.callback_query(F.data == "knowledge")
async def knowledge(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="block_body")]
    ])
    await call.message.edit_text(
        "Полезный перекус для мозга:\n\n"
        "Грецкие орехи + тёмный шоколад + ягоды = суперсила для учёбы 🍫🥜🫐",
        reply_markup=kb
    )
    await call.answer()

@router.callback_query(F.data == "challenges")
async def challenges(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="block_body")]
    ])
    await call.message.edit_text(
        "Челлендж на сегодня:\n\n"
        "Сделай 5-минутную зарядку прямо сейчас!\n\n"
        "Выполнил? → Отметь в трекере и получи очки 💪",
        reply_markup=kb
    )
    await call.answer()

# === БЛОК ДУША ===
@router.callback_query(F.data == "block_soul")
async def soul_menu_handler(call: CallbackQuery):
    await call.message.edit_text(
        "Психологическое благополучие (Душа)\n\n"
        "Эмоциональная поддержка — что тебе нужно прямо сейчас?",
        reply_markup=soul_menu
    )
    await call.answer()

@router.callback_query(F.data == "sos")
async def sos(call: CallbackQuery):
    await call.message.edit_text(
        "Дыхательная практика 4-7-8\n\n"
        "Вдохни на 4 секунды\n"
        "Задержи дыхание на 7 секунд\n"
        "Медленно выдохни на 8 секунд\n\n"
        "Повтори 4 раза — станет легче 💙",
        reply_markup=back_to_soul_kb
    )
    await call.answer()

@router.callback_query(F.data == "navigator")
async def navigator_handler(call: CallbackQuery):
    await call.message.edit_text("Выбери проблему:", reply_markup=navigator_menu)
    await call.answer()

@router.callback_query(F.data.startswith("nav_"))
async def navigator_problems(call: CallbackQuery):
    texts = {
        "nav_bullying": "При буллинге:\n• Поговори с доверенным взрослым\n• Запиши факты\n• Ты не один — поддержка рядом",
        "nav_parents": "Конфликты с родителями:\n• Выбери спокойный момент\n• Говори от «я»: «Мне тяжело, когда...»\n• Предложи решение вместе",
        "nav_exam": "Стресс перед экзаменами:\n• Делай перерывы каждые 25 мин\n• Дыши 4-7-8\n• Ты готов больше, чем думаешь"
    }
    await call.message.edit_text(texts.get(call.data, "Нет совета"), reply_markup=back_to_soul_kb)
    await call.answer()

@router.callback_query(F.data == "mood_diary")
async def mood_diary(call: CallbackQuery):
    if has_mood_today(call.from_user.id):
        await call.message.edit_text("Ты уже отметил настроение сегодня! Завтра новый день 🌅", reply_markup=back_to_soul_kb)
    else:
        await call.message.edit_text("Как твоё настроение сегодня?", reply_markup=mood_keyboard)
    await call.answer()

@router.callback_query(F.data.startswith("mood_"))
async def save_mood_cb(call: CallbackQuery):
    mood_map = {
        "mood_Отлично": "Отлично", "mood_Хорошо": "Хорошо", "mood_Нормально": "Нормально",
        "mood_Грустно": "Грустно", "mood_Плохо": "Плохо"
    }
    mood = mood_map.get(call.data, "Неизвестно")
    save_mood(call.from_user.id, mood)
    await call.message.edit_text(f"Записал: {mood}\nСпасибо, что поделился со мной 💛", reply_markup=back_to_soul_kb)
    await call.answer()

# === БЛОК РАЗВИТИЕ ===
@router.callback_query(F.data == "block_dev")
async def dev_menu_handler(call: CallbackQuery):
    await call.message.edit_text(
        "Социальное благополучие (Развитие)\n\n"
        "Помощь в учёбе и адаптации — что будем прокачивать?",
        reply_markup=dev_menu
    )
    await call.answer()

@router.callback_query(F.data == "time_mgmt")
async def pomodoro(call: CallbackQuery):
    await call.message.edit_text(
        "Pomodoro запущен!\n\n"
        "25 минут сосредоточенной работы ⏳\n"
        "Потом 5 минут отдыха\n"
        "Я напомню, когда перерыв!",
        reply_markup=back_to_main_kb
    )
    await call.answer()
    # 25 минут работы
    await asyncio.sleep(25 * 60)
    try:
        await call.message.answer("Время перерыва! Отдохни 5 минут 🕔")
    except Exception:
        # Сообщение могло быть удалено/изменено — просто игнорируем
        pass
    # 5 минут отдыха
    await asyncio.sleep(5 * 60)
    try:
        await call.message.answer("Цикл завершён! Готов повторить? 🔁")
    except Exception:
        pass

@router.callback_query(F.data == "prof_test")
async def prof_test(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="block_dev")]
    ])
    await call.message.edit_text(
        "Мини-тест: Ты больше любишь:\n\n"
        "А) Работать с людьми → ты эмпат\n"
        "Б) Работать с техникой → ты аналитик\n"
        "В) Творить → ты креатор",
        reply_markup=kb
    )
    await call.answer()

@router.callback_query(F.data == "soft_skills")
async def soft_skills(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="block_dev")]
    ])
    await call.message.edit_text(
        "Софт-скиллы (коммуникация, эмпатия, сотрудничество)\n\n"
        "Совет на сегодня:\n"
        "1) Слушай активно: перефразируй услышанное.\n"
        "2) Задавай уточняющие вопросы.\n"
        "3) Благодари за откровенность.\n\n"
        "Попробуй применить это сегодня!",
        reply_markup=kb
    )
    await call.answer()

@router.callback_query(F.data == "my_stats")
async def my_stats(call: CallbackQuery):
    points = get_points(call.from_user.id)
    achs = get_achievements(call.from_user.id)
    text = f"Твои очки: {points}\n\nДостижения:\n"
    text += "\n".join(f"{a['emoji']} {a['title']}" for a in achs) if achs else "Пока нет — но всё впереди!"
    await call.message.edit_text(text, reply_markup=back_to_main_kb)
    await call.answer()
