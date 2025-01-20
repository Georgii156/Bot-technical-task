from aiogram import Router, F
from aiogram import types
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime
import random
from aiogram.fsm.state import State, StatesGroup
from bot.db_creation import save_diary_entry, get_diary_entries 
from bot.Fsm import UserState

router = Router()

@router.callback_query(F.data == "option1")
async def option_1_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserState.waiting_for_physical_exercise)
    await callback_query.answer()
    await callback_query.message.answer("🤸‍♂️ Напишите физическое упражнение.")

@router.message(UserState.waiting_for_physical_exercise)
async def process_physical_exercise(message: Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_cognitive_exercise)
    physical_exercise = message.text
    await state.update_data(physical_exercise=physical_exercise)
    await message.answer("🧘 Теперь напишите когнитивное упражнение.")

@router.message(UserState.waiting_for_cognitive_exercise)
async def process_cognitive_exercise(message: Message, state: FSMContext):
    await state.set_state(UserState.waiting_for_effect)
    cognitive_exercise = message.text
    await state.update_data(cognitive_exercise=cognitive_exercise)
    await message.answer("🤧 Теперь напишите ваше самочувствие.")

@router.message(UserState.waiting_for_effect)
async def process_effect(message: Message, state: FSMContext):
    effect = message.text
    user_id = message.from_user.id
    user_data = await state.get_data()

    physical_exercise = user_data.get("physical_exercise")
    cognitive_exercise = user_data.get("cognitive_exercise")

    await save_diary_entry(user_id, physical_exercise, cognitive_exercise, effect)

    await message.answer("✅ Ваш дневник успешно записан!")
    await state.clear()

@router.callback_query(F.data == "option2")
async def option_2_handler(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    records = await get_diary_entries(user_id)

    if records:
        diary_entries = "\n".join([f"|- Дата: {entry[0]}\nФизическое упражнение: {entry[1]}\nКогнитивное упражнение: {entry[2]}\nСамочувствие: {entry[3]}\n" for entry in records])
        await callback_query.answer()
        await callback_query.message.answer(diary_entries)
    else:
        await callback_query.answer()
        await callback_query.message.answer("😭 У вас нет записей в дневнике.")