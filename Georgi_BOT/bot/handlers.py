from aiogram import Router, F
from aiogram import Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from bot.db_creation import get_user_name, insert_user, update_user, save_feedback, save_diary_entry
from bot.keyboard import create_dynamic_menu
from bot.inline_handlers import router as inline_router
from bot.LLM import get_response
from bot.Fsm import UserState
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

router = Router()
scheduler = AsyncIOScheduler()

async def send_notify(user_id: int, bot: Bot):
    user = await get_user_name(user_id)
    await bot.send_message(user_id, f"🙋 {user}, делали сегодня упражнения? Можем обсудить!")

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user_name(user_id)

    if user:
        username, chat_enabled = user
        await message.answer(
            f"👋 Рад видеть снова, {username}!",
            reply_markup=create_dynamic_menu(chat_enabled)
        )
    else:
        await insert_user(user_id, {"name": None, "chat_enabled": False})
        await message.answer("🤝 Приветствую, как Вас зовут?")
        await state.set_state(UserState.waiting_for_name)

    bot = message.bot
    scheduler.add_job(
        send_notify, 
        trigger=IntervalTrigger(hours=24),
        args=[user_id, bot],
        max_instances=1
    )
    scheduler.start()

@router.message(F.text == "Изменить имя")
async def change_username_prompt(message: Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_name)
    await message.reply("🙌 Как Вас называть?")

@router.message(UserState.waiting_for_name)
async def change_username(message: Message, state: FSMContext):
    new_username = message.text
    user_id = message.from_user.id

    await update_user(user_id, {"name": new_username})
    await message.reply(f"Отлично, {new_username}!")
    await state.clear()

@router.message(Command("review"))
async def feedback_handler(message: Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_feedback)
    await message.reply("✍️ Можете написать отзыв:")

@router.message(UserState.waiting_for_feedback)
async def save_feedback_handler(message: Message, state: FSMContext):
    feedback_text = message.text
    user_id = message.from_user.id

    await save_feedback(user_id, feedback_text)
    await message.reply("Спасибо за отзыв!")
    
    await state.clear()

@router.message(Command("information"))
async def information_handler(message: Message):
    instruction_text = (
        "|-Как этим пользоваться?\n\n"
        "|-- /start — Запуск бота\n"
        "|-- /information — Инструкции\n"
        "|-- /review — Оставить отзыв\n"
        "|-- 'Включить чат'-'Выключить чат' — Общение с экспертом по нейропластичности мозга\n"
        "|-- 'Изменить имя' — Смена имени\n"
        "|-- 'Опции' — Узнать цитату и совет дня\n"
    )
    await message.answer(instruction_text)

@router.message(F.text == "Включить чат")
async def chat_start_handler(message: Message):
    user_id = message.from_user.id
    await update_user(user_id, {"chat_enabled": True})
    await message.answer("✅ Чат включен!", reply_markup=create_dynamic_menu(True))

@router.message(F.text == "Выключить чат")
async def chat_end_handler(message: Message):
    user_id = message.from_user.id
    await update_user(user_id, {"chat_enabled": False})
    await message.answer("❌ Чат выключен, буду ждать нового диалога!", reply_markup=create_dynamic_menu(False))

@router.message(F.text == "Опции")
async def show_options_handler(message: Message):
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Запись в дневник", callback_data="option1")],
        [InlineKeyboardButton(text="Посмотреть записи", callback_data="option2")]
    ])
    await message.answer("🙈 Выберите опцию ниже:", reply_markup=inline_keyboard)

@router.message()
async def conversation_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user = await get_user_name(user_id)

    if user and user[1]:
        user_message = message.text
        model_response = get_response(user_message)
        await message.answer(model_response)

    elif await state.get_state() == UserState.waiting_for_physical_exercise.state:
        await state.update_data(physical_exercise=message.text)
        await state.set_state(UserState.waiting_for_cognitive_exercise)
        await message.answer("🧘 Теперь напишите когнитивное упражнение.")

    elif await state.get_state() == UserState.waiting_for_cognitive_exercise.state:
        await state.update_data(cognitive_exercise=message.text)
        await state.set_state(UserState.waiting_for_effect)
        await message.answer("🤧 Теперь напишите ваше самочувствие.")

    elif await state.get_state() == UserState.waiting_for_effect.state:
        user_data = await state.get_data()
        physical_exercise = user_data.get("physical_exercise")
        cognitive_exercise = user_data.get("cognitive_exercise")

        entry_date = datetime.now().strftime("%Y-%m-%d")
        await save_diary_entry(
            user_id=user_id,
            physical_exercise=physical_exercise,
            cognitive_exercise=cognitive_exercise,
            effect=message.text
        )

        await message.answer(f"✅ Дневник записан на {entry_date}!\n")
        await state.clear()

    else:
        await message.answer("‼️ Вы не в чате сейчас. Включите чат!")

router.include_router(inline_router)
