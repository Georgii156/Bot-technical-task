from aiogram.fsm.state import State, StatesGroup

class UserState(StatesGroup):
    waiting_for_name = State()
    waiting_for_feedback = State() 
    waiting_for_physical_exercise = State()
    waiting_for_cognitive_exercise = State()
    waiting_for_effect = State()