# keyboards.py — ПОСЛЕДНЯЯ РАБОЧАЯ ВЕРСИЯ (проверено на Python 3.13 + aiogram 3.13.1)
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# === ГЛАВНОЕ МЕНЮ ===
main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Физическое благополучие (Тело)", callback_data="block_body")],
        [InlineKeyboardButton(text="Психологическое благополучие (Душа)", callback_data="block_soul")],
        [InlineKeyboardButton(text="Социальное благополучие (Развитие)", callback_data="block_dev")],
        [InlineKeyboardButton(text="Моя статистика", callback_data="my_stats")]
    ]
)

# === БЛОК ТЕЛО ===
body_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Трекер активности", callback_data="tracker")],
        [InlineKeyboardButton(text="База знаний", callback_data="knowledge")],
        [InlineKeyboardButton(text="Челленджи", callback_data="challenges")],
        [InlineKeyboardButton(text="Назад", callback_data="main")]
    ]
)

tracker_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Записать воду", callback_data="track_water")],
        [InlineKeyboardButton(text="Записать сон", callback_data="track_sleep")],
        [InlineKeyboardButton(text="Назад", callback_data="block_body")]
    ]
)

# === БЛОК ДУША ===
soul_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="SOS (анти-стресс)", callback_data="sos")],
        [InlineKeyboardButton(text="Навигатор помощи", callback_data="navigator")],
        [InlineKeyboardButton(text="Дневник настроения", callback_data="mood_diary")],
        [InlineKeyboardButton(text="Назад", callback_data="main")]
    ]
)

navigator_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Буллинг", callback_data="nav_bullying")],
        [InlineKeyboardButton(text="Конфликты с родителями/учителями", callback_data="nav_parents")],
        [InlineKeyboardButton(text="Стресс перед экзаменами", callback_data="nav_exam")],
        [InlineKeyboardButton(text="Назад", callback_data="block_soul")]
    ]
)

back_to_soul_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="block_soul")]]
)

mood_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отлично", callback_data="mood_Отлично")],
        [InlineKeyboardButton(text="Хорошо", callback_data="mood_Хорошо")],
        [InlineKeyboardButton(text="Нормально", callback_data="mood_Нормально")],
        [InlineKeyboardButton(text="Грустно", callback_data="mood_Грустно")],
        [InlineKeyboardButton(text="Плохо", callback_data="mood_Плохо")],
        [InlineKeyboardButton(text="Назад", callback_data="block_soul")]
    ]
)

# === БЛОК РАЗВИТИЕ ===
dev_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Тайм-менеджмент (Pomodoro)", callback_data="time_mgmt")],
        [InlineKeyboardButton(text="Профориентация / Самопознание", callback_data="prof_test")],
        [InlineKeyboardButton(text="Софт-скиллы", callback_data="soft_skills")],
        [InlineKeyboardButton(text="Назад", callback_data="main")]
    ]
)

back_to_main_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="В главное меню", callback_data="main")]]
)